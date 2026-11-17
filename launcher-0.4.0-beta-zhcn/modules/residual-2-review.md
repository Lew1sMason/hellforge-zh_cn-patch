# HellForge 启动器 0.4.0-beta 简体中文：余留队列第 2 组（Windows 全量收尾）

本批只处理 `work/residual-review-queue-2.csv` 的 94 条已分派候选，不触碰其他队列、其他组产出、总表与源安装。只写 `launcher-0.4.0-beta-zhcn/modules/residual-2.csv` 与本文件；未运行程序、未联网、未改 DLL/Git、未重新解析程序集。上一轮产物（`profiles-mods.csv`、`account-sync.csv`、`residual-ledger.csv` 等）保持原样。

## 1 范围、口径与去向

队列给 94 条候选（86 条初判可见、8 条初判待查），`class=可见` 只是按方法初判，本批逐条核实原文与 `ldstr_refs.tsv` 调用点后再定去向。核实依据：

- `work/us_all.tsv`：逐条核对原文、`#US` 偏移与 token；94 条全部逐字一致。
- `work/ldstr_refs.tsv`：按 token 反查调用方法、类型与 IL；94 条全部命中。同一方法内相邻 IL 的字符串用于判断拼接关系与界面位置。
- 相邻模块口径：`modules/console-review.md`（AppendOldScriptRemovals 非控制台显示、OpenSteamConsole 属设置页「打开 Steam 控制台」）、`modules/settings.csv`（Steam 桥接）、`modules/account-sync.csv`（共享右括号 1127、采集/管理员提示用词）、`modules/profiles-mods.csv` 与 `modules/residual-review.md`（模组同步卡、TakeCapture 待查结论）。
- 已确认术语按用户裁定使用：会话启动程序、开始游戏、停止、同步、模组、档案、沙盒、属性；本队列字符串不涉及部署/模组部署/本地会话/模组库/HELLDIVER 副本档案/战争债券/超级商店物品/DLC装备/超级货币，故这些仅作口径记录。

去重口径：队列已由主会话去掉其他组与现有成果，本批信任队列的范围筛选，未重扫总表与各模块文件以免重复读取大文件；CSV 行均来自队列 token，未新增队列外 token。

去向总账（94 = 80 + 5 + 9，每 token 一条去向）：

| 去向 | 数量 | 说明 |
|---|---|---|
| 写入 `residual-2.csv` | 80 | 已译 76、保留 2、待裁定 2 |
| 排除（仅评审列明） | 5 | Linux 专属、安装/卸载清单、疑内部日志 |
| 待查（仅评审列明） | 9 | 缺显示位置证据，不作可见/已译判定 |

## 2 产出统计（`residual-2.csv`）

| 项目 | 数量 | 说明 |
|---|---|---|
| 行数 | 80 | 七列：token,method_il,original,translation,status,context,decision_id |
| 已译 | 76 | 其中 26 条为含首/尾空格的拼接片段行，接缝逐字保留 |
| 保留 | 2 | 模组标签 LUA、ZIP（技术专名） |
| 待裁定 | 2 | R2-01、R2-02，见第 5 节 |
| 方法组 | 29 | 模组同步卡、模组标签、同步清理、导入规则、变更说明、会话/崩溃状态、安装/卸载/下载、设置等 |

按界面与功能分组（写入行）：

| 组 | 行数 | 代表条目 |
|---|---|---|
| 模组同步卡片段（信任/屏蔽/已下载列表） | 12 | 受信任的模组（、来自 、内容哈希、来自主机 ( |
| 模组行标签 Tags | 9 | 未编译、不支持、内置、外观包、原生、属性、数据、LUA、ZIP |
| 同步清理状态（`<CleanUpSync>`） | 5 | 安装文件夹不存在。、清理需要管理员权限提示。、清理完成…… |
| 导入规则标签 RuleLabel | 5 | 同原版、所有物品、无、保留较高者、使用原版 |
| 模组变更说明片段 ModChanges | 4 | 网络字段 、 位、 属性变更、 游戏数据文件 |
| 会话结束/崩溃状态 | 7 | 游戏关闭了窗口但未退出……、会话已结束。、游戏崩溃了。 |
| 导入/同步完成提示 | 6 | 已同步。请在下方选择要导入的内容。、已导入。事先已备份档案…… |
| 安装/卸载/下载/主按钮状态 | 18 | 主按钮 停止/正在停止/正在安装、卸载确认长说明、安装 depot 诊断、Steam 控制台 |
| 设置/标签/其它状态 | 14 | 全部开启/全部关闭、复制、已保存、正在构建 、已复制 |

## 3 排除 5 条（不进 CSV）

| token | 方法 | 原文 | 理由 |
|---|---|---|---|
| 0x7001A0E0 | `<FindGameStep>d__360.MoveNext@1212` | `. Setup ` | Linux 专属：与下一行连成「Setup runs inside HellForge's network namespace…」，同方法前段自述 On Linux；Windows 首版不纳入。 |
| 0x7001A0F2 | `<FindGameStep>d__360.MoveNext@1229` | `runs inside HellForge's network namespace and cannot reach Steam's servers itself; …` | 同上；网络命名空间为 Linux 机制，Windows 分支不走该文案。 |
| 0x700037DC | `MainWindow.AppendOldScriptRemovals@9` | `  - the removed shell installer's files: none found` | Linux 卸载清单行；`console-review.md` 已核为该组行属安装/卸载清单、非控制台显示文本，且 shell installer 为 Linux 专属。 |
| 0x70003844 | `MainWindow.AppendOldScriptRemovals@52` | `  - the removed shell installer's ` | 同上，为上一行的拼接前段。 |
| 0x7001736C | `<>c__DisplayClass432_1.<DownloadWithSteamCmd>b__5@11` | `SteamCMD: ` | 疑内部日志前缀：该回调中仅此一个字符串，形态为「SteamCMD: +进程输出」日志行，无控件/状态区证据；按内部日志口径跳过，未译。 |

## 4 待查 9 条（不进 CSV，保留待证据）

| token | 方法 | 原文 | 缺证据点 |
|---|---|---|---|
| 0x70001F5C | `MainWindow.TakeCapture@32` | `capture not taken: ` | 同步采集诊断文本；仅 TakeCapture 一处引用，同方法相邻字符串含路径/日志拼接（capture taken into …proxy.log），无法区分状态卡与内部日志。沿用 `residual-review.md` 待查结论。 |
| 0x70001F84 | `MainWindow.TakeCapture@98` | `capture taken into ` | 同上；后接采集目录路径，疑日志行。 |
| 0x70001FAC | `MainWindow.TakeCapture@149` | ` items, progression ` | 同上；数量/进度片段，显示位置未证实。 |
| 0x70001FDC | `MainWindow.TakeCapture@195` | `capture ` | 同上；与 exited / still forwarding 拼接，疑日志。 |
| 0x70001FFC | `MainWindow.TakeCapture@235` | `still forwarding the game` | 同上。 |
| 0x70002030 | `MainWindow.TakeCapture@261` | `The capture got your inventory but not your progression (see ` | 同上；含 proxy.log 路径。 |
| 0x700020AC | `MainWindow.TakeCapture@277` | `). Nothing was imported; sync again.` | 同上；若为状态卡则属共享状态范围，待实机同步状态区截图确认。 |
| 0x700020F6 | `MainWindow.TakeCapture@300` | `Inventory sync complete for profile ` | 同上；完成提示与档案名拼接，位置未证实。 |
| 0x7000D25F | `MainWindow.SteamHas@19` | `no HELLDIVERS 2 setup can copy from` | 证据不足：SteamHas 方法内仅 3 个分支字符串（另有 Wine 只读分支），本片段缺主语/整句结构，可能是内部状态或拼在「Steam has …」之后；不作可见判定。 |

建议下一步：取同步状态区、设置页 Steam 控制台与安装进度区截图，或由共享状态/安装模块确认 TakeCapture、SteamHas 的显示归属；证据到位后可补译入表。

## 5 待裁定（R2-01 起）

### R2-01 「 mod」复数与量词片段

| 字段 | 内容 |
|---|---|
| 类型 | 拼接片段/跨 token |
| 关联条目 | us=39777，token 0x70009B61，`MainWindow.AddModSyncCard@2194`（同 token 亦见 ModsSummaryText@98） |
| 原文 | ` mod` |
| 语境 | 模组页摘要「N of M mods」与已下载模组数量「N mods from hosts (X MB)…」共用；相邻片段还有复数后缀 `s`（0x70009B6B，不在本队列）与共享 ` of `（0x70007767，属 PM-04 未决）。 |
| 候选 | A 单独译「 个模组」，但 `s` 残留会成「模组s」；B 与 `s` 合并为一个整体「 个模组」（需同时改两 token）；C 保留英文 ` mod` |
| 候选区别 | A 改动最小但输出破损；B 中文正确、需跨模块协调 0x70009B6B；C 与摘要其余中文混排突兀。 |
| 建议 | B：把 0x70009B61 + 0x70009B6B 视为整体译为「 个模组」，由主会话合并时同步处理复数后缀；本行暂空。 |
| 理由 | 单片段无法独立成句，复数后缀与「 of 」分属不同 token，须整句口径统一。 |
| 状态 | 待裁定 |

### R2-02 「 options on」数量摘要语序

| 字段 | 内容 |
|---|---|
| 类型 | 拼接语序 |
| 关联条目 | us=45913，token 0x7000B359，`MainWindow.ModRow@1316` |
| 原文 | ` options on` |
| 语境 | 模组行摘要「N of M options on」，前接共享 ` of `（0x70007767，PM-04 未决）与数字，后接 `" · "` 等状态。 |
| 候选 | A 在 PM-04 采用「 / 」后译「 个选项已开启」，拼成「3/5 个选项已开启」；B 改写为「M 个选项中 N 个已开启」，需跨片段移动信息；C 保留英文 |
| 候选区别 | A 与 PM-04 建议兼容、改动小，但「N/M 个选项」略机械；B 最自然但违反片段顺序规则；C 不解决中文摘要。 |
| 建议 | A：待 PM-04 定为「 / 」后，本片段译「 个选项已开启」；若 PM-04 改选其它方案，本片段随之调整。本行暂空。 |
| 理由 | 语序由固定片段顺序决定，单独翻译无法成句。 |
| 状态 | 待裁定 |

## 6 QA 与机器核对

| 检查项 | 结果 | 说明 |
|---|---|---|
| 队列全覆盖 | 通过 | 94 token 全部有去向：80 写入 CSV、5 排除、9 待查；无漏项、无队列外 token |
| 原文一致 | 通过 | 94 条与 `us_all.tsv` 逐字比对一致；CSV 80 行再次逐字复核 0 差异 |
| 定位可回溯 | 通过 | 94 条 `方法@IL` 均在 `ldstr_refs.tsv` 命中（类型+方法+IL），CSV 已按 `MainWindow.<方法>@IL` 或状态机类型名归一 |
| token 唯一 | 通过 | 80 行无重复 token |
| 状态与编号 | 通过 | 状态仅 已译/保留/待裁定；待裁定 2 行均挂 R2-01/R2-02；其余 `decision_id` 为「—」 |
| 首尾空格 | 通过 | 28 条含首/尾空格：26 条已译行的接缝逐字保留（前导 13 条、尾随 14 条，其中 1 条两端均有），2 条待裁定行无译文；脚本比对 0 处不匹配 |
| ASCII 冒号/括号 | 通过 | 5 条含 ASCII 冒号片段（4 条为「…: 」尾接缝，1 条为「: …」起始片段）；` from hosts (` 与 ` MB)` 半角括号配对；`Trusted mods (` 接共享右括号 1127「）」 |
| 格式 | 通过 | UTF-8 带 BOM、LF、7 列，80 行 |
| 术语一致 | 通过 | 会话启动程序、开始游戏、停止、同步、模组、档案、沙盒、属性与既有模块一致；LUA/ZIP 保留 |

## 7 假设与限制

- 队列已由主会话完成跨模块去重，本批未重扫总表/模块文件复核 token 交集（避免重复读取大文件）；若队列后续变更，以新队列重跑同法。
- `ShowDepotProgress` 两条按安装进度/诊断文本译入（与 `settings-followup.csv` 对同类安装进度片段的处理一致）；若实机确认只进日志，可整组退回排除。
- `OpenSteamConsole` 三条按 `console-review.md` 的归属按设置页「打开 Steam 控制台」状态译入。
- 可见性判断止于方法/IL 与相邻字符串，不含实机截图；排除/待查均写明缺证据点，未把不确定项强行定稿。
- 共享 token（0x70009B6B 复数 `s`、0x70007767 ` of `、0x70007BDE ` (`、0x70000029 共享句点等）不在本队列，未改动；相关行只按现有译文/原文引用。
- 未改动其它输出；未运行、联网、改 Git、接触源安装。

## 8 交付

| 文件 | 内容 | 校验 |
|---|---|---|
| `launcher-0.4.0-beta-zhcn/modules/residual-2.csv` | 80 行：76 已译、2 保留、2 待裁定；七列；UTF-8 带 BOM、LF | 原文/token/定位/空格/重复/队列去向全部通过 |
| `launcher-0.4.0-beta-zhcn/modules/residual-2-review.md` | 本文件：去向总账、排除 5、待查 9、R2-01/R2-02、QA | — |
