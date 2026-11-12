# 花瓣航迹（Petalwake）— 本地完整中文复刻版

原作：[Petalwake](https://petalwake.non.io/v2/)（https://petalwake.non.io/v2/）
复刻方式：整站镜像（全部 192 个文件，含 152MB 资源），随后将全部界面文本翻译为简体中文。

## 启动

```bash
python3 -m http.server 8765
# 打开 http://127.0.0.1:8765/
```

必须通过 HTTP 访问（ES modules + fetch 资源），不能用 file:// 直接打开。

## 玩法

骑扫帚在小岛上空飞行：
- 收集 **38 枚风种**（左上角计数，指南针指向最近一枚）
- 寻找 **12 处宝藏**（按 `J` 打开手记查看线索）
- 递送包裹：跟随右上角金色指南针，在塔台旁连按两次 `Space` 降落
- 收集 10 枚风种后解锁特技「踢翻身」（按 `Q`）

按键：`W/S` 俯冲·爬升 · `A/D` 转向 · `Shift` 乘疾风 · `Space` 缓速 · 鼠标转向 · `C` 镜头 · `I` 反转俯仰 · `P` 隐藏界面 · `M` 静音 · `J` 手记

## 翻译范围

- 标题屏 / HUD / 按键说明（index.html）
- 加载文案、提示 toast、地名（src/main.js）
- 快递任务、降落提示、特技解锁（src/game/*.js）
- 手记 / 宝藏发现卡（src/ui/journal.js）
- 相机模式名（src/player/camera.js）
- 距离单位（米 / 千米）（src/game/hud.js）
- 12 处宝藏的名称、线索与传说（assets/places/*.json）
- 3 座城镇与全部 35 个降落点名称（assets/town/*.json）
- CSS 增加中文回退字体（苹方 / 宋体）

游戏标题意译为「花瓣航迹」（Petal = 花瓣，wake = 航迹）。地名译名表见 git 提交历史（原版快照 `169f7d4`，翻译提交 `86b7094` 及之后）。

## 目录

- 仓库根目录即游戏本体（镜像 + 中文翻译），可直接作为 GitHub Pages 站点发布
- `scripts/` — 镜像与翻译辅助脚本（mirror.py / assets.py / translate_assets.py / translate_treasures.py）
