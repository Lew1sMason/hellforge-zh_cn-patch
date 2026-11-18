param([Parameter(Mandatory = $true)][string]$HellForgeRoot)

$ErrorActionPreference = 'Stop'
& (Join-Path $PSScriptRoot 'patch.ps1') -Mode Restore -HellForgeRoot $HellForgeRoot
