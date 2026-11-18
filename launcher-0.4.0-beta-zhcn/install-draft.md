# HellForge 简体中文补丁安装草案（0.4.0-beta / d8a8b46）

状态：草案。仅确定数据范围、校验清单与安装/恢复流程；本轮未打安装包、未实测安装/恢复，不宣称可安装。预览构建与独立副本验收由负责人执行。

## 目标与范围

面向已安装的 Windows HellForge Launcher 0.4.0-beta（上游提交 `d8a8b46`）的小型离线 ZIP。包内只含三份汉化数据：

| 文件 | 作用 |
|---|---|
| `app/launcher/HellForge.Launcher.dll` | 启动器主界面、设置、模组与安装流程的简中回填 |
| `app/launcher/HellForge.SteamDownload.dll` | Steam 下载卡三种登录方式与说明的简中回填 |
| `app/profile-templates.json` | 新建档案模板描述的简中映射 |

不含游戏本体、Steam、`HellForge.Launcher.exe`、其他 `HellForge.Core` 文件，以及用户档案、存档、日志、缓存；安装与恢复脚本只处理上述三文件。安装过程离线，不联网。

## 包结构（计划）

```
HellForge-0.4.0-beta-zhcn-d8a8b46.zip
  app/launcher/HellForge.Launcher.dll
  app/launcher/HellForge.SteamDownload.dll
  app/profile-templates.json
  manifest.sha256
  install.ps1
  restore.ps1
```

本轮只定稿数据与流程；`install.ps1`、`restore.ps1` 为脚本计划，尚不可执行。

## 校验清单

`manifest.sha256` 采用简单行格式（数值在构建时生成，此处为示意）：

```
version 0.4.0-beta d8a8b46
original app/launcher/HellForge.Launcher.dll <SHA-256>
original app/launcher/HellForge.SteamDownload.dll <SHA-256>
original app/profile-templates.json <SHA-256>
patched  app/launcher/HellForge.Launcher.dll <SHA-256>
patched  app/launcher/HellForge.SteamDownload.dll <SHA-256>
patched  app/profile-templates.json <SHA-256>
```

`original` 为上游原版文件哈希，`patched` 为汉化包文件哈希；安装时两者都要校验。

## 安装流程（计划）

1. 关闭 HellForge 启动器：脚本检测 `HellForge.Launcher.exe` 进程，运行中则提示退出，不自动结束。
2. 显式指定目标根目录：`install.ps1 -HellForgeRoot "D:\HellForge"`；根目录必须存在 `app/launcher/HellForge.Launcher.dll` 等三文件，不自动搜索、不猜路径。
3. 校验目标：三文件当前 SHA-256 必须逐一等于 `original`；任一不符则停止并输出实际哈希，不写入。
4. 校验包：ZIP 内三文件 SHA-256 必须等于 `patched`；不符则停止。
5. 全部校验通过后先备份：把三文件复制到根目录下 `.hfzh-backup\<时间戳>\`，并写入备份清单；备份完成前不改动目标。
6. 写入三文件；任一写入失败，立即用本次备份回滚。
7. 重复执行：目标已是 `patched` 哈希时报“已安装”并退出；三文件状态混杂时停止，提示先恢复或人工核对。

## 恢复流程（计划）

- `restore.ps1 -HellForgeRoot ...` 先校验当前三文件是否仍等于 `patched` 哈希；不是则拒绝覆盖，避免覆盖上游更新或未知改动。
- 校验备份中的三文件等于 `original` 哈希，全部通过后才还原；失败则回滚。
- 恢复可重复执行；已恢复状态（等于 `original`）直接报“未安装补丁”。

## 版本升级/修复后是否仍适用

安装和恢复都以哈希判断，不只看版本号：

| 当前三文件状态 | 判断 |
|---|---|
| 等于 `original` | 原版，可安装 |
| 等于 `patched` | 已安装 |
| 其他 | 不可继续；停止并记录实际哈希。可能是安装失败导致的 `original`/`patched` 混合，或未知自定义改动，不一概归因版本变更；版本升级或修复则等待匹配新版本的补丁 |

若升级或修复替换了这些文件，以哈希判断；旧备份不应再强行覆盖，需重新生成对应版本的三文件与 `manifest.sha256`。

## 待做（本轮不宣称）

- 实现并审查 `install.ps1`、`restore.ps1`，覆盖写入失败回滚、重复执行与恢复前校验。
- 由负责人在独立游戏副本上验收：构建、启动、页签切换、新建档案、计数后缀、下载卡三种登录方式与拼接。
- 安装/恢复演练仅针对独立测试副本；不把真实安装演练列为必做。本轮不宣称已测试或可直接安装。
