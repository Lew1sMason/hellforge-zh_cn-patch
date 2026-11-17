# 控制台与诊断页文本 汉化审校记录（console 模块）

| 项目 | 内容 |
|---|---|
| 输入版本 | HellForge Launcher 0.4.0-beta（提交 d8a8b46，输入副本 `launcher-0.4.0-beta-input/HellForge.Launcher.dll`，609792 字节） |
| 输入哈希 | 与批次 1 同一副本：DLL SHA256 3EBFC7E2…4FE1（沿用 `launcher-0.4.0-beta-trial.md` 已记录值，本轮未重算） |
| 交付文件 | `launcher-0.4.0-beta-zhcn/modules/console.csv`（UTF-8，28 行） |
| 定位依据 | `work/ldstr_refs.tsv`（ldstr 引用）、`work/inventory-full.tsv`（候选盘点）、`work/trial-entries.csv`（16 条批准样本）、`work/zh-cn-master`（锁定项） |
| 本轮性质 | 静态文本定位 + 翻译，未运行程序、未改 DLL、未动 Git、未联网、未访问源安装目录 |
| 实机状态 | 未验证（无运行构建与截图） |

**口径假设。** 本版 `MainWindow.axaml` 编译产物中没有独立的诊断页：XAML 页头序列为 `ModsPage@17681`、`ConsolePage@19038`、`SettingsPage@20526`，未出现 `Diagnostics` 页名。因此本模块把「诊断页」理解为控制台页（`ConsolePage`，眉标 BACKEND、说明文字自述为实时后端请求）+ 其日志/诊断输出代码。若委托方后续提供截图证明另有诊断界面，需补检后追加。

## 1 范围与排除

### 1.1 控制台页 XAML

`MainWindow.!XamlIlPopulate` 的 IL 19038–20526 区间对应 `ConsolePage`（19038 起）到 `SettingsPage`（20526，下一页，不含）。区间内共 29 条 ldstr 引用，其中用户可见文本 7 条（见 CSV 前 7 行），其余 22 条为控件名与样式键，全部排除：

| 排除项 | 文本 | 理由 |
|---|---|---|
| 控件名 | `ConsolePage`、`AutoScroll`、`ClearButton`、`ConsoleLogsButton`、`ShareLogsButton`、`ConsoleList` | x:Name，非显示文本 |
| 样式键 | `eyebrow`、`h1`、`ghost`、`muted`、`CardBorderBrush`、`console`、`MonoFont` | 样式/字体键 |
| 下一页 | `SettingsPage` | 属设置页 |

### 1.2 控制台与日志显示相关代码

按方法名与引用位置确认为控制台列表/日志显示服务的字符串：

| 方法 | 作用（按方法名与用途归纳） | 收录 |
|---|---|---|
| `MainWindow.BackendMessage` | 后端输出行的前缀 | 1 条 |
| `MainWindow.ShowLiveResult` | 运行期改动结果追加到控制台的行 | 3 条 |
| `MainWindow.AppendSandboxLine` | 沙箱状态诊断行 | 4 条 |
| `MainWindow.AppendCoopRelaysLine` | 多人合作状态诊断行 | 2 条 |
| `MainWindow.AppendGameClosing` | 库存同步期间关闭游戏提示 | 2 条 |
| `MainWindow.SaveLogsToDesktop` | 保存日志到桌面的成功/失败提示及其拼接段 | 4 条 + 1 条共享格式 |
| `MainWindow.<>c__DisplayClass162_1.<PruneSessionLogs>b__2` | 旧日志清理提示（闭包） | 4 条 |
| `MainWindow.!XamlIlPopulate`（19038–20526） | 控制台页可见文本 | 7 条 |

### 1.3 明确排除

- 控制台请求行的内部格式：`AppendRequest` 中的 `timeUtc`、`status`、`path`、`method`、`outcome`（数据键），`--:--:--`、`HH:mm:ss`（时间格式），`/SeasonPass`、`/Pes/`（运行期路径），以及多个单空格分隔片段。
- 路径与文件名：`HellForge-logs-`、`yyyyMMdd-HHmmss`、`.zip`、`userdata`、`logs`、`proxy.log`、`steam://open/console`、`xdg-open`。
- 数据键：`Text`、`Brush`、`changes`、`blocking`、`detail`、`applied`。
- 纯 Linux 内容：`Sandboxed (…Wine prefix and a read-only filesystem view.)`（us=33406，Wine 前缀沙箱行，首版 Windows 范围排除）。
- 安装/卸载清单行：`AppendSteamRemovals`、`AppendSteamLeft`、`AppendOldScriptRemovals`、`AppendPrefixRemoval` 的 ` - Steam's …` 系列 16 条，属设置/安装模块的卸载确认清单，不是控制台显示文本。
- 设置页相邻项：`Engine log` 开关（us=86923、86945）、`BuildPaths` 诊断清单（us=31252–31414：Project/Installation/Data folder/Profiles/Templates/Selected profile/Current run/No session started yet）、设置页「打开 Steam 控制台」（us=90549、55715、55763、55833）。
- 模组页与档案/导入页文本、状态区文本、崩溃报告按钮文本。

## 2 交付摘要

`console.csv` 共 28 行：已译 18、保留 1、待裁定 9。字段为 `token,method_il,original,translation,status,context,decision_id`；`decision_id` 中 `CON-xx` 指向本文件待裁定项，`T-12` 指向批次 1 第 12 条锁定样本，`—` 表示例行译法。待裁定行 `translation` 留空（与主表、`launch-errors` 模块约定一致），草案与备选写在 3 节各 CON 项下，避免草案被误当定稿。

| 分组 | 行数 | 说明 |
|---|---|---|
| 控制台页 XAML | 7 | 眉标、标题、说明、复选框、3 个按钮 |
| 控制台日志行 | 6 | 后端前缀、实时改动结果 |
| 沙箱诊断行 | 4 | 已启用/未启用沙箱、关闭原因 |
| 多人合作诊断行 | 2 | Steam 中继关闭提示及其后段 |
| 库存同步诊断行 | 2 | 关闭正常游戏、保持连接说明 |
| 保存日志 | 5 | 无日志提示、成功提示前后段、共享 `" ("`、失败前段 |
| 日志清理 | 4 | 数量/容量/保留数量的拼接片段 |

跨文件重叠说明：us=31774 已存在于 `zh-cn-master.csv`（锁定，T-12），本模块为可追溯而原样收录，不重复翻译，合并时以主表为准。us=75945、71663、31710、31716、1015、33611 的译文与设置页或崩溃报告界面共用；若其他模块 CSV 也收录同一 token，其译文须与本表逐字一致。

## 3 待裁定项

### CON-01 控制台眉标 BACKEND

| 字段 | 内容 |
|---|---|
| 类型 | 样式口径 |
| 关联条目 | token 0x70012865（us=75877），`MainWindow.!XamlIlPopulate@19290` |
| 原文 | `BACKEND` |
| 语境 | 控制台页一级标题「Console」上方的眉标（eyebrow），纯装饰性小标题；同页说明文字说明控制台展示实时后端请求。 |
| 候选 | 后端 / 保留 `BACKEND` |
| 候选区别 | 「后端」与已译的「本地后端」用词一致、信息准确；保留英文可与界面其余大写眉标（DEPLOYMENT、HELLDIVER、SYSTEM）保持视觉统一。 |
| 建议 | 后端（暂定），并与批次 1 的 PD-001 `DEPLOYMENT`、PD-003 `HELLDIVER` 及设置页 `SYSTEM` 眉标一并定口径。 |
| 理由 | 语义无争议，争议只在眉标是否译；单条裁定会造成同风格眉标中英混排。 |
| 状态 | 待裁定 |

草案译法：0x70012865 → `后端`（与「本地后端」用词一致；若决定眉标整体保留英文，则整条保留 `BACKEND`）。

### CON-02 沙箱术语族

| 字段 | 内容 |
|---|---|
| 类型 | 术语 |
| 关联条目 | 0x700081B3（us=33203 `AppendSandboxLine@29`）、0x7000834B（us=33611 `AppendSandboxLine@115`）、0x7000837F（us=33663 `@122`）、0x700083BF（us=33727 `@128`） |
| 原文 | `Sandboxed (Settings > Sandbox): …` / `Settings > Sandbox is off` / `This session is not sandboxed (` / `). The game, its mods and anything they run can write your files.`，以及 `low integrity`、`Steam broker` |
| 语境 | 控制台诊断行，说明本会话是否在沙箱中运行；`Settings > Sandbox` 是设置页开关，属设置/安装模块的同一术语。 |
| 候选 | sandbox：沙箱 / 沙盒；Steam broker：Steam 中转 / Steam 代理 / Steam 中介；low integrity：低完整性 / 低完整性级别 / 低权限级 |
| 候选区别 | 「沙箱」是 Windows/浏览器领域常见译法，与「网络阻断」「断网」等已出现技术词区分清楚；「沙盒」偏测试环境语义。「中转」描述 broker 只转发所需调用的行为；「代理」更像通用 proxy。「低完整性级别」完整对应 Windows 完整性级别，单说「低完整性」略短。 |
| 建议 | 沙箱 / Steam 中转 / 低完整性级别；请与设置/安装模块统一后回填。 |
| 理由 | 这 4 条与设置页开关文案共用同一术语，逐模块各自定名会造成界面内不一致；本模块只给草案。 |
| 状态 | 待裁定 |

草案译法：

| token | 草案译文 |
|---|---|
| 0x700081B3 | 已启用沙箱（设置 > 沙箱）：游戏以低完整性级别运行，Steam 连接经由 Steam 中转。 |
| 0x7000834B | 设置 > 沙箱已关闭 |
| 0x7000837F | 此会话未启用沙箱（ |
| 0x700083BF | ）。游戏、模组以及它们运行的一切都能写入你的文件。 |

### CON-03 多人合作术语族

| 字段 | 内容 |
|---|---|
| 类型 | 术语 |
| 关联条目 | 0x70005D55（us=23893 `AppendCoopRelaysLine@30`）、0x70005E6E（us=24174 `@58`） |
| 原文 | `Co-op over Steam relays is off (Settings > Multiplayer): other players' lobbies show but can't be joined; the lobby browser can turn it on.` / ` Until then this session plays without co-op.` |
| 语境 | 控制台诊断行，说明本次会话的多人合作经 Steam 中继不可用；`Settings > Multiplayer` 为设置页开关。 |
| 候选 | co-op：多人合作 / 合作模式 / 联机合作；Steam relays：Steam 中继 / Steam 中继转发；lobbies：房间 / 大厅；lobby browser：大厅浏览器 / 房间浏览器 |
| 候选区别 | 「多人合作」直译且不与游戏内「合作模式」菜单名冲突；「大厅浏览器」与游戏内大厅概念贴合；「房间」更口语但玩家易懂。 |
| 建议 | 多人合作 / Steam 中继 / 房间 / 大厅浏览器；优先与设置页 `Multiplayer` 区文案统一。 |
| 理由 | 属设置/安装模块的开关周边文本，跨模块必须同词；本模块只给草案。 |
| 状态 | 待裁定 |

草案译法（`␠`=半角空格，按现有拼接保留）：

| token | 草案译文 |
|---|---|
| 0x70005D55 | Steam 中继的多人合作已关闭（设置 > 多人游戏）：其他玩家的房间会显示但无法加入；可由大厅浏览器开启。 |
| 0x70005E6E | `␠`在此之前，本次会话将不启用多人合作。 |

旁证：`launch-errors` 模块 ERR-01 对 `Settings > Multiplayer` 的草案同样取「设置 > 多人游戏」，本模块已对齐；若设置/安装模块最终改用别的标签，本条与 ERR-01 一并改。

### CON-04 库存同步与捕获术语

| 字段 | 内容 |
|---|---|
| 类型 | 术语 |
| 关联条目 | 0x700021D2（us=8658 `AppendGameClosing@27`）、0x700022C5（us=8901 `@34`） |
| 原文 | `Inventory sync: HellForge is closing the normal game it opened for the sync; start it from Steam again to play normally.` / `Inventory sync: the game stays connected through the capture until you close it; then the hosts line and certificate are removed.` |
| 语境 | 控制台诊断行，库存同步期间追加；同一批文本中另有 `capture`、`hosts line`、`certificate` 等词。 |
| 候选 | Inventory sync：库存同步 / 清单同步；capture：捕获 / 抓取 / 截取；hosts 行：保留 `hosts 行` |
| 候选区别 | 批次 1 已把 `Sync Inventory` 定为「同步库存」、`inventory` 定为「库存」，故「库存同步」有已批准词根依据；「捕获」对应本工具抓取登录数据的行为，「抓取」偏网络爬取；`hosts` 是文件名，保留英文。 |
| 建议 | 库存同步 / 捕获 / hosts 行；待共享状态模块确认 `Inventory sync` 的固定译法后回填。 |
| 理由 | `Inventory sync` 在启动、状态与档案模块多处出现，需一处定名；本模块只给草案。 |
| 状态 | 待裁定 |

草案译法：

| token | 草案译文 |
|---|---|
| 0x700021D2 | 库存同步：HellForge 正在关闭它为同步而打开的正常游戏；请从 Steam 重新启动，才能正常游玩。 |
| 0x700022C5 | 库存同步：游戏会通过捕获保持连接，直到你关闭它；之后 hosts 行和证书会被移除。 |

## 4 拼接边界

`␠` 表示真实半角空格，CSV 中为真实空格。片段按 IL 顺序拼接，语序只在片段内部调整。

| 组 | 原文拼接 | 译文拼接 |
|---|---|---|
| 保存日志成功 | `Saved the latest session's logs to␠` + 路径 + `␠(` + N + `␠files in use were left out)` | `已将最近一次会话的日志保存到␠` + 路径 + `␠(` + N + `␠个正在使用而略过的文件)` |
| 日志清理 | `Removed the logs of␠` + N + `␠older session(s) (` + MB + `␠MB); the newest␠` + N + `␠stay.` | `已删除␠` + N + `␠个较早会话的日志（` + MB + `␠MB）；最新的␠` + N + `␠个保留。` |
| 未启用沙箱 | `This session is not sandboxed (` + 原因 + `). The game, its mods and anything they run can write your files.` | `此会话未启用沙箱（` + 原因 + `）。游戏、模组以及它们运行的一切都能写入你的文件。` |
| 后端输出 | `HellForge local backend:␠` + 后端输出 | `HellForge 本地后端:␠` + 后端输出 |
| 实时改动 | `Applied to the running game:␠` + 列表（共享 `,␠` 分隔）+ `.␠` + 说明；另有 `Mods:␠` 行与 `␠Friends need the same mods to join.` | `已应用到运行中的游戏:␠` + 列表 + `.␠` + `␠好友需要相同的模组才能加入。`；`Mods:␠`→`模组:␠` |
| 库存同步提示 | 两条为独立整句，无拼接 | 两条独立整句 |

跨模块共享格式片段未改动：us=3317 `:␠`（13 处引用，批次 1 锁定）、us=31710 `␠(`（11 处引用，本模块按保留处理）、us=165 单空格（多处拼接空格）。其中 `:␠` 与 `␠(` 保持 ASCII，保存日志失败行沿用锁定译法「无法保存日志:␠」。

片段首尾空格按本轮要求原样保留。`launch-errors` 模块 ERR-03 仍在讨论「中文与中文之间是否保留前导空格」（其例为 ` is missing.` 接在「本地后端」之后），若最终决定去掉中文间空格，本模块 0x70005E6E、0x70007BE4 等前导空格片段需同步调整；本轮不做此改动，待项目统一。

## 5 有效覆盖与余留

盘点表把 42 条候选归入「控制台」，本模块覆盖 16 条；其余 26 条按下表处理。另有 12 条不在盘点「控制台」归属内、但按控制台页/日志显示面确认为本模块范围（控制台页 XAML 7 条属「界面静态」，`HellForge local backend: ` 等 4 条属「未分类」，共享格式 `␠(` 1 条盘点归「模组」但为跨页共用）。合计 28 行。

| 处理 | 条数 | 明细 |
|---|---|---|
| 本模块已收录 | 16 | us=8658、8901、23893、24174、31460、31638、31716、31774、33203、33611、33663、33727、92499、92541、92581、92617 |
| 转出：安装/卸载清单 | 16 | us=12750、12941、13049、13127、13153、13229、13287、13369、13497、13537、13663、13683、13816、13973、14300、14404，属设置/安装模块 |
| 转出：设置页 Steam 控制台 | 3 | us=55715、55763、55833（设置页「打开 Steam 控制台」按钮周边） |
| 排除：日志内部格式 | 2 | us=30297 `--:--:--`、30315 `HH:mm:ss` |
| 排除：文件名/属性 | 3 | us=31546 `HellForge-logs-`、31578 `yyyyMMdd-HHmmss`、125672 `Text` |
| 排除：路径/命令 | 2 | us=55655 `steam://open/console`、55697 `xdg-open` |

控制台范围内的余留：

1. 设置页同名控件 `Open session logs`（us=75945 的第二个引用点 IL 30208）与 `Engine log` 开关、`BuildPaths` 诊断清单由设置/安装模块统一处理；本模块已给出 `Open session logs` 的译法，设置页直接复用即可。
2. 控制台是否还渲染其他子系统的运行期日志行，静态提取无法证明；本模块只覆盖方法名与引用结构能确认的控制台行构造方法，属已知余留风险，需实机日志截图确认。
3. 4 项跨模块术语（CON-01 至 CON-04）落定后，本模块 9 条待裁定行即可转已译。
4. 实机项：控制台等宽字体（`MonoFont`）对中文的字体回退、长说明换行、按钮宽度、2xx/501 颜色是否可辨，均未验证。

## 6 机器核对

脚本 `work/console_scratch/con_qa.py` 重新解析 CSV，并与 `work/ldstr_refs.tsv` 逐条比对，结果：

| 检查项 | 结果 |
|---|---|
| 行数与列数 | 通过：28 行，7 列，列名与约定一致 |
| 编码 | 通过：UTF-8 无 BOM，LF 换行，末行有换行 |
| token 唯一 | 通过：28 个唯一 token；全部满足 `token = 0x70000000 + us` |
| 原文字符一致 | 通过：28/28 与引用表原文逐字一致（含首尾空格） |
| method_il 对应 | 通过：28/28 能在引用表中命中同 token 同方法同 IL |
| 首尾空格 | 通过：原文有前导/尾随空格的 13 行中，12 行已译/保留行译文对应保留；1 行待裁定（us=24174）译文按约定留空，第 3 节草案保留首空格 |
| 状态取值 | 通过：18 已译 / 1 保留 / 9 待裁定，均在允许集合内 |
| 待裁定编号 | 通过：9 条待裁定全部挂 CON 编号、译文留空，草案均在本文件有记录；4 个 CON 编号均被引用 |
| 重复 | 通过：无重复 token，无重复原文 |
| 缺译 | 通过：非待裁定行无空译文；9 条待裁定行按约定留空并在第 3 节给出草案 |
| 拼接边界 | 通过：5 组拼接 + 1 组独立整句，片段数量与空格位置见第 4 节 |
| 实机验证 | 待验证：未提供构建与截图 |

## 7 假设与待办

- 假设本版无独立诊断页（依据：XAML 页头只有 Mods/Console/Settings 三页，无 Diagnostics 页名）；如另有诊断界面，按其引用点补检。
- 假设 `AppendSandboxLine`、`AppendCoopRelaysLine`、`AppendGameClosing`、`ShowLiveResult` 的行进入控制台列表（依据：方法名为行追加构造、`ShowLiveResult` 绑定 `LogLine.Text/Brush`、盘点将其中多条归入「控制台」）；未实机确认显示位置。
- 待办：与设置/安装、共享状态两个会话统一 CON-01 至 CON-04 的术语；提供构建后补做控制台实机核对。
