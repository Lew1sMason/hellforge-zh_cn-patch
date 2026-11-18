# launcher-0.4.0-beta-zhcn 工作目录说明

本目录存放 0.4.0-beta 构建简体中文汉化的活动产出。输入副本在 `launcher-0.4.0-beta-input/`，只读；试译基线在 `work/trial-entries.csv`，只读。分析中间文件留在 `work/`，本目录只放可交付、可分批维护的文件。

## 文件

| 文件 | 作用 | 维护方式 |
|---|---|---|
| `zh-cn-master.csv` | 原译对照总表，交付主件 | 只追加行，锁定行不改 |
| `pending-decisions.md` | 待裁定清单，稳定编号 PD-xxx | 只追加，已关闭项保留并标状态 |
| `inventory/scope-inventory.csv` | 全量范围盘点台账 | 追加或改状态，不删行 |
| `inventory/inventory-summary.md` | 台账按模块与状态的统计 | 每次合并后重新生成 |
| `STATUS.md` | 当前进度、接续点、验证记录 | 每批更新 |

## BAT 拖拽安装与卸载

适用于 Windows 版 HellForge Launcher `0.4.0-beta`（`d8a8b46`）。使用补丁目录里的 `app`，也可直接用旧版拖拽 ZIP 解压后的 `payload/app`。

1. 在记事本中分别复制两段源码，另存为 `install.bat` 和 `uninstall.bat`。文件类型选「所有文件」，编码选 ANSI。两个 BAT 放在补丁目录根部，与 `app` 或 `payload` 同级。[安装 BAT 源码](installer/batch/install.bat) · [卸载 BAT 源码](installer/batch/uninstall.bat)
2. 关闭 HellForge，将包含 `app` 的 HellForge 安装目录拖到 `install.bat` 上。脚本将准备覆盖的两份 DLL 和一份 JSON 备份到补丁目录的 `backup/app`，校验后执行覆盖。显示 `Install OK.` 即完成。
3. 卸载时关闭 HellForge，将同一安装目录拖到 `uninstall.bat` 上。保留同一目录下的两个 BAT 和 `backup`。显示 `Uninstall OK.` 即恢复完成。

如果脚本提示 SHA-256 不匹配，请先检查安装版本、补丁文件或备份。更新补丁时，同步校对 [manifest.json](installer/manifest.json) 和安装 BAT 中的 SHA-256。

## 主表字段

`item_id` 为 `HF-` 加 `#US` 堆偏移，同一构建内稳定。`token` 为 `0x70000000+us_index`。`locator` 为方法名加 IL 偏移，用于定位运行期引用点。`file_offset` 为字符串记录在 DLL 内的字节位置，长度前缀所在处。`pending_id` 只在待裁定行为空译时填写。

状态取值如下。

- `锁定` 阶段 3 已确认的 15 条试译与 1 条共享格式，原样保留，不得改写。
- `已译` 本批新译，可审可改。
- `待裁定` 译文留空，必须关联 PD 编号。

## 空格与格式

原文与译文中的首尾空格是拼接语义的一部分，CSV 里保存真实空格，不在单元格里加标记。检查时按字节比对 `work/us_all.tsv`。`01   PLAY` 这类导航保留两位编号与编号后的三个空格。ASCII 冒号加空格的分隔片段（如 `": "`、`Could not save the logs: `）按锁定样本先例原样保留。

## 追加规则

新增行写入主表末尾，按模块与 us 排序后再提交。同一 us 只保留一行，重复出现时以主表已有行为准。新模块先落台账，再补主表。术语变更先改 `pending-decisions.md` 或术语表，再回查相关行，不做全库字符串替换。

## 合并

独立会话按模块产出的草稿文件在 `modules/` 下（由负责人统筹），合并进主表时保留其 `item_id` 与来源定位，逐条复核原文与空格后再改状态。合并前不改动锁定行。
