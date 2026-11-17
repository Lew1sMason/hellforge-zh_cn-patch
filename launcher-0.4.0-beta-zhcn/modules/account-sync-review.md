# HellForge 启动器 0.4.0-beta 简体中文：账户同步增量批（存档/账户同步状态、进度、失败与引导）

构建 0.4.0-beta，输入副本 DLL SHA256 `3EBFC7E2…4FE1`。本批只读 `work/` 内既有证据文件，未重新解析程序集，未启动程序，未联网，未修改 DLL/Git。产出 `launcher-0.4.0-beta-zhcn/modules/account-sync.csv` 与本文件，二者仅由本批书写。

## 1 范围与口径

本批补齐上一轮档案模块余留中的账户同步可见文案：

- `UpdateSyncStatus` 余留：清理按钮与“上次同步未完成”说明（PD-004 运行期拼接项除外）。
- `UpdatePlaySync`：同步状态卡全部可见状态词与说明（上次同步归属、无法检查、付费内容锁定、管理员提示、同步成功、同步/更新按钮）。
- `Sync*`：`SyncStartingText`、`SyncNotStarted`、`SyncRefusal`、`RefreshSync`、`WatchSyncProgress`、`SyncFailed`、`OpenGameForSync`、`<StopSyncForCloseAsync>` 的启动等待、拒绝、失败、进度、引导与关闭前清理文案。
- 方法内补充的可见片段：同步文件夹读取失败说明（6669）、采集诊断括号内的 no/yes（6621/6627）、共享右括号片段（1127）。

证据口径与上一轮一致：`work/us_all.tsv` 取原文、`#US` 偏移与 token；`work/ldstr_refs.tsv` 取方法@IL；`work/inventory-full.tsv` 作候选池；`work/trial-entries.csv`、`zh-cn-master.csv` 中已锁定译文作准。“capture”在同步取数语境统一译“采集”，“administrator prompt”统一译“管理员权限提示”，“title screen”统一译“标题画面”，“play page”沿用“开始页”。

覆盖冲突控制：主会话正在合并上一批 `profiles-mods.csv`，本批未读写该文件；已覆盖 token 集合按上一批三份批次数据重建（155 个 token，另加主表/试译已覆盖的 3582、3401、3317，共 158 个）用于校验。本批 47 个 token 与覆盖集合零交集，未重复已交付词条。

PD-004 排除项：`3249`、`3279`、`3329`、`3347`、`3391`、`3437` 属 UpdateSyncStatus 运行期拼接未决项，本批不裁定、不写入。`3401` 为首批锁定译文，`3582` 已在主表译为“尚无快照。同步后可将真实库存复制到此档案。”，均不重复。

新裁定用语：`Warbonds=战争债券`、`Superstore items=超级商店物品`、`DLC gear=DLC 装备`、`Super Credits=超级货币`、`ARMORY=模组库`、`HELLDIVER 眉标=HELLDIVER 副本档案`。本批字符串只涉及前四项中的前三项（4566）；`Super Credits`、`ARMORY`、`HELLDIVER` 不出现在本批，等待主会话合并时按裁定应用。

## 2 产出与统计

分两批追加写入同一 CSV：批 A 18 条（UpdateSyncStatus 余留 2 条、UpdatePlaySync 16 条），批 B 29 条（Sync* 25 条、共享括号 1 条、方法内补充 3 条）。合计 47 条。

| 项目 | 数量 | 说明 |
|---|---|---|
| 新增词条 | 47 | token 唯一，与上一批已覆盖集合零交集 |
| 已译 | 41 | 含接缝、状态词与失败/进度说明 |
| 待裁定 | 6 | AS-01 4 条、AS-02 2 条，见第 4 节 |
| 方法覆盖 | 10 个 | UpdateSyncStatus、UpdatePlaySync、SyncStartingText、SyncNotStarted、SyncRefusal、RefreshSync、WatchSyncProgress、SyncFailed、OpenGameForSync、`<StopSyncForCloseAsync>b__0` |
| 台账归属 | 档案 43 条 + 方法内补充 4 条 | 43 条来自上一轮档案余留；4 条为同方法内可见片段（6669/6621/6627/1127） |

## 3 原文、定位与空格核对

| 检查项 | 结果 | 说明 |
|---|---|---|
| 原文逐字一致 | 通过 | 47 行按 token 反推 us，与 `us_all.tsv` 同 us 记录逐字比对，0 处差异 |
| token 一致 | 通过 | 全部满足 token = 0x70000000 + us，无重复 token |
| 定位可回溯 | 通过 | 47 行 `方法@IL` 均在 `ldstr_refs.tsv` 中存在 (us, 方法, IL) 记录 |
| 覆盖冲突 | 通过 | 47 个 token 与上一批 158 个已覆盖 token 无交集 |
| 首尾空格 | 通过（1 处已说明） | 16 条含首/尾空格：12 条已译行接缝逐字一致，1 条（4566）尾空格由全角逗号承接，另 3 条为待裁定行（译文留空）；脚本比对除 4566 外 0 处不匹配 |
| 运行期接缝 | 通过 | 5960、8582、8610、9606、95166 保留 ASCII 冒号+尾空格；6539、6635、7288、7575 保留尾空格；6591 保留前后空格；括号由 3984/6591/1127 配对 |
| 引号与省略号 | 通过 | 正文全角标点；5648 的 `...` 改中文六点“……” |
| 重复与漏译 | 通过 | 无重复 token；已译行无空译文；待裁定行译文留空并挂 AS 编号 |

接缝说明（本轮唯一结构性调整）：4566 原文以连接词 `and ` 收尾，后接 4923（“asks for administrator access”）或 4983（“the first time asks…”）两个分支。译文 4566 以全角逗号收尾，连接词“并”并入 4923（“并请求管理员访问权限”），4983 直接从“首次会要求……”起句；因此 4566 不再保留原尾空格，接缝语义由全角逗号与 4923 的“并”承担，其余 13 条已译接缝逐字保留空格。

其他片段处理：3984“上次同步（”与 1127“）”配对为全角括号；6591“ （游戏已打开 ”、6621“否”、6635“，采集完成 ”、6627“是”、1127“）”拼成“ （游戏已打开 否，采集完成 是）”。7288 后接 `proxy.log` 文件名与共享句点片段 7356（未译，被多处复用），最终显示为“请查看 proxy.log.”，ASCII 句点来自共享 token，未改动。

## 4 待裁定（AS-01 起）

### AS-01 premium content

| 字段 | 内容 |
|---|---|
| 类型 | 术语 |
| 关联条目 | us=4016（token 0x70000FB0，`UpdatePlaySync@191`，偏移 420680）、us=4277（0x700010B5，`@204`，420941）、us=5205（0x70001455，`@281`，421869）、us=5293（0x700014AD，`@330`，421957） |
| 原文 | Your premium content stays locked in the game until you sync with this one. / Your premium content stays locked in the game until you sync again. / Your premium content is not in this profile / Premium content you owned … |
| 语境 | 游戏开始页的同步状态卡与档案同步说明，描述尚未同步或同步到错误账户时，游戏内已购买/已解锁内容处于锁定状态；同段列举战争债券、超级商店物品、DLC 装备、超级货币。 |
| 候选 | A 付费内容；B 高级内容；C 已购内容；D 保留 premium content |
| 候选区别 | A 与本应用语境最贴合（指已购买或已解锁的内容，不限于购买）；B 贴近 premium 字面，但易与游戏内“高级战争债券”等既有称谓混；C 只覆盖购买、漏掉解锁；D 在中文句中突兀且与已有中文说明混排。 |
| 建议 | A“付费内容”；本批 4 行译文暂空，待裁定后回填。 |
| 理由 | 非游戏专名，但官方简中口径未核对，且该词是 4 条状态文案的成句关键；先登记避免主会话合并后前后不一致。 |
| 状态 | 待裁定 |

### AS-02 同步卡日期句的片段语序

| 字段 | 内容 |
|---|---|
| 类型 | 拼接语序 |
| 关联条目 | us=5347（token 0x700014E3，`UpdatePlaySync@338`，偏移 422011）、us=5381（0x70001505，`@345`，422045）；前后为 5293（AS-01）与 5389（已译） |
| 原文 | "Premium content you owned " + "at the last sync" + "on " + {日期} + " is unlocked. Bought or unlocked something since? Update the sync to bring it in." |
| 语境 | 同步状态卡成功态说明：上次同步时拥有的付费内容已解锁；片段顺序由运行期拼接固定，不能跨片段重排。 |
| 候选 | A 保持片段顺序：“你拥有的付费内容 在上次同步时于 {日期} 已解锁。”（“在…于…”略叠但可读）；B 把“你拥有的”移到日期之后（跨片段移动信息，违反既有规则）；C 时间片段改括注：“（上次同步时间 {日期}）”并相应改 5347/5381 与 5389。 |
| 候选区别 | A 改动最小、与规则兼容，但读感略生硬；B 最自然但必须跨片段重排；C 可读性最好，需改写 3 个片段且会改变括号风格。 |
| 建议 | 先用 A 兜底；若实机读感差，再评估 C。本批 5347/5381 译文暂空，5293 挂 AS-01、5389 已按“ 已解锁。…”译出，待 AS-02 定后可直接拼接。 |
| 理由 | 片段顺序固定，自然中文需要把“拥有的”放在日期之后；在规则内只能接受轻微叠词。 |
| 状态 | 待裁定 |

## 5 排除与剩余范围

本批排除的内容：

- 纯 Linux 分支：`5728`“Starting the native capture and the Linux helper...”（Windows 首版排除 Linux 辅助程序状态），不译不改写。
- 共享/技术片段：`3275`（“g”，时间格式符）、`7268`（`proxy.log` 文件名）、`7356`（共享句点，被多处复用，未改动）——仅在已译句中按原样引用。
- PD-004 未决项：`3249`、`3279`、`3329`、`3347`、`3391`、`3437`（运行期拼接语序待裁定，沿用共享 PD-004，不在本批另立编号）。
- 已覆盖：`3401`（试译锁定）、`3582`（主表已译）。
- 数据键：`125646` IsDev、`125658` Detail。

剩余范围统计：上一轮档案余留 54 条中，本批处理 43 条，余 11 条——UpdateSyncStatus 8 条（PD-004 六片段、锁定 3401、主表已译 3582）、Sync* 1 条（5728，Linux 专属）、属性名数据键 2 条（IsDev、Detail）；另有 3275、7268、7356 三条技术/共享片段未纳入。上一轮余留的 UpdatePlaySync 16 条与 Sync* 可译部分本批已全部覆盖，无遗漏的账户同步可见状态文案。

## 6 假设与限制

- “DLC 装备”按既有中英文空格规则写作“DLC 装备”（裁定词为“DLC装备”），如主会话统一要求无空格，可在合并时全局替换，不影响其它词。
- `premium content`、拼接日期句两处存在实质取舍，按规则转 AS-01/AS-02，未自行定稿；其余状态、进度、失败与引导文案均按明显可译处理。
- 未提供可运行构建与截图：同步卡文案的实际换行、括号显示、共享句点 7356 在中文句末的观感未实机验证；`admin` 权限提示为系统弹窗，与文案显示先后关系待实机核对。
- 游戏内报错与文件名（`proxy.log`、`logs\sync-...`、`steam://rungameid/553850`）保持原样；`Easy Anti Cheat` 相关文案不在本批。
- 未读写 `profiles-mods.csv` 及其元数据；覆盖校验通过重建上一批批次数据完成。未修改其它输出、未联网、未启动程序、未改 Git。

## 7 交付文件

| 文件 | 内容 | 校验 |
|---|---|---|
| `launcher-0.4.0-beta-zhcn/modules/account-sync.csv` | 47 条：41 已译、6 待裁定；字段 token,method_il,original,translation,status,context,decision_id；UTF-8 带 BOM、CRLF | 原文/token/定位/空格/覆盖冲突/重复全部通过 |
| `launcher-0.4.0-beta-zhcn/modules/account-sync-review.md` | 本文件：范围、批次、核对、AS-01/AS-02、剩余范围 | — |
