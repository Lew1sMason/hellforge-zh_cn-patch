$ErrorActionPreference = 'Stop'
$workspace = Split-Path -Parent $PSScriptRoot
$preview = Join-Path $workspace 'preview-0.4.0-beta-zhcn'
$exe = Join-Path $preview 'app\launcher\HellForge.Launcher.exe'

Add-Type -AssemblyName System.Drawing.Common
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class PreviewWindow
{
    [StructLayout(LayoutKind.Sequential)] public struct Rect { public int Left, Top, Right, Bottom; }
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hwnd, out Rect rect);
    [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr hwnd, IntPtr dc, uint flags);
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hwnd);
}
'@

$process = Start-Process -FilePath $exe -WorkingDirectory $preview -PassThru `
    -RedirectStandardError (Join-Path $preview 'launcher-stderr.txt') `
    -RedirectStandardOutput (Join-Path $preview 'launcher-stdout.txt')
try {
    for ($i = 0; $i -lt 50; $i++) {
        $process.Refresh()
        if ($process.HasExited) { throw "Preview exited with code $($process.ExitCode)" }
        if ($process.MainWindowHandle -ne 0 -and [PreviewWindow]::IsWindowVisible($process.MainWindowHandle)) { break }
        Start-Sleep -Milliseconds 250
    }
    Start-Sleep -Milliseconds 1200
    $process.Refresh()
    if ($process.HasExited -or $process.MainWindowHandle -eq 0) { throw 'Preview window did not remain open' }
    $bounds = [PreviewWindow+Rect]::new()
    if (-not [PreviewWindow]::GetWindowRect($process.MainWindowHandle, [ref]$bounds)) { throw 'Cannot determine window bounds' }
    $width = $bounds.Right - $bounds.Left
    $height = $bounds.Bottom - $bounds.Top

    $bitmap = [Drawing.Bitmap]::new($width, $height)
    try {
        $graphics = [Drawing.Graphics]::FromImage($bitmap)
        try {
            $dc = $graphics.GetHdc()
            try { $captured = [PreviewWindow]::PrintWindow($process.MainWindowHandle, $dc, 2) }
            finally { $graphics.ReleaseHdc($dc) }
        } finally { $graphics.Dispose() }
        if (-not $captured) { throw 'Window capture failed' }
        $out = Join-Path $preview 'launcher-smoke.png'
        $bitmap.Save($out, [Drawing.Imaging.ImageFormat]::Png)
    } finally { $bitmap.Dispose() }

    [pscustomobject]@{ Title = $process.MainWindowTitle; Screenshot = $out; Width = $width; Height = $height }
    if ($width -lt 700 -or $height -lt 450) { throw 'Expected the main launcher window, received a small dialog' }
} finally {
    $process.Refresh()
    if (-not $process.HasExited) {
        [void]$process.CloseMainWindow()
        [void]$process.WaitForExit(3000)
    }
}
