# HANDOFF（2026-11-18）

交接给新会话。只读本文件与所列文件即可继续，不要重新搜索已核实内容。

## 工作区与授权

| 项目 | 内容 |
|---|---|
| 仓库根 | `E:\CN Translations\HellForge_ZH-CN\DS-TranslationWorkspace` |
| 任务说明 | `E:\CN Translations\HellForge_ZH-CN\hellforge-zhcn-pm-prompt.md` |
| 可写范围 | 仅 `DS-TranslationWorkspace`；翻译、术语、语校、文档由 DeepSeek 完成，负责人负责构建与实测 |
| 禁止 | 不写源安装 `E:\HD2Modified\HellForge`，不用指向源目录的软链接，不联网，不改原生程序 |
| 异常 | DeepSeek Messages transport failed 时在同一会话续做，不另起炉灶 |

当前没有新翻译任务在跑，未改任何译文或预览副本。四张最新截图来自上一会话用户，未另存，新会话不假设可见；下面从图中读出的说明足够继续，必要时再请用户提供原图。

## 当前状态

Windows 启动器 0.4.0-beta，提交 d8a8b46。Git 仓库在仓库根，基线 `ae5c4e2` 生成首个可运行预览，`bca80cb` 保存昨日细化清单。Git 若报 ownership，用单命令 `-c safe.directory=该仓库绝对路径`。

预览入口 `preview-0.4.0-beta-zhcn/app/launcher/HellForge.Launcher.exe`。预览已复制独立游戏 22.20 GiB，迭代不再复制。EXE 与原版 SHA-256 相同且均未签名，简中在预览同目录 DLL。已实测配置页与启动主界面可打开并显示中文，正常游戏未启动验证。

主表 791 行，已译 762、历史锁定 16、保留 13、待裁定空译 0；779 个回填调用点，3236 条 IL 字符串已比对。361 条候选未逐一判定，不能算作漏译。

## 核心文件

| 文件 | 用途 |
|---|---|
| `launcher-0.4.0-beta-zhcn/zh-cn-master.csv` | 原译对照主表 |
| `launcher-0.4.0-beta-zhcn/modules/sync-callpoints.csv` | 作用域覆盖记录，名字含 sync 但可写多类经核验的调用点 |
| `launcher-0.4.0-beta-zhcn/pending-decisions.md` | 待裁定与已关闭记录 |
| `launcher-0.4.0-beta-zhcn/preview-refinement.md` | 细化清单 RF-01 至 RF-14 |
| `launcher-0.4.0-beta-zhcn/STATUS.md` | 造包与实测状态 |
| `work/ldstr_refs.tsv` | 方法@IL 与字符串引用 |

## 操作规程

按 token 加方法@IL 分别回填，同一共享串语义相同的调用才复用；禁止全局替换，不改数据键、文件名、路径。组装片段先核对最后整句，再验证显示。提交前核对锁定样本、未涉及原件与实际预览。构建用 `python work/build_launcher_preview.py`；已验证 `work/smoke_launcher_preview.ps1` 可在预览副本执行。人工重点看页签，不触发修复、卸载、同步或游戏启动。若用户正在运行预览，不要关窗口，先确认是否影响 DLL 更新。

## 今日四图待办（尚未实施）

**图 1 设置 → 安装。** `Check and repair` 应为「检查并修复」，锁定译文在 `!XamlIlPopulate@4229`，截图处是 `!XamlIlPopulate@21340`。另核实 `EnterSetup@303` 与 `@329` 是否为重设标签。

**图 2 设置 → 银河战争 → 所有行星开放。** HF-84302，`!XamlIlPopulate@27597`。对照正式原文重写生硬段落，说明对应战线划分玩家阵营持有的行星、每阵营约占银河三分之一、子阵营与 SEAF、Megafactories，以及无需联网、下次会话生效；细节严格依 CSV 英文源文。Super Earth、Predator Strain、Jet Brigade、SEAF、Cyberstan 等专名留到下一轮集中确认，需先查证官方词，不杜撰。

**图 3 设置 → 路径。** `Session runner` 应为「会话启动程序」，补 `BuildPaths@56`（原来只 `StartPreflight@63`）。`Open session logs` 应为「打开会话日志」，补 `!XamlIlPopulate@30208`（控制台 `@19710` 已译）。PD-006 标签位置已由截图证实，修复后复测。

**图 4 模组页。** 保留 ARMORY→「模组库」与大标题「模组」。计数仍显示 `3 / 3 mods 已开启`。`ModsSummaryText@78` 的 `of` 已译，缺 `@98` 的 0x70009B61（同 token 的 `AddModSyncCard@2194` 已译）；`@114` 复数 `s` 只在明确中文调用点移除，`@133` 配合组成「3 / 3 个模组已启用。」。附带复核 `RefreshMods@484/501` 的玩法模组计数，其他引用不要批量改。

用户明确要求「外观包」改「外观模组」，涉及 HF-41326、HF-38863、HF-46289、HF-110788 的可见文案，不改文件格式或数据键。内置模组名称与描述属清单元数据，是否纳入待范围确认，不假定用户要改。

昨日三项顺手列入下一轮：RF-01 PLAY 的 `UpdateButton@51`；RF-02 Running 的 `.cctor@53` 与 `ShowObserving@217`；RF-03 INSTALLATION 的 `!XamlIlPopulate@31196`。均从已确认译名出发。

## 交付优先与完成条件

先做图 1 至图 4 与昨日三项中可复现的可见项，再处理待核；不改未确证位置。完成条件是预览重建后逐项显示中文、无截断，锁定样本未变，重建仅改预览 DLL，且原安装保持只读。难词集中登记，一轮结束请用户最终裁定，不中途追问。请勿推进上述待办，等新会话按本文件执行。
