# 设置页、安装与引导 补充批次复核（settings-followup）

只补齐 `settings-review.md` 第 7 节列出的、证据可核对且语境足够的三类剩余项：安装流程 Windows 进度/版本拼接、共享确认对话框、设置导入状态。上轮 `settings.csv` 与 `settings-review.md` 未改动；主表、锁定样本、其他模块文件、输入 DLL 未改动。机器可读结果在同目录 `settings-followup.csv`，字段与上轮相同。

## 1 范围与筛选

| 来源（上轮报告） | 候选 | 本批 | 处理 |
|---|---|---|---|
| 安装流程 Windows 进度/版本拼接 | 18 | 17 | 逐条核对所属方法内 IL 先后，按拼接链复原后翻译 |
| 共享确认对话框代码文案 | 7 | 6 | 102115 已由启动错误模块合并进主表且译法一致，不重复列出 |
| 设置页导入提示三段拼接 | 3 | 3 | 67365 + 运行期值 + 67604/67634 两个分支 |

判据与上轮一致：写入显示控件或状态标签的片段；控制名、样式键、路径、脚本参数、格式说明符不译。不重读整表，只按 us 索引定点取 `work/us_all.tsv` 原文与 `work/ldstr_refs.tsv` 调用点。

## 2 条目统计

26 条：已译 24、待裁定 1、保留 1。与上轮 `settings.csv` 无重复 token，与主表、`launch-errors.csv` 无重复 token。

| 区域 | 条数 | 明细 |
|---|---|---|
| 安装引导页·进度/版本拼接 | 17 | 二维码下载 5（103132、103170、103200、103270、103280）、SteamCMD 下载 5（104135、104187、104229、104769、104910）、查找游戏 6（106516、106530、106540、107309、107327、107373）、运行库提示 1（109461） |
| 共享确认对话框·关闭流程 | 6 | 101790、101824、101908、101940、102073、102231 |
| 设置页·游戏设置导入 | 3 | 67365、67604、67634 |

首尾空格：16 条片段带边缘空格（首空格 9 条、尾空格 12 条、两端 5 条），逐字保留并与拼接位置对应。另有 1 条保留项（103270，仅空格与 `GB` 单位）。

## 3 拼接链复原（按方法内 IL 先后；`{…}` 为运行期值）

**二维码下载（`<DownloadWithQr>`）**

`Signed in. The download's progress shows under Game files.` + `Downloading build ` + `{版本}` + ` from Steam...` + ` files (` + `{容量}` + ` GB) from Steam for your account: ` + `{进度}` + ` GB ` + `downloaded, ` + `{进度}` + ` GB copied from your Steam install. Each file verified against Steam's hashes.`

中文：`已登录。下载进度显示在“游戏文件”下。` + `正在下载版本 ` + `{版本}` + ` 来自 Steam……` + ` 个文件（` + `{容量}` + ` GB），由 Steam 为你的账户提供：` + `{进度}` + ` GB ` + `已下载， ` + `{进度}` + ` GB 复制自你的 Steam 安装。每个文件都已对照 Steam 的哈希校验。`

**SteamCMD 下载（`<DownloadWithSteamCmd>`）**

成功：` files (` + `{容量}` + ` GB), downloaded by SteamCMD for your account, each verified against ` + `Steam's hashes. SteamCMD and what it remembered of the sign-in were removed.`

中文：` 个文件（` + `{容量}` + ` GB），由 SteamCMD 为你的账户下载，每个文件都已对照 ` + `Steam 的哈希校验。SteamCMD 以及它记住的登录信息已被移除。`

开始：`SteamCMD downloads build ` + `{版本}` + ` for your account...` → `SteamCMD 会下载版本 ` + `{版本}` + ` 到你的账户……`

失败分支：`…it could not be set up (` + `{详情}` + `).`，本批只处理左段 104229（待裁定 SET-F01），右段 `).`（67808）是与 Linux 前缀共用的分隔符，未改动。

**查找游戏（`<FindGameStep>`）**

`Build ` + `{版本}` + ` in ` + `{路径}` + `, downloaded by Steam into ` + `{路径2}` → `版本 ` + `{版本}` + ` 位于 ` + `{路径}` + `，已由 Steam 下载到 ` + `{路径2}`

`No HELLDIVERS 2 setup can copy from. Steam sends build ` + `{版本}` + ` (about ` + `{容量}` + ` GB) for your account.` → `没有可供配置复制的 HELLDIVERS 2。Steam 会发送版本 ` + `{版本}` + ` （约 ` + `{容量}` + ` GB）。`

`. Steam sends build ` + `{版本}` + ` for your account; what your install already has is copied, not downloaded.` → `。Steam 会发送版本 ` + `{版本}` + ` 到你的账户；你的安装中已有的部分会被复制，而不会重新下载。`（`for your account` 由已译的 107415 承接）

**关闭确认（`<ConfirmCloseAsync>`）**

`Stopping session` / `Closing the game and the local backend...`；成功：`Session stopped`；超时但已结束：`The session did not stop in time, so it was ended before closing.`；失败：`Session did not stop` + `The session did not stop in time and could not be ended: ` + `{详情}` + ` Closing anyway.`

中文：`正在停止会话` / `正在关闭游戏与本地后端……`；`会话已停止`；`会话未能及时停止，因此在关闭前已将其结束。`；`会话未能停止` + `会话未能及时停止，也无法结束: ` + `{详情}` + ` 仍将关闭。`

**游戏设置导入（`<InitializeSettingsImport>`）**

`Nothing to import: the normal HELLDIVERS 2 has no settings on this PC yet (play it once, or check that it is the same ` + `{运行时值}` + （`Windows user).` | `Steam installation HellForge runs under).`）

中文：`没有可导入的设置：本机上的正常 HELLDIVERS 2 还没有设置（先游玩一次，或确认它与 HellForge 运行在同一个 ` + `{运行时值}` + （`Windows 用户下）。` | `Steam 安装下）。`）

两个后缀原文都没有前导空格，说明运行期值自带分隔（与英文 “the same {值} Windows user” 一致），因此译文也不加前导空格，避免运行时出现双空格。

## 4 待裁定 SET-F01

| 字段 | 内容 |
|---|---|
| 类型 | 括号格式 / 共享分隔符 |
| 关联 | HF-104229（us=104229，token 0x70019725，`<DownloadWithSteamCmd>d__432.MoveNext@1723`，偏移 520893）；右段为 67808 `).`，同时被 Linux 的 `<InitializePrefix>d__19.MoveNext@400` 使用 |
| 原文 | `it could not be set up (` + `{详情}` + `).` |
| 语境 | SteamCMD 失败分支的错误详情；前导片段在字符串堆内不可见，主语需按运行时上下文确认 |
| 候选 | A 保留 ASCII 括号：`无法完成配置 (` + `{详情}` + `).`；B 全角括号：`无法完成配置（` + `{详情}` + `），并把共享分隔符 67808 改成 `）。`；C 不改字符串，由上游把整句合为一个片段 |
| 差别 | A 不动共享 token，改动最小，但错误详情处英文括号与中文混排；B 视觉统一，但 67808 在 Linux 前缀提示里与 ASCII `(` 配对，会变成 `(` 与 `）` 混用；C 效果最好，但需改代码，超出译文范围 |
| 建议 | A。本行暂留空，其余 25 条不受影响 |

## 5 与主表、上轮的关系

- 102115「The session did not stop in time and could not be ended: 」已由 `launch-errors.csv` 合并进主表（HF-102115），译法与本轮一致，未重复。
- 上轮 `settings.csv` 已有 `Session running`、`A play session is running. Stop it and close the game?`、`Keep playing`、`Stop and close` 4 条（设置页确认浮层 XAML 位置）；本批补的是同一对话框的代码侧状态文案，合并时两处 token 相同、译文一致，无需去重。
- 跨批次接缝：上轮 HF-107197「No HELLDIVERS 2 setup can copy from. Steam sends build 」译为「没有可供配置复制的 HELLDIVERS 2。Steam 会为你的账户发送版本 」，已含「为你的账户」；本轮 107327 原文的 `for your account` 若直译会重复，故译作「 GB）。」。若合并时要求逐字对应，可把 107197 改回「Steam 会发送版本 」、107327 改回「 GB），供你的账户使用。」。
- 共享确认对话框的 4 个按钮/标题 token 与启动页模块的 `ConfirmCloseAsync` 文案共用，本节未新增共享 token 改动。

## 6 未处理项

- 106720 `. Setup `：其后只接 Linux 专属的 106738（「runs inside HellForge's network namespace…」），Windows 路径不出现完整链，按纯 Linux 文案不译。
- 67808 `).`：与 Linux 前缀共用的格式分隔符，随 SET-F01 一并决定，本轮不改。
- 上轮报告第 7 节其余剩余项（分隔符/路径/脚本参数、后端参数键、Linux 安装文案）维持不译，状态不变。

## 7 验证与边界

本批只写入 `modules/settings-followup.csv` 与本文件；上轮 `settings.csv`、`settings-review.md` 与其他模块文件未改动，主表未改动。未运行程序，未联网，未访问真实安装目录或 Git。

逐行验证：原文取自 `work/us_all.tsv` 的 `#US` 堆逐字回填；每行 `method_il@偏移` 在 `work/ldstr_refs.tsv` 中存在同一 us 的调用点且文本与堆一致；`token` 由 us 推导核对；`context` 内声明的 us 与偏移与实际记录一致；26 行 token 唯一；待裁定行译文为空且有编号；已译/保留行译文非空；16 条片段的首尾空格与原文逐条比对；CSV 回读逐字一致，UTF-8 带 BOM，七列固定。

未验证项：界面实际显示与换行；拼接后的完整句子按方法内 IL 先后复原，未在运行环境核对；104229 前导片段与主语需按运行时确认（SET-F01）。
