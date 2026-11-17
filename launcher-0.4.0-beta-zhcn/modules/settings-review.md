# 设置页、安装与引导 批次复核（settings）

覆盖 HellForge 0.4.0-beta Windows 启动器的设置页、安装引导页与安装流程核心提示文案。档案/模组/控制台/导航与启动页状态区由其他会话负责，本文件不处理也不合并其产出。机器可读结果在同目录 `settings.csv`。本轮只依据 `work/ldstr_refs.tsv`、`work/us_all.tsv`、`work/inventory-full.tsv`、`launcher-0.4.0-beta-zhcn/inventory/scope-inventory.csv` 与主表现有记录，未重新解析程序集。

## 1 筛选口径

设置页 XAML 位于 `MainWindow.!XamlIlPopulate` 的 IL 20526–31035（`SettingsPage` 起，`PlatformText` 止），安装引导页位于 IL 31036–37539（`SetupPage` 起，`Stop and close` 止），与任务给定的「SettingsPage 的 IL 20526 到 SetupPage」一致。两段内共 208 个唯一字符串（设置页 132、安装页 76），按控件类型（文本块/按钮/复选框/说明段）取用户可见项。

另核对安装流程的方法级文案：`InitializeSetup`、`EnterSetup`、`StartSteamCmd`、`CreateShortcuts`、`Describe`、`OfferDownload`、`ShowDownload`、`SteamHas`，以及安装流水线状态机 `<FindGameStep>`、`<CopyStep>`、`<CheckDownload>`、`<NetworkBlockStep>`、`<OwnershipStep>`、`<SteamDownloadStep>`、`<DownloadWithSteamCmd>`、`<DownloadWithQr>`、`<ImportStep>`、`<ShortcutsStep>`、`<RunSetup>`、`<Uninstall>`，和设置页动态文案 `UpdateSettingsImport`、`<InitializeSettingsImport>`、`ApplyStrangersSetting`、`ShowStrangersDefaultNotice`、`<InitializeLiveChanges>`、`<InitializeStrangers>`、`<SettingSwitch>`。

判据是「写入显示控件」：XAML 的 `Text`/`Content`/`Watermark` 位、状态栏与提示标签的赋值点。控制名（`x:Name`）、样式键（`card`、`h1`、`muted`、`eyebrow` 等）、数据键（`war` 单选组名）、路径、命令行、正则、脚本和 PowerShell 参数一律不译。

## 2 条目统计

169 条，已译 164，待裁定 4，保留 1。分六批追加写入同一 CSV（A 设置页 XAML 53 → B 设置页动态 12 + 安装页 XAML 18 → C 安装流程 37 → D 导入与 SteamCMD 补充 16 → E 下载/复制/所有权补充 22 → F 从 Steam 获取版本卡 11），最终一次性校验后写盘。

| 区域 | 条数 | 说明 |
|---|---|---|
| 设置页（XAML 静态） | 53 | 页眉与一级标题、安装卡、多人游戏、沙箱、实验性、银河战争、启动选项、疑难解答、路径、关于 |
| 设置页（动态/状态） | 12 | 游戏设置导入成功/失败、开关保存失败、默认值提示 |
| 安装引导页（XAML 静态） | 18 | 引言、商标声明、SteamCMD 登录、选项卡、确认浮层 |
| 安装流程文案 | 84 | 查找游戏、复制/下载、网络阻断、所有权检查、SteamCMD、二维码登录、导入复核、配置暂停/重试、卸载前置 |
| 运行库安装提示 | 2 | `InstallRuntimesThenStart`，随安装流程出现，归本模块 |

| status | 条数 |
|---|---|
| 已译 | 164 |
| 待裁定 | 4（SET-01 ×1、SET-02 ×1、SET-03 ×2） |
| 保留 | 1（`SteamCMD` 区段标签，Valve 工具名） |

## 3 覆盖统计

两个 XAML 区间的 Windows 用户可见字符串已全部覆盖，无遗漏项。

| 区间 | 唯一字符串 | 本模块 | 主表已覆盖 | 纯 Linux | 控件名/样式键/数据键 |
|---|---|---|---|---|---|
| 设置页 IL 20526–31035 | 132 | 53 | 2（HF-52145 检查并修复、HF-75945 打开会话日志） | 11 | 66 |
| 安装页 IL 31036–37539 | 76 | 19（含 `INSTALLATION` 与设置页共用 1） | 3（HF-52101 返回、HF-52111 配置 HellForge、HF-52179 开始配置） | 1（`PROTON VERSION`） | 53 |

安装流程共 86 条新增（84 条流程文案 + 2 条运行库提示），覆盖 Windows 路径下的查找游戏、复制校验、网络阻断权限、Steam 所有权、SteamCMD/二维码两种下载、导入复核、暂停/继续/重试与卸载前置检查。Steam 下载说明链（`OfferDownload`/`ShowDownload`/`SteamHas`）的 15 条拼接片段已全部译出，含首尾空格。

主表与相邻模块无重复 token：169 行与 `zh-cn-master.csv` 无交集，与 `modules/launch-errors.csv` 无交集。主表已有的 HF-75945「打开会话日志」本模块复核译法一致，未重复列出。

## 4 待裁定（SET-01 起）

待裁定行译文留空，`decision_id` 指向本节编号；关联条目的草稿译法已写入并在 `context` 标注。

### SET-01 Play with strangers

| 字段 | 内容 |
|---|---|
| 类型 | 术语/语义 |
| 关联 | HF-80017（按钮，us=80017，token 0x70013891，`!XamlIlPopulate@25555`，偏移 496681）；HF-34564、HF-80081、HF-68200、HF-35089 使用同一概念 |
| 候选 | A 与陌生人同玩；B 与非好友玩家同玩；C 允许非好友加入 |
| 差别 | A 直译、短（6 字），与警告句「陌生人的游戏」自然衔接；B 准确对应「非好友」的实现语义（公开大厅只对非好友开放），但按钮 8 字，且与「仅限好友」形成对照；C 改变句义，原文强调一起玩而不是允许加入 |
| 建议 | A。按钮与警告、默认值提示、保存失败提示共 4 处需一致（其中 3 条已按草稿「陌生人」译出）；若委托方要求突出「非好友」，改 B 时这 3 条同步替换 |

### SET-02 sandbox / sandboxed

| 字段 | 内容 |
|---|---|
| 类型 | 术语 |
| 关联 | HF-80456（复选框，us=80456，token 0x70013A48，偏移 497120）；HF-80440（SANDBOX 分区标题）、HF-80502（说明段，含「沙箱」2 处）、HF-81891（Steam 桥接缺失提示） |
| 候选 | A 沙箱；B 沙盒 |
| 差别 | A 是安全工程与 Linux 语境常用词，与「低完整性级别」「只读文件系统」等技术表述一致；B 是 Windows 自带功能（Windows 沙盒）的官方写法，玩家更熟，但与系统功能同名，可能被理解成同一机制。两者语义相同，差别主要是官方用词与联想 |
| 建议 | A（沙箱）。若委托方决定跟随 Windows 官方术语改 B，本模块需同步 4 条：待定的 `Run the game sandboxed`、`SANDBOX` 分区标题、`SandboxBox` 说明段、`SandboxUnavailable` 提示 |

### SET-03 deal subfactions / deal SEAF allies

| 字段 | 内容 |
|---|---|
| 类型 | 用词/语义 |
| 关联 | HF-85245（复选框，us=85245，token 0x70014CFD，偏移 501909）、HF-85732（复选框，us=85732，token 0x70014EE4，偏移 502396） |
| 候选 | A 部署；B 分配；C 分布 |
| 差别 | A 暗示主动部署，偏军事动作；B 强调按种子随机分派，与紧邻说明「根据种子，每颗行星会获得……」一致；C 只描述空间分布，不体现分配动作 |
| 建议 | B（在各行星分配子阵营 / 在各行星分配 SEAF 友军）。两条必须同改；说明段的「获得」措辞已按 B 写好 |

## 5 排除边界

| 类别 | 条数 | us 索引或范围 |
|---|---|---|
| 设置页纯 Linux（Proton 前缀备份、sudo 命令、UDP 中继、Linux 沙箱说明） | 11 | 56111、77144、77172、77753、77781、77811、77847、77875、79322、79428、82062 |
| 安装页纯 Linux（Proton 版本卡） | 1 | 90301 |
| 其他纯 Linux 方法 | 约 60 | `LinuxInstallerWindow.*`、`<InitializePrefix>`、`<InstallAndLaunch>`、`<UninstallLinux>`、`<DiscoverProtons>`、`ProtonPicker`、`LinuxSetupSource`、`<CheckLinuxOwnership>`、`<CheckLinuxNetworkBlock>`、`<CheckLinuxSetupFiles>` 等 |
| 控件名/样式键/数据键 | 119 | 设置页 66（`SettingsPage`、`InstallCard`、`card`、`h1`、`muted`、`eyebrow`、`DangerBrush`、`war` 等）+ 安装页 53（`SetupPage`、`SetupSteps`、`CopyProgress`、`ConfirmOverlay` 等） |
| 主表已覆盖 | 5 | 52145、75945、52101、52111、52179 |
| 共享按钮 | 2 | 35387 `Cancel`（跨对话框 9+ 调用点，按共享模块统一）；55551 `Copy`（复制命令按钮） |
| 文件名/路径/脚本/命令 | — | `user_settings.config`（51927）、`Test-SteamOwnership.ps1`、`hellforge-uninstall-*.ps1`、`Steam's hashes` 中的脚本参数、`api.helldivers2.dev` 等域名按句内保留 |
| 内部日志/后端参数 | — | `proxy.log`、`ownership`、`import`、`profile`、`import-preview`、`setup-ownership.json`、`steamprobe` |
| 其他模块范围 | — | 模组信任对话框（49051–51175）、模组页保存失败（48631、94558、94622）、档案页（96153、125388）、崩溃报告（115232）、启动页状态（33611、34390、34464 与 `ShowState` 的 25860、26177） |

启动错误模块放弃的 18 条安装类字符串中，97511、106596、51795、51899、59826、60167、60229、57233、57399、92631、104229 已由本批覆盖；其余为 Linux（105447、106738、118922、122956、124592、124744）或文件名（51927）。

## 6 术语、格式与运行期接缝

术语沿用主表与锁定样本：档案、开始游戏、模组、同步、会话、会话启动程序、启动选项、检查并修复；网络阻断沿用 PD-005 暂定写法并与 `About` 段落统一；`Local PlayFab` 保留英文功能名（与启动错误模块一致）。分区名定为：安装、多人游戏、沙箱（SET-02）、实验性、银河战争、启动选项、疑难解答、路径、关于；其中「多人游戏」「安装」「沙箱」与启动错误模块引用「设置 > 多人游戏」「设置 > 安装」「设置 > Sandbox」一致。

保留英文：`HELLDIVERS 2`、`Steam`、`SteamCMD`、`PlayFab`、`PlayFab Party`、`Lobby`、`Valve`、`Arrowhead Game Studios`、`Sony Interactive Entertainment`、`Steam Family Sharing`、`Steam Guard`、`Steam Deck`、`Steam broker`、`Windows Script Host`、`Microsoft`、`Xbox`、`DirectX 11`、`Super Earth`、`Illuminate`、`SEAF`、`Cyberstan`、`Predator Strain`、`Jet Brigade`、`api.helldivers2.dev`、`playfabapi.com`、`--use-d3d11`、`--log-to-file`、`%command%`、`1 GB`、`24 GB`。`Steam broker` 与 `Steam bridge` 区分处理：前者保留英文（设置页沙箱说明），后者译「Steam 桥接」（构建缺失提示）。

格式：省略号统一六点（……）；句内冒号用全角「：」；拼接前缀后接运行期值或详情时保留 ASCII 冒号「: 」与尾空格（如「无法检查下载: 」「所有权检查未通过: 」）；首尾空格按原文逐条保留（45 条含首或尾空格的片段已逐字核对，其中首空格 16 条、尾空格 32 条、两端都有 3 条，含「 未找到: 」「 GB）」「 请确认 Steam 正在运行并已登录，然后重新开始配置。」）；编号、括号与占位符沿用原文，`item(s)` 译「项」。括号在拼接跨字符串时统一为全角（HF-51795 左括号 + HF-51899 右括号、HF-102536 + HF-102554）。

运行期接缝示例（仅演示，未写入主表）：
- 游戏设置导入：`已导入到 ` + 档案名 + `。下一次会话将使用它们。`
- 设置开关保存失败：`无法保存 ` + 开关名 + `: ` + 异常
- Steam 下载说明：`Steam 上 ` + `有 HELLDIVERS 2 版本 ` + 版本 + `，但此版本的 HellForge 需要版本 ` + 版本 + `。Steam 可以下载同一版本 ` + `供你的账户使用：请按下方步骤操作。`
- 卸载权限被拒：`Windows 未授予权限` + `: 未移除任何内容。`

## 7 剩余范围统计

已完成后，本模块内仍可细分如下（不计入本轮 169 条，均非 XAML 静态可见文案）：

| 剩余项 | 条数 | 举例 |
|---|---|---|
| 安装流程 Windows 进度/版本拼接片段 | 18 | us=103132、103170、103200、103270、103280、104135、104187、104229、104769、104910、106516、106530、106540、106720、107309、107327、107373、109461（多为「版本 X」「N GB」中间值，单独翻译价值低，建议并入整句时统一处理） |
| 共享确认对话框代码文案 | 6 | `Stopping session`、`Closing the game and the local backend...`、`Session stopped`、`The session did not stop in time...`、`Session did not stop`、` Closing anyway.`，属启动页/共享状态 |
| 纯 Linux 安装流程 | 5 | 106738、105968、106295、114416、117187 |
| 分隔符、格式符、路径、脚本参数 | 30 | us=165、1127、7356、8150、9913、10153、30121、30399、37910、45603、57181、110184–118262 的 PowerShell 片段 |
| 后端参数键 | 3 | `profile`、`Importing`、`import`（写入后端请求，不进界面） |
| 设置页导入提示的三段拼接 | 3 | 67365、67604、67634，中间夹运行期用户名/Steam 路径，拆句方式未定，留给实机确认 |
| 其他模块范围 | — | 见第 5 节末行 |

## 8 验证与边界

本批只写入 `modules/settings.csv` 与本文件，未改主表、锁定样本、试译基线、其他模块文件与输入 DLL。未运行程序，未联网，未访问真实安装目录或 Git。

逐行验证项（脚本在临时目录执行，交付前已删除）：原文取自 `work/us_all.tsv` 的 `#US` 堆，逐字回填，不做手工转写；每行的 `method_il@偏移` 必须能在 `work/ldstr_refs.tsv` 找到同一 us 的调用点，且该调用点的文本与堆内文本一致；`token` 由 us 索引推导并核对（`0x70000000 | us`）；`context` 中声明的 `us=`、`偏移` 与记录比对一致；169 行 token 唯一；待裁定行译文为空且 `decision_id` 存在；已译/保留行译文非空；原文首尾空格与译文逐条比对（原文以空格结尾而译文未保留者判错）；CSV 回读逐字一致，UTF-8 带 BOM，七列固定为 token、method_il、original、translation、status、context、decision_id。

未验证项：界面实际显示、换行与控件宽度、字体回退；拼接后的完整句子按 IL 先后推断，未在运行环境核对；Windows 与 Linux 共用字符串（98824、98894、97041、53466、53488、60345、48483、76240、90273、104321、108907、34564 等）只按 Windows 语境定稿，Linux 界面同 token 会显示同一译文；`Session running` 等 4 条确认浮层文案与 `ConfirmCloseAsync` 的代码文案同 token，合并时需去重。
