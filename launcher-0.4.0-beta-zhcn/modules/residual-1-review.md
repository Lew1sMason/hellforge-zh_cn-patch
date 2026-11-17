# 残余复核队列（第 1 批）settings 关联合并

处理 `work/residual-review-queue-1.csv` 的 95 条残余候选，属 Windows 启动器全量范围收尾。队列 `class=可见` 仅为按方法初判，本批逐条按原文语义与 `ldstr_refs` 调用点复核后再定去向。只写 `modules/residual-1.csv` 与本文件；上轮 settings/settings-followup、其他模块文件与主表未改动。

## 1 判据与去向

判据：写入显示控件、对话框、状态区或用户可读控制台行的文本才处理；控制名、样式键、数据键、路径、格式占位符、纯 Linux 文案、第三方资源与独立帮助文档不在范围内。队列 95 条逐条核对后：

| 去向 | 条数 | 说明 |
|---|---|---|
| CSV 已译 | 91 | 含真对话框（信任模组、崩溃转储）、模组页文案、安装/卸载提示、状态区、导入复核等 |
| CSV 待裁定 | 1 | R1-01（Premium items） |
| CSV 保留 | 1 | 产品名片段 `HellForge ` |
| 待查（无 CSV 行） | 2 | 证据不足，见第 2 节，不强行判定为可见/已译 |
| 排除 | 0 | 队列已预筛，本批未发现应由其他类别排除的项 |

队列 95 个 token 全部有去向：93 个在 CSV，2 个在待查清单；CSV 不含队列外 token。

| status | 条数 |
|---|---|
| 已译 | 91 |
| 待裁定 | 1 |
| 保留 | 1 |

## 2 待查（缺证据，保留待查）

| token | 方法@偏移 | 原文 | 理由 |
|---|---|---|---|
| 0x7001659E | `<>c.<UpdateImportControls>b__6_0@32` | ` — before ` | 同闭包 @17 只取日期格式符 `g`，可佐证是「时间后缀」，但前导文本与所写控件不在字符串堆内可见，无法判断是导入控件说明还是工具提示；不改写、不判定 |
| 0x70005CDF | `HellForge.Launcher.MainWindow.Refresh@10` | `Launcher status error: ` | `Refresh` 方法内没有其他显示字符串，无法区分状态栏提示与内部日志前缀；队列原判为待查，本批维持 |

## 3 疑难

### R1-01 Premium items

| 字段 | 内容 |
|---|---|
| 类型 | 术语 / 已确认术语边界 |
| 关联 | us=67123，token 0x70010633，`<InitializeAccountImport>b__4_2@13`，偏移 483787；原文 `Nothing imported. Premium items you own still follow the sync.` |
| 语境 | 账户导入结束后的提示，说明没有导入文件时，已拥有的付费类物品仍随同步更新；`BuildReview` 中 premium 与 warbonds 是两个并列分类 |
| 候选 | A 高级物品；B 超级商店物品；C DLC装备；D 保留 Premium items |
| 差别 | A 为泛称，安全但信息弱；B/C 绑定已确认术语，但会收窄语义（premium 不限于超级商店或 DLC，且与 BuildReview 的独立分类不一致）；D 与整句中文混排 |
| 建议 | A（高级物品）。待主控结合 BuildReview 的 premium/warbonds 分类关系最终确认；若定 B/C，本行同步替换 |

## 4 术语与格式处理

已确认术语按队列要求落用：主机（host）、档案（profile）、模组、模组库（mods folder）、会话、超级货币（Super Credits）、开始菜单（与设置页「开始菜单快捷方式」一致）、返回（与锁定译名一致）、PLAY→「开始游戏」、`HellForge-Setup` 保留英文。第三方模组名 `Stratagem Compendium` 保留英文；Steam 术语 `depot` 保留英文；Discord 支持行保留 URL 原文。

拼接与空格：

- 38 条片段含首或尾空格（首空格 26、尾空格 24、两端 12），均按原文逐字保留（含下述两处前导空格）。
- 括号对：HF-93782/HF-93806（`is built (… KB);`）与 HF-95971/HF-96069（`mods (…);`）两对括号的左右段都在本队列，统一改全角；HF-35243 与 HF-94806 的后半括号不在本队列或为共享 ASCII ` MB/s), `，保留 ASCII 左括号以免跨模块错配。
- 行首格式：三条卸载计划行保留「  - 」前缀与 ASCII 冒号加尾空格（如「  - Steam 的 depot 下载内容（未勾选 Steam 选项则保留）： 」）。
- 保留前导空格两处：HF-50599（原文 ` through the game.`）、HF-35706（原文 ` permanently: the mod's files`）均以 ASCII 空格开头，后接中文逗号；按项目规则保留该前导空格，不因中文标点删去，译文相应写作 ` ，…`，context 已同步说明；其余片段首尾空格未动。
- 运行期值位置未动：信任说明中的接受信任方名称、构建体积、下载速度、路径、异常详情等均按原片段边界拼接。

## 5 QA 与边界

- 队列 95 条逐条核对：原文取自 `work/us_all.tsv` 的 `#US` 堆逐字回填；每行 `method_il@偏移` 在 `work/ldstr_refs.tsv` 中找到同 us 的调用点且堆文本一致；token 由 us 推导核对（`0x70000000 | us`）。
- 覆盖校验：95 = 93（CSV）+ 2（待查），无未去向、无队列外 token。
- 重复校验：与 `zh-cn-master.csv`、`settings.csv`、`settings-followup.csv`、`launch-errors.csv`、`console.csv`、`profiles-mods.csv`、`account-sync.csv` 均无重复 token。
- 格式：CSV 回读逐字一致，UTF-8 带 BOM，七列固定为 token、method_il、original、translation、status、context、decision_id；93 行 token 唯一；待裁定行译文为空且编号存在；保留行译文非空。
- 边界：未运行程序，未联网，未接触输入副本、源安装与 Git；临时校验脚本与数据已删除。

假设：`Premium items` 暂按「高级物品」待定（R1-01），`host` 取「主机」与既有设置页译文一致；两处待查 token 维持原样，待后续有调用点或界面证据再处理。
