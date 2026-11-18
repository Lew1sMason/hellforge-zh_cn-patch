param(
    [Parameter(Mandatory = $true)][ValidateSet('Install', 'Restore')][string]$Mode,
    [Parameter(Mandatory = $true)][string]$HellForgeRoot
)

$ErrorActionPreference = 'Stop'

function Assert-PlainPath([string]$Path) {
    while ($Path) {
        if ((Test-Path -LiteralPath $Path) -and
            ((Get-Item -LiteralPath $Path -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw "Linked path is unsupported: $Path"
        }
        $Path = Split-Path -Parent $Path
    }
}

function Get-Sha256([string]$Path) {
    $stream = [IO.File]::OpenRead($Path)
    try {
        $algorithm = [Security.Cryptography.SHA256]::Create()
        try {
            [BitConverter]::ToString($algorithm.ComputeHash($stream)).Replace('-', '')
        } finally {
            $algorithm.Dispose()
        }
    } finally {
        $stream.Dispose()
    }
}

function Assert-Hash([string]$Path, [string]$Expected) {
    $actual = Get-Sha256 $Path
    if ($actual -ne $Expected) { throw "SHA-256 mismatch: $Path (found $actual)" }
}

function Get-PendingFiles {
    foreach ($entry in $entries) {
        $hash = Get-Sha256 $entry.Target
        if ($hash -ne $entry.Original -and $hash -ne $entry.Patched) {
            throw "Unexpected file version: $($entry.Target) (SHA-256 $hash)"
        }
        if ($hash -ne $entry.Expected) { $entry }
    }
}

if (Get-Process -Name 'HellForge.Launcher','HellForge.Session' -ErrorAction SilentlyContinue) {
    throw 'Close HellForge and stop the current session, then run this script again.'
}

$manifest = Get-Content -Raw -LiteralPath (Join-Path $PSScriptRoot 'manifest.json') | ConvertFrom-Json
$root = (Get-Item -LiteralPath $HellForgeRoot -Force).FullName
Assert-PlainPath $root
$versionFile = Join-Path $root 'app/app-build.json'
Assert-PlainPath $versionFile
$build = Get-Content -Raw -LiteralPath $versionFile | ConvertFrom-Json
if ($build.version -cne $manifest.version -or $build.commit -cne $manifest.commit) {
    throw "This patch requires HellForge $($manifest.version) ($($manifest.commit))."
}

$backupRoot = Join-Path $root ".hfzh-backup/$($build.commit)"
Assert-PlainPath $backupRoot
$paths = @(
    'app/launcher/HellForge.Launcher.dll',
    'app/launcher/HellForge.SteamDownload.dll',
    'app/profile-templates.json'
)
$entries = @(
    foreach ($path in $paths) {
        $hashes = $manifest.files.$path
        $entry = [pscustomobject]@{
            Target = Join-Path $root $path
            Payload = Join-Path (Join-Path $PSScriptRoot 'payload') $path
            Backup = Join-Path $backupRoot $path
            Original = $hashes.original
            Patched = $hashes.patched
            Expected = if ($Mode -eq 'Install') { $hashes.patched } else { $hashes.original }
        }
        Assert-PlainPath $entry.Target
        Assert-PlainPath $entry.Backup
        $entry
    }
)

$pending = @(Get-PendingFiles)
if ($pending.Count -eq 0) {
    Write-Output "Already in the requested state ($Mode)."
    return
}

[void][IO.Directory]::CreateDirectory($backupRoot)
$lockPath = Join-Path $backupRoot 'patch.lock'
Assert-PlainPath $lockPath
$lock = [IO.File]::Open($lockPath, 'OpenOrCreate', 'ReadWrite', 'None')
try {
    $pending = @(Get-PendingFiles)
    if ($pending.Count -eq 0) {
        Write-Output "Already in the requested state ($Mode)."
        return
    }
    if ($Mode -eq 'Install' -and $pending.Count -ne $entries.Count) {
        throw 'Original and patched files are mixed. Run restore.ps1 first.'
    }

    if ($Mode -eq 'Install') {
        foreach ($entry in $entries) { Assert-Hash $entry.Payload $entry.Patched }
        foreach ($entry in $entries) {
            if (-not (Test-Path -LiteralPath $entry.Backup)) {
                [void][IO.Directory]::CreateDirectory((Split-Path -Parent $entry.Backup))
                $copy = "$($entry.Backup).$([guid]::NewGuid().ToString('N')).tmp"
                try {
                    [IO.File]::Copy($entry.Target, $copy)
                    Assert-Hash $copy $entry.Original
                    [IO.File]::Move($copy, $entry.Backup)
                } finally {
                    [IO.File]::Delete($copy)
                }
            }
        }
    }
    foreach ($entry in $entries) { Assert-Hash $entry.Backup $entry.Original }

    $staged = @()
    try {
        foreach ($entry in $pending) {
            $temp = "$($entry.Target).hfzh-$([guid]::NewGuid().ToString('N'))"
            $replacement = [pscustomobject]@{
                Entry = $entry
                Next = "$temp.next"
                Previous = "$temp.previous"
                Current = if ($Mode -eq 'Install') { $entry.Original } else { $entry.Patched }
            }
            $staged += $replacement
            $source = if ($Mode -eq 'Install') { $entry.Payload } else { $entry.Backup }
            [IO.File]::Copy($source, $replacement.Next)
            Assert-Hash $replacement.Next $entry.Expected
        }
        foreach ($replacement in $staged) {
            Assert-Hash $replacement.Entry.Target $replacement.Current
            [IO.File]::Replace($replacement.Next, $replacement.Entry.Target, $replacement.Previous)
        }
        foreach ($entry in $entries) { Assert-Hash $entry.Target $entry.Expected }
    } catch {
        $failure = $_
        $rollbackFailures = @()
        foreach ($replacement in $staged) {
            if (-not [IO.File]::Exists($replacement.Previous)) { continue }
            try {
                Assert-Hash $replacement.Previous $replacement.Current
                $target = $replacement.Entry.Target
                if (-not [IO.File]::Exists($target)) {
                    [IO.File]::Move($replacement.Previous, $target)
                } elseif ((Get-Sha256 $target) -eq $replacement.Current) {
                    [IO.File]::Delete($replacement.Previous)
                } else {
                    Assert-Hash $target $replacement.Entry.Expected
                    [IO.File]::Replace($replacement.Previous, $target, [NullString]::Value)
                }
            } catch {
                $rollbackFailures += "Rollback failed. Check $($replacement.Previous). $_"
            }
        }
        if ($rollbackFailures) {
            throw (@($failure.Exception.Message) + $rollbackFailures -join [Environment]::NewLine)
        }
        throw $failure
    } finally {
        foreach ($replacement in $staged) {
            [IO.File]::Delete($replacement.Next)
        }
    }
    foreach ($replacement in $staged) { [IO.File]::Delete($replacement.Previous) }
    Write-Output "HellForge Chinese patch $Mode completed."
    Write-Output "Original files: $backupRoot"
} finally {
    $lock.Dispose()
}
