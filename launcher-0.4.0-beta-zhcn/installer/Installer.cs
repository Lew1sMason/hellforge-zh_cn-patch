using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Security.Cryptography;
using System.Web.Script.Serialization;
using System.Windows.Forms;

internal sealed class InstallerForm : Form
{
    private readonly TextBox folder = new TextBox();
    private readonly Button browse = new Button();
    private readonly Button install = new Button();
    private readonly Button restore = new Button();
    private readonly Label status = new Label();

    [STAThread]
    private static void Main()
    {
        Application.EnableVisualStyles();
        Application.SetCompatibleTextRenderingDefault(false);
        Application.Run(new InstallerForm());
    }

    private InstallerForm()
    {
        Text = "HellForge 简中补丁";
        ClientSize = new Size(570, 180);
        AutoScaleMode = AutoScaleMode.Dpi;
        FormBorderStyle = FormBorderStyle.FixedDialog;
        MaximizeBox = false;
        StartPosition = FormStartPosition.CenterScreen;
        Font = new Font("Microsoft YaHei UI", 10);

        var title = new Label { Text = "HellForge 安装目录", AutoSize = true, Location = new Point(20, 16) };
        folder.SetBounds(20, 45, 420, 30);
        folder.ReadOnly = true;
        folder.AccessibleName = title.Text;
        browse.SetBounds(450, 42, 100, 32);
        browse.Text = "选择文件夹";
        install.SetBounds(20, 89, 123, 35);
        install.Text = "安装汉化";
        restore.SetBounds(153, 89, 123, 35);
        restore.Text = "卸载汉化";
        status.SetBounds(20, 140, 530, 30);
        status.Text = "适用于 HellForge 0.4.0-beta（d8a8b46）。请先关闭 HellForge。";
        Controls.AddRange(new Control[] { title, folder, browse, install, restore, status });

        browse.Click += ChooseFolder;
        install.Click += delegate { ApplyPatch(true); };
        restore.Click += delegate { ApplyPatch(false); };
        SetActionsEnabled(false);
        for (var dir = new DirectoryInfo(AppDomain.CurrentDomain.BaseDirectory); dir != null; dir = dir.Parent)
        {
            if (!Patch.HasBuildFile(dir.FullName)) continue;
            folder.Text = dir.FullName;
            SetActionsEnabled(true);
            break;
        }
    }

    private void ChooseFolder(object sender, EventArgs args)
    {
        using (var dialog = new FolderBrowserDialog())
        {
            dialog.Description = "请选择 HellForge 安装目录（包含 app 文件夹）";
            dialog.ShowNewFolderButton = false;
            dialog.SelectedPath = folder.Text;
            if (dialog.ShowDialog(this) != DialogResult.OK) return;
            if (!Patch.HasBuildFile(dialog.SelectedPath))
            {
                status.Text = "所选目录未找到 HellForge，请选择包含 app 文件夹的安装目录。";
                return;
            }
            folder.Text = dialog.SelectedPath;
            status.Text = "请选择安装或卸载汉化。";
            SetActionsEnabled(true);
        }
    }

    private void SetActionsEnabled(bool enabled)
    {
        install.Enabled = enabled;
        restore.Enabled = enabled;
    }

    private void ApplyPatch(bool installPatch)
    {
        SetActionsEnabled(false);
        browse.Enabled = false;
        UseWaitCursor = true;
        status.Text = installPatch ? "正在校验并安装汉化…" : "正在校验并恢复原文件…";
        status.Refresh();
        try
        {
            Patch.Apply(folder.Text, installPatch);
            status.Text = installPatch ? "汉化已安装，可以打开 HellForge。" : "汉化已卸载，原文件已恢复。";
        }
        catch (Exception error)
        {
            status.Text = "操作未完成，请查看提示。";
            MessageBox.Show(this, error.Message, "操作未完成", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
        finally
        {
            UseWaitCursor = false;
            browse.Enabled = true;
            SetActionsEnabled(true);
        }
    }
}

internal static class Patch
{
    private static readonly string[] Targets =
    {
        "app/launcher/HellForge.Launcher.dll",
        "app/launcher/HellForge.SteamDownload.dll",
        "app/profile-templates.json"
    };

    public sealed class Manifest
    {
        public string version { get; set; }
        public string commit { get; set; }
        public Dictionary<string, Hashes> files { get; set; }
    }

    public sealed class Hashes
    {
        public string original { get; set; }
        public string patched { get; set; }
    }

    private sealed class Entry
    {
        public string RelativePath;
        public string Target;
        public string Backup;
        public Hashes Hashes;
        public string ExpectedHash;
        public string CurrentHash;
        public string Next;
        public string Previous;
    }

    internal static bool HasBuildFile(string root)
    {
        return File.Exists(Path.Combine(root, "app", "app-build.json"));
    }

    internal static void Apply(string root, bool install)
    {
        root = Path.GetFullPath(root);
        var buildPath = Path.Combine(root, "app", "app-build.json");
        AssertPlainPath(buildPath);
        var json = new JavaScriptSerializer();
        Manifest manifest;
        using (var stream = OpenResource("manifest.json"))
        using (var reader = new StreamReader(stream))
            manifest = json.Deserialize<Manifest>(reader.ReadToEnd());

        var build = json.Deserialize<Manifest>(File.ReadAllText(buildPath));
        if (build.version != manifest.version || build.commit != manifest.commit)
            throw new InvalidOperationException("此补丁要求 HellForge " + manifest.version + "（" + manifest.commit + "）。");

        if (IsRunning("HellForge.Launcher") || IsRunning("HellForge.Session"))
            throw new InvalidOperationException("请关闭 HellForge 并结束当前会话，再试一次。");

        var backupRoot = Path.Combine(root, ".hfzh-backup", manifest.commit);
        var entries = Targets.Select(relative =>
        {
            var hashes = manifest.files[relative];
            return new Entry
            {
                RelativePath = relative, Hashes = hashes,
                Target = Path.Combine(root, relative), Backup = Path.Combine(backupRoot, relative),
                ExpectedHash = install ? hashes.patched : hashes.original
            };
        }).ToArray();
        foreach (var entry in entries)
        {
            AssertPlainPath(entry.Target);
            AssertPlainPath(entry.Backup);
        }
        if (Pending(entries).Length == 0) return;

        var lockPath = Path.Combine(backupRoot, "patch.lock");
        AssertPlainPath(lockPath);
        Directory.CreateDirectory(backupRoot);
        using (File.Open(lockPath, FileMode.OpenOrCreate, FileAccess.ReadWrite, FileShare.None))
        {
            var pending = Pending(entries);
            if (pending.Length == 0) return;
            if (install && pending.Length != entries.Length)
                throw new InvalidOperationException("目录里同时存在原版和汉化文件。请先点击「卸载汉化」，再重新安装。");
            ApplyFiles(entries, pending, install);
        }
    }

    private static Entry[] Pending(Entry[] entries)
    {
        foreach (var entry in entries)
        {
            entry.CurrentHash = Hash(entry.Target);
            if (entry.CurrentHash != entry.Hashes.original && entry.CurrentHash != entry.Hashes.patched)
                throw new IOException("文件版本与补丁不匹配，校验未通过。\r\n" + entry.Target);
        }
        return entries.Where(entry => entry.ExpectedHash != entry.CurrentHash).ToArray();
    }

    private static void ApplyFiles(Entry[] entries, Entry[] pending, bool install)
    {
        try
        {
            foreach (var entry in pending)
            {
                var temp = entry.Target + ".hfzh-" + Guid.NewGuid().ToString("N");
                entry.Next = temp + ".next";
                entry.Previous = temp + ".previous";
                if (install)
                {
                    using (var input = OpenResource(entry.RelativePath))
                    using (var output = File.Open(entry.Next, FileMode.CreateNew))
                        input.CopyTo(output);
                }
                else
                    File.Copy(entry.Backup, entry.Next);
                AssertHash(entry.Next, entry.ExpectedHash);
            }
            foreach (var entry in entries)
            {
                if (install) SaveBackup(entry);
                AssertHash(entry.Backup, entry.Hashes.original);
            }
            foreach (var entry in pending)
            {
                AssertHash(entry.Target, entry.CurrentHash);
                File.Replace(entry.Next, entry.Target, entry.Previous);
            }
            foreach (var entry in entries) AssertHash(entry.Target, entry.ExpectedHash);
        }
        catch (Exception error)
        {
            var rollbackErrors = new List<string>();
            foreach (var entry in pending.Reverse())
            {
                if (!File.Exists(entry.Previous)) continue;
                try
                {
                    AssertHash(entry.Previous, entry.CurrentHash);
                    if (!File.Exists(entry.Target))
                        File.Move(entry.Previous, entry.Target);
                    else if (Hash(entry.Target) == entry.CurrentHash)
                        File.Delete(entry.Previous);
                    else
                    {
                        AssertHash(entry.Target, entry.ExpectedHash);
                        File.Replace(entry.Previous, entry.Target, null);
                    }
                }
                catch (Exception rollback)
                {
                    rollbackErrors.Add(entry.Previous + "\r\n" + rollback.Message);
                }
            }
            if (rollbackErrors.Count > 0)
                throw new IOException(error.Message + "\r\n部分文件未能自动恢复，临时备份位于：\r\n"
                    + string.Join("\r\n", rollbackErrors), error);
            throw;
        }
        finally
        {
            foreach (var entry in pending)
                if (File.Exists(entry.Next)) File.Delete(entry.Next);
        }
        foreach (var entry in pending) File.Delete(entry.Previous);
    }

    private static void SaveBackup(Entry entry)
    {
        if (File.Exists(entry.Backup)) return;
        Directory.CreateDirectory(Path.GetDirectoryName(entry.Backup));
        var temp = entry.Backup + "." + Guid.NewGuid().ToString("N") + ".tmp";
        try
        {
            File.Copy(entry.Target, temp);
            AssertHash(temp, entry.Hashes.original);
            File.Move(temp, entry.Backup);
        }
        finally
        {
            File.Delete(temp);
        }
    }

    private static bool IsRunning(string name)
    {
        var processes = Process.GetProcessesByName(name);
        foreach (var process in processes) process.Dispose();
        return processes.Length > 0;
    }

    private static void AssertPlainPath(string path)
    {
        for (var current = Path.GetFullPath(path); current != null; current = Path.GetDirectoryName(current))
        {
            if ((File.Exists(current) || Directory.Exists(current)) &&
                (File.GetAttributes(current) & FileAttributes.ReparsePoint) != 0)
                throw new IOException("请选择实际安装目录，补丁无法使用链接目录或链接文件。\r\n" + current);
        }
    }

    private static Stream OpenResource(string name)
    {
        var stream = Assembly.GetExecutingAssembly().GetManifestResourceStream(name);
        if (stream == null) throw new IOException("补丁文件缺失：" + name);
        return stream;
    }

    private static string Hash(string path)
    {
        using (var input = File.OpenRead(path))
        using (var algorithm = SHA256.Create())
            return BitConverter.ToString(algorithm.ComputeHash(input)).Replace("-", "").ToLowerInvariant();
    }

    private static void AssertHash(string path, string expected)
    {
        if (Hash(path) != expected) throw new IOException("文件校验未通过。\r\n" + path);
    }
}
