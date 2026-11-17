# 余留候选范围核对与 Windows 余留分类台账

本文件是独立范围核对任务的产出，不改动 `console.csv`、`console-review.md`、主表或其他模块文件，不合并总表、不改 Git、不运行程序、不联网。机器可读台账为 `modules/residual-ledger.csv`，小批译文为 `modules/residual-ui.csv`。分析中间件在 `work/residual_scratch/`（含冻结覆盖快照 `coverage_snapshot.json`）。

## 1 快照与计数口径

统计期间其他会话仍在产出模块，为保证本台账可复核，先冻结覆盖快照再计算。快照 v2 读取主表与 `modules/` 下全部非 residual 的 CSV，记录行数与 SHA256 前 12 位；此后其他会话新增的覆盖不计入本台账。

| 文件 | 行数 | SHA256 前 12 位 |
|---|---|---|
| `zh-cn-master.csv` | 446 | 1357e04c5fff |
| `modules/account-sync.csv` | 47 | 9ab30f0fb014 |
| `modules/console.csv` | 28 | fd6d92cbcb91 |
| `modules/launch-errors.csv` | 23 | ad983ef36c67 |
| `modules/profiles-mods.csv` | 155 | adbff0e90f5a |
| `modules/settings-followup.csv` | 26 | 74cd0ca32b0d |
| `modules/settings.csv` | 169 | e277c476578d |

计数规则。

| 项目 | 数量 | 说明 |
|---|---|---|
| 台账覆盖的非空 `#US` 字符串 | 1737 | 与 `inventory/scope-inventory.csv` 一致，另有 1 条空串 |
| 候选 | 1149 | 盘点条目即候选，token 唯一（1149 个） |
| 盘点已排除 | 588 | 控件名、Linux 专属、数据键、文件名等，见盘点统计 |
| 快照覆盖 token | 517 | 主表与六个模块文件按 token 取并集（主表已含部分模块行） |
| 余留未覆盖 | 636 | 1149 − 517；即 `residual-ledger.csv` 行数 |

口径变化说明。任务给出「约 736」；核对的第一次快照只有 4 个模块文件，余留 703。核对过程中出现两个新模块 `account-sync.csv`（47 行）、`settings-followup.csv`（26 行），合计新增覆盖 71 个 token（其中 67 个是先一次台账中的行）。本文件最终以快照 v2 为准：余留 636，台账已剔除这 67 条已覆盖项，不会与模块重复。后续若模块继续增长，可按同一脚本重取快照复算。

## 2 台账结构与分类定义

`residual-ledger.csv` 字段：`token,method_il,original,module,confidence,class,reason`。行覆盖全部 636 条余留候选，一行一个 token；`method_il` 取该字符串在 `work/ldstr_refs.tsv` 中的引用方法，多引用点取首选（优先 `MainWindow` 方法，XAML 取 `!XamlIlPopulate`）。

| class | 含义 | 判定依据 |
|---|---|---|
| 可见 | 用户可见界面文本，现有模块未覆盖 | XAML 内容文本且有布局/控件上下文；或方法本身是已知界面写入方法且同类文本已有已译样本；或短标签有按钮/表头/标签方法佐证 |
| 排除 | 非翻译目标 | 仅在有证据时标注：XAML 控件名（`InitializeComponent` 名称引用）、`App.axaml` 样式键/值、Linux/Proton 专属方法或自述文本、内部日志前缀（`launch-errors` 已证只进日志）、脚本参数、数据键/序列化输出、文件名/路径/字体名、颜色/数值/符号格式、品牌名保留 |
| 待查 | 证据不足 | 方法用途与显示位置均无法从静态引用确认，不做猜测 |

不把「整组排除」当默认。排除原因逐行写在 `reason`；方法级排除均附方法名，字符串级排除均附具体形态（如 `#FF6054`、` -File `、`*.zip` 等）。

## 3 分类结果

| 模块 | 余留 | 可见 | 排除 | 待查 |
|---|---|---|---|---|
| 未分类 | 423 | 177 | 238 | 8 |
| 界面静态 | 61 | 8 | 53 | 0 |
| 模组 | 60 | 35 | 25 | 0 |
| 控制台 | 26 | 19 | 7 | 0 |
| 设置 | 25 | 23 | 2 | 0 |
| 错误 | 23 | 10 | 13 | 0 |
| 状态 | 11 | 10 | 0 | 1 |
| 启动 | 4 | 0 | 4 | 0 |
| 档案 | 3 | 0 | 3 | 0 |
| 合计 | 636 | 282 | 345 | 9 |

排除类主要证据分布（按 345 条的首因归类）：非 Windows 157、XAML 控件名 31、技术标识/路径/数值 27、颜色与样式值 27、格式字面量/符号 24、脚本与命令行参数 21、数据键/序列化 18、`App.axaml` 样式键与模板部件 11、内部日志前缀 9、品牌/Logo 6、SVG 路径 3、字体名 2、文件筛选模式 2，其余 7 条为单项格式值。

可见 282 条按现有归属：未分类 177、模组 35、设置 23、控制台 19、错误 10、状态 10、界面静态 8。这些条目**尚未翻译**（仅第 6 节小批 8 条已译），不得视为完成。

## 4 64 条中高置信候选核实

余留中置信度为中/高的恰为 64 条，逐条核实结果：可见 9、排除 55。构成如下。

| 类别 | 条数 | 核实方式与结论 |
|---|---|---|
| XAML 控制名 | 31 | `SidebarState`、`Nav`、`AutoScroll`、`UninstallConfirm`、`ConfirmStop`、`SandboxUnavailable` 等；均为 `InitializeComponent` 名称引用 + 两处 `!XamlIlPopulate` 引用，属 x:Name，排除 |
| `App.axaml` 样式键/值 | 11 | `CheckBoxCheckGlyphForegroundChecked*`、`PART_ContentPresenter`、`:pointerover`、`0%`、`0 6 22 0 #55E5392B` 等，App 全局样式表，排除 |
| 品牌/Logo | 4 | `HellForge`、`HELL`、`FORGE`（Logo 两段）、`Discord`，界面保留原文，排除 |
| 非 Windows XAML | 8 | `PREFIX BACKUP`、`Back up prefix`、`PROTON VERSION` 等 Linux 前缀备份/安装器区块，以及含 passt/python3 的 UDP 说明，排除 |
| SVG 资源 | 1 | Discord 图标矢量路径，无待译文本，排除 |
| 可见标签 | 8 | `Cancel`、`Save crash report`、`Open a GitHub issue`、`End these processes`、`PLAY WITH STRANGERS`、`SESSION`、`Local HELLDIVERS 2`、`Co-op over Steam relays (UDP…)`，全部位于 `!XamlIlPopulate` 且有控件内容/布局上下文，进入第 6 节小批 |
| 可见状态 | 1 | `0x7000677D`（`ShowState@561`，沙箱游戏经 Steam 中转连接 Steam，该中转正在启动）；术语与 `console-review` 的 CON-02 草案重叠，只登记不译 |

结论：64 条无一条按猜测定稿；55 条排除均有控件名/样式键/Linux 页面/资源形态证据，9 条可见中 8 条已译、1 条因跨模块术语未定暂留。

### XAML 控件核对方法

在 `work/ldstr_refs.tsv` 中，凡字符串同时满足「`!XamlIlPopulate` 两处相邻引用」+「`InitializeComponent` 按名字引用」的，判定为 x:Name 而不是显示文本；`App.axaml` 侧则按 `HellForge.Launcher.App.!XamlIlPopulate` 中的颜色/选择器/模板部件判定样式键。仅凭文本形状或「像英文单词」不作为可见或排除依据。

## 5 明确状态/错误信息的核对

按方法筛出状态与错误写入点并逐组核对。

| 方法 | 余留中的处理 |
|---|---|
| `ShowState`、`ShowObserving`、`ShowObserved`、`ShowCrashEnding`、`ShowPreparing`、`ShowRunnerEnded`、`ShowLeftoverProcesses` | 可见；与方法内已译样本同域，属状态区/播放页提示，尚未翻译 |
| `OfferCrashReport`、`AskAboutDump`、`SaveCrashReport` | 可见；崩溃报告对话框与结果提示，尚未翻译 |
| `SyncRefusal`、`ImportRefusal`、`SyncFailed`、`SyncStartingText`、`SyncNotStarted`、`WatchSyncProgress`、`OpenGameForSync` | 可见（其中日志式前缀按第 2 节规则排除）；同步拒绝/进度提示，尚未翻译 |
| `WarnIfGameStillOpen`、`RefreshSync`、`ReportStartFailure`、`EndLeftoverProcesses` | 可见分片；属状态/错误拼接片段，尚未翻译 |
| `ProxyClosedLine`、`Start`（`Profile: `/`Launch options: ` 一类）、`SaveLogsToDesktop`（文件名/时间格式）、`AppendRequest` | 排除；内部日志或请求行格式，`launch-errors` 与 `console` 模块已有同类先例 |
| `TakeCapture`、`Refresh`（`Launcher status error: `） | 待查；见第 7 节 |

## 6 小批译文（8 条）

`modules/residual-ui.csv`，字段与模块表一致，状态全部为已译，`decision_id` 为 `—`。选入条件：位于 XAML、界面可见、术语已有主表或模块先例、不属于快照已覆盖 token（与六个模块文件及主表均无重叠）。

| token | 原文 | 译文 | 依据 |
|---|---|---|---|
| 0x70008A3B | Cancel | 取消 | 主表 `CANCEL`→取消 |
| 0x70011819 | Save crash report | 保存崩溃报告 | 试译基线 crash report→崩溃报告 |
| 0x7001183D | Open a GitHub issue | 打开 GitHub 问题 | 既有「打开……」动词风格；GitHub 保留 |
| 0x700118AF | End these processes | 结束这些进程 | 主表「无法结束残留的会话进程」 |
| 0x700118E7 | PLAY WITH STRANGERS | 与陌生人同玩 | 主表「与陌生人同玩」 |
| 0x700116E9 | SESSION | 会话 | 主表 session→会话 |
| 0x70010CC2 | Local HELLDIVERS 2 | 本地 HELLDIVERS 2 | 主表 Local backend/本地会话；HELLDIVERS 2 保留英文 |
| 0x700135DA | Co-op over Steam relays (UDP to Valve's relays only) | Steam 中继联机（仅以 UDP 连接 Valve 的中继服务器） | 主表「Steam 中继联机」 |

小批机器核对：8 行 token 唯一；均不在快照覆盖集合内；原文与盘点逐字一致；`method_il` 均在 `ldstr_refs.tsv` 命中对应 XAML IL；无首尾空格；7 列；UTF-8 无 BOM、LF；0 问题。

## 7 待查 9 条与下一步

| token | 方法 | 原文 | 未定原因 |
|---|---|---|---|
| 0x70001F5C、0x70001F84、0x70001FAC、0x70001FDC、0x70001FFC、0x70002030、0x700020AC、0x700020F6 | `MainWindow.TakeCapture@…` | `capture not taken: `、` items, progression `、`Inventory sync complete for profile ` 等 | 同步采集的诊断文本；无法从静态引用区分是状态卡还是日志。下一步：取实机同步状态区与控制台截图，或由共享状态模块确认是否归其范围。 |
| 0x70005CDF | `MainWindow.Refresh@10` | `Launcher status error: ` | 状态刷新错误前缀，可能只进日志。下一步同上。 |

## 8 来源与机器核对

| 检查项 | 结果 |
|---|---|
| 余留集合 | 通过：台账 636 token 与「盘点 1149 − 快照覆盖 517」完全相等，无缺行、无多余 |
| 原文一致 | 通过：636 行与 `scope-inventory.csv` 原文逐字一致 |
| 方法定位 | 通过：636 行 `method_il` 均能在 `work/ldstr_refs.tsv` 命中同 us 同方法同 IL |
| 分类取值 | 通过：仅 可见/排除/待查 三种，`reason` 无空值 |
| 64 条中高置信 | 通过：全部出现在台账，9 可见 + 55 排除，无待查 |
| 排除证据 | 通过：排除行均带方法名或具体形态证据；无无法解释的整组排除 |
| 小批文件 | 通过：8 行，见第 6 节；与快照已覆盖 token 无重叠 |
| 盘点统计 | 通过：`scope-inventory.csv` 1149 行、1149 个唯一 token；盘点排除 588；`#US` 记录 1738（1 条空串）与 `inventory-summary.md` 一致 |
| 未完成边界 | 明确：282 条可见只完成分类，除小批 8 条外未翻译；9 条待查未定性 |

## 9 余留工作与口径

1. 282 条可见按归属分发：未分类 177 需先按方法落到具体界面（状态/控制台/配置/播放页），再交对应模块；模组 35 交模组模块；设置 23 交设置/安装；控制台 19 交控制台；错误 10、状态 10 交启动/共享状态；界面静态 8 已在小批处理。
2. 9 条待查需要运行截图或模块负责人裁定，不建议静态猜译。
3. 本台账只做分类，不合并主表；后续其他会话新增覆盖后，可重取快照复算余留。
4. 未验证：所有可见性判断止于方法与 IL 层级，未实机核对；分类为静态证据结论，不宣称界面文本已全量覆盖。
