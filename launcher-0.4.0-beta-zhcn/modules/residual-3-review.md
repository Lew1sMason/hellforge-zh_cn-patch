# 余留第三批（queue-3）审校记录

本批只处理 `work/residual-review-queue-3.csv` 的 94 条余留候选，产出 `modules/residual-3.csv`。未改动 `residual-ledger.csv`、`residual-ui.csv`、`residual-review.md`、主表与其他模块文件；未合并总表、未运行程序、未访问 Git 或网络。字段与模块表一致：`token,method_il,original,translation,status,context,decision_id`。

**假设（一行）**：`AppendSteamRemovals` 的 11 行属 Windows 设置页卸载警告清单（依据同页 XAML 控件 `UninstallSteamBox`、`UninstallSteamPaths` 与 MainWindow 方法），若实为 Linux 专属需改判。

## 1 计数与去向

94 条逐条有去向。

| status | 条数 | 说明 |
|---|---|---|
| 已译 | 85 | 写入 `residual-3.csv` |
| 待裁定 | 7 | 译文留空，挂 R3-01/R3-02，草案见第 3 节 |
| 保留 | 1 | `depot ` 技术前缀，原样保留 |
| 排除 | 1 | `--mod` 命令行参数 |
| 待查 | 0 | 本批无需保留待查项：94 条的证据链均可归入以上四类 |

方法数 34 个；原文含首/尾空格的 38 条，译文按原边界保留（唯一例外见第 4 节）。处理前复核队列与主表、六个模块 CSV 的 token 无重叠（0 条重复）。

## 2 调用点核对（方法级）

队列的「可见」只是按方法初筛，本批逐条回到 `work/ldstr_refs.tsv` 核对方法内 IL 与同方法相邻片段，并以同方法已被主表/模块翻译的片段作先例。

| 方法组 | 条数 | 调用点结论 |
|---|---|---|
| `AppendSteamRemovals` | 11 | 设置页卸载警告清单行；XAML 有 `UninstallSteamBox`/`UninstallSteamPaths` 控件，属 Windows 卸载文案。行首 `  - `、尾空格、`content/app_` 路径片段保留 |
| `MainWindow..cctor` | 10 | 配置步骤名与状态词静态字段；同方法相邻 `Running` 已被主表译为“运行中”，确认界面可见 |
| `PremiumText`、`PremiumTag` | 7+3 | 高级内容面板与标签；同组其他说明文案已按界面文本处理。其中 Premium 术语未定 4 条转 R3-02 |
| `ShowObserving`、`ShowState`、`PlayClicked`、`ServeCoopRelays`、`WarnIfGameStillOpen`、`AccountCheckNote`、`Cleanup` | 6+1+1+1+3+1+1 | 启动/同步状态区文本；相邻片段 `Running`、`Waiting for Steam...`、`Approve the Windows prompt…`、`yes`、`Inventory sync failed: ` 等均有主表译文，确认可见。含 STOP 的 3 条转 R3-01 |
| `OfferCrashReport`、`SaveCrashReport` | 4+4 | 崩溃提示与保存结果；相邻 `)`、` (`、` files in use were left out)` 已有主表译文，确认可见 |
| `AddMods`、`PickMods`、`ZipItem`、`ZipMod`、`ShowModBuilds`、`BuildItem`、`InstallModTools`、`AddModSyncCard`、`ModSyncRow`、`Details` | 4+3+4+1+3+3+2+1+1+1 | 模组页/文件对话框/进度提示；同方法相邻 `Not added: `、` of `、`you have it` 等已有译文，确认可见 |
| `SyncAccountAsync`、`InitializeAccountImport`、`InitializeSettingsImport`、`ReportStartFailure` | 3+2+2+2 | 账户同步与导入状态/错误；同方法 `Imported into `、`capture did not start: ` 等已有译文，确认可见 |
| `ApplyStrangersSetting`、`CheckFilteringEngine` | 2+1 | 设置页说明与 Windows BFE 服务错误，界面可见 |
| `ShowDepotProgress` 闭包 | 1 | depot 进度行前缀，属可见文本但为技术名词，按“保留”处理 |
| `<>c__DisplayClass256_0.<BuildMod>b__0` | 1 | 相邻文本均为 native Linux build agent 与命令行，`--mod` 是构建代理参数，改判排除 |

逐条核对后与初筛的差异：1 条改排除（`--mod`），1 条改保留（`depot `），7 条因术语/按钮名未定转待裁定，其余 85 条按 Windows 界面文案翻译。

## 3 R3 疑难（2 项，7 条）

### R3-01 STOP 按钮标签

| 字段 | 内容 |
|---|---|
| 类型 | 按钮名口径 |
| 关联 token | 0x70006A8B、0x70006BC6、0x70006D2D（`ShowObserving`） |
| 原文 | `…Press STOP or close the game to end the session.` / `…Press STOP, then PLAY again: the next launch goes through.` |
| 语境 | 启动观察状态提示，指导用户按界面按钮 STOP / PLAY。PLAY 已被主表定为“开始游戏”，STOP 尚无定稿译名（`UpdateButton` 的 `STOP`、`STOPPING` 仍未处理）。 |
| 候选 | A：按钮名译“停止”，句中写“按‘停止’”；B：句中保留 `STOP`；C：改写为“停止会话或关闭游戏”。 |
| 候选区别 | A 与 PLAY 的口径一致，但需与按钮标签同时定稿；B 保留英文与括号内混排；C 绕开按钮名但丢失“按钮在哪”的信息。 |
| 建议 | A，待 `UpdateButton` 的 STOP 定稿后统一回填；若按钮保留英文则改 B。 |
| 草案 | 0x70006A8B：`在此期间游戏窗口会一直黑屏。之后的启动会很快。按“停止”或关闭游戏即可结束会话。`；0x70006BC6：`新安装首次启动时可能出现这种情况。请按“停止”，再按“开始游戏”：下一次启动会正常通过。`；0x70006D2D：`按“停止”或关闭游戏即可结束会话。` |
| 状态 | 待裁定（译文留空） |

### R3-02 Premium 术语

| 字段 | 内容 |
|---|---|
| 类型 | 术语 |
| 关联 token | 0x7000B5F1（`PremiumText`）、0x7000B569、0x7000B589、0x7000B5A9（`PremiumTag`） |
| 原文 | `Premium items are checked against the signed-in Steam account when the session starts.` / `PREMIUM` / `PREMIUM: LOCKED` / `PREMIUM: CHECK AT SESSION` |
| 语境 | 高级内容面板与模组/物品标签，指战争债券、超级商店物品等付费内容；主表已有多条 `premium content` 待裁定行，尚未定名。 |
| 候选 | A：高级（高级物品 / 高级：已锁定 / 高级：会话时检查）；B：付费；C：保留 `PREMIUM` 英文。 |
| 候选区别 | A 与“高级内容”语感一致但不暗示必须付费；B 直白但可能误伤通过同步获得的內容；C 与界面其他标签风格不一致，且需同步改主表待裁定行。 |
| 建议 | A，并与主表 `Your premium content is not in this profile`、`Premium content you owned ` 等待裁定行一并定稿。 |
| 草案 | 0x7000B5F1：`高级物品会在会话开始时对照已登录的 Steam 账户进行检查。`；0x7000B569：`高级`；0x7000B589：`高级：已锁定`；0x7000B5A9：`高级：会话时检查` |
| 状态 | 待裁定（译文留空） |

## 4 排除与保留

| token | 原文 | 处理 | 理由 |
|---|---|---|---|
| 0x70016D58 | `--mod` | 排除 | `BuildMod` 闭包中的构建代理命令行参数；相邻字符串均为 native Linux build agent 相关，非界面文案 |
| 0x7001667C | `depot ` | 保留 | Steam depot 进度行前缀，depot 为 Steam 技术术语；与 SteamCMD、Steam broker 同类保留英文，不改写 |

**待查 0 条。** 本批每条都能给出调用点结论；未把“无法证实”的条目塞进排除。

## 5 术语与拼接处理

### 5.1 术语（沿用已定稿与既有译文）

| 原文 | 处理 | 依据 |
|---|---|---|
| PLAY | 开始游戏 | 主表 `PLAY`→开始游戏 |
| network block | 网络阻断 | 主表多条已译 |
| inventory sync | 库存同步 | 主表 `Inventory sync: …`、`Inventory sync failed: ` |
| capture | 采集 | 主表 `capture did not start: `、`capture taken ` |
| sandbox / sandboxed | 沙箱 | 主表 `SANDBOX`→沙箱 |
| Steam broker | 保留英文 | 主表已译段落中保留 `Steam broker` |
| Steam Input | Steam 输入 | 主表 Windows 沙箱说明 |
| cosmetic packs | 外观包 | 主表 `cosmetic pack` 相关行 |
| unblock | 取消屏蔽 | 主表 `Unblock`→取消屏蔽 |
| mod tools | 模组工具 | 主表 `MOD TOOLS`、`Install mod tools` |
| 游戏内专名 | cryo pod→冷冻舱；stratagems→战略配备 | 未与官方简中核对，作为草案标记，建议实机或官方词表复核；不阻塞本批 |

### 5.2 拼接边界（38 条含首/尾空格，逐条保留）

| 组 | 拼接形态（`␠`=半角空格） |
|---|---|
| 卸载清单 `AppendSteamRemovals` | 行首 `␠␠-␠` 保留；`…版本␠` + 版本号 + `：仅当…`/`：未找到`；`…content/app_` + `␠文件夹内或旁边:␠` + 路径 |
| `WarnIfGameStillOpen` | `库存同步:␠` + `游戏仍在运行␠` + N + `␠秒（自采集完成起）` |
| `OfferCrashReport` | `游戏崩溃了` + `␠（退出代码␠` + N + `）` + `。…` |
| `SaveCrashReport` | `已将崩溃报告保存到␠` + 路径 + `，包含崩溃转储` + `。…` |
| `AddMods` | `正在添加␠` + 名称 + `...`；`…, 替换已安装的那个`；`␠未添加:␠` + 原因 |
| `PickMods` | `正在读取␠` + N + `␠个文件……` |
| `ReportStartFailure` | `；安全软件:␠` + 列表；`除 Microsoft Defender 外没有其他安全软件，或未询问` |
| `ZipItem` | 整段末尾空格保留；`exports 文件夹` 保留英文 |
| `ModSyncRow` | `下载（` + 尺寸 + 既有未译片段 `␠MB)`；**待 0x7000C899 处理时统一为全角右括号** |

边界空格说明：仅 0x7000B747（`'s synced account lacks `）在译文首部**新增**一个空格，因前接运行期档案名、中文“的”前按中英混排留空；其余 37 条按原文首尾空格的增删零差异。`AppendSteamRemovals` 的 `…下载:␠`、`…（清空后）:␠` 等拼接前缀沿用 ASCII 冒号加空格先例。

## 6 机器核对

| 检查项 | 结果 |
|---|---|
| 行数与 token | 通过：94 行，token 与 queue-3 完全一致且唯一，无缺行/多行 |
| 重复与去重 | 通过：与处理时主表及六个模块 CSV 的 token 重叠 0 条 |
| 原文一致 | 通过：94 行原文与 queue-3 及 `scope-inventory.csv` 逐字一致 |
| 定位可回查 | 通过：94 行 `method_il` 均能在 `work/ldstr_refs.tsv` 命中同 token 同方法同 IL |
| 状态与去向 | 通过：已译 85、待裁定 7（均挂 R3 编号且译文留空）、保留 1、排除 1、待查 0 |
| 首尾空格 | 通过：38 条边界空格行按原文保留，0x7000B747 的新增首个空格已在第 5.2 节说明 |
| 编码与结构 | 通过：UTF-8 无 BOM、LF、7 列、末行有换行 |
| 未完成边界 | 明确：7 条等 R3-01/R3-02 结论后回填；其余 87 条已有最终去向 |

## 7 交付边界

只写 `modules/residual-3.csv` 与本文件；未改 `residual-ledger.csv`、`residual-ui.csv`、`residual-review.md`、主表或任何模块 CSV，未改 Git、未运行、未联网。可见性判断仍止于方法与 IL 层级，未实机核对。
