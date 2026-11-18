$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[Windows.Forms.Application]::EnableVisualStyles()

$form = [Windows.Forms.Form]::new()
$form.Text = 'HellForge 简中补丁'
$form.ClientSize = [Drawing.Size]::new(550, 193)
$form.AutoScaleMode = 'Dpi'
$form.FormBorderStyle = 'FixedDialog'
$form.MaximizeBox = $false
$form.StartPosition = 'CenterScreen'
$form.Font = [Drawing.Font]::new('Microsoft YaHei UI', 10)

$title = [Windows.Forms.Label]::new()
$title.Text = '选择 HellForge 安装目录'
$title.Location = [Drawing.Point]::new(20, 15)
$title.AutoSize = $true

$folder = [Windows.Forms.TextBox]::new()
$folder.Location = [Drawing.Point]::new(20, 47)
$folder.Width = 400
$folder.ReadOnly = $true
$folder.AccessibleName = 'HellForge 安装目录'

$browse = [Windows.Forms.Button]::new()
$browse.Text = '选择文件夹'
$browse.SetBounds(430, 44, 100, 32)

$install = [Windows.Forms.Button]::new()
$install.Text = '安装汉化'
$install.SetBounds(20, 95, 124, 36)
$install.Enabled = $false

$restore = [Windows.Forms.Button]::new()
$restore.Text = '卸载汉化'
$restore.SetBounds(154, 95, 124, 36)
$restore.Enabled = $false

$status = [Windows.Forms.Label]::new()
$status.Text = '适用于 HellForge 0.4.0-beta（d8a8b46）。请先关闭 HellForge。'
$status.SetBounds(20, 147, 510, 34)
$status.AccessibleName = '操作状态'
$form.Controls.AddRange(@($title, $folder, $browse, $install, $restore, $status))

function Set-InstallFolder([string]$Path) {
    if (-not (Test-Path -LiteralPath (Join-Path $Path 'app/app-build.json') -PathType Leaf)) {
        return $false
    }
    $folder.Text = $Path
    $install.Enabled = $true
    $restore.Enabled = $true
    return $true
}

$browse.Add_Click({
    $picker = [Windows.Forms.FolderBrowserDialog]::new()
    try {
        $picker.Description = '请选择 HellForge 安装目录（包含 app 文件夹）'
        $picker.ShowNewFolderButton = $false
        $picker.SelectedPath = $folder.Text
        if ($picker.ShowDialog($form) -eq 'OK' -and -not (Set-InstallFolder $picker.SelectedPath)) {
            $status.Text = '所选目录没有找到 HellForge。请选择包含 app 文件夹的安装目录。'
        }
    } finally {
        $picker.Dispose()
    }
})

function Invoke-Patch([string]$Mode, [string]$ProgressText, [string]$SuccessText) {
    $install.Enabled = $false
    $restore.Enabled = $false
    $browse.Enabled = $false
    $form.UseWaitCursor = $true
    $status.Text = $ProgressText
    $status.Refresh()
    try {
        & (Join-Path $PSScriptRoot 'patch.ps1') -Mode $Mode -HellForgeRoot $folder.Text | Out-Null
        $status.Text = $SuccessText
    } catch {
        $status.Text = '操作未完成，请查看提示。'
        [void][Windows.Forms.MessageBox]::Show(
            $form, $_.Exception.Message, '操作未完成', 'OK', 'Error'
        )
    } finally {
        $form.UseWaitCursor = $false
        $browse.Enabled = $true
        $install.Enabled = $true
        $restore.Enabled = $true
    }
}

$install.Add_Click({ Invoke-Patch 'Install' '正在校验并安装汉化…' '汉化已安装，可以打开 HellForge。' })
$restore.Add_Click({ Invoke-Patch 'Restore' '正在校验并恢复原文件…' '汉化已卸载，原文件已恢复。' })

# Preselect an installation when the package was extracted into its directory.
for ($directory = [IO.DirectoryInfo]::new($PSScriptRoot); $directory; $directory = $directory.Parent) {
    if (Set-InstallFolder $directory.FullName) { break }
}
[void]$form.ShowDialog()
$form.Dispose()
