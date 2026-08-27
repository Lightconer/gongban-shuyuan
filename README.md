# 合规公版书源（GongBan ShuYuan）

一个**只收录公有领域 / 开放许可内容**的阅读 App 书源项目，自带「自动校验 → 自动更新 → 自动部署」流水线（GitHub Actions + GitHub Pages），**国内网络可直接使用**。

## 合规声明（重要）

本项目**不含**盗版站点、付费墙绕过、需要登录或验证的内容，也**不含成人内容**。
书单与书源规则只指向一个合规来源：

- **Project Gutenberg（www.gutenberg.org）**：公有领域电子书（含中文公版典籍，四大名著、诸子、史记、鲁迅等 30 部），免登录、免费，**国内网络可直接访问**。

自动校验脚本只做「内容可达性与有效性」检查，不解析任何受版权保护的内容。

## 项目结构

```
gongban-shuyuan/
├── books.json                     # 书单（公有领域作品清单，可自行增删）
├── sources.json                   # 校验结果（自动生成）
├── 书单.md                        # 人类可读的校验清单（自动生成）
├── index.html                     # GitHub Pages 展示页（自动读取 sources.json）
├── 书源/
│   └── Gutenberg_公版中文书.json   # 阅读 App 书源（国内可达）
├── scripts/
│   └── validate.py                # 自动校验脚本（纯标准库，零依赖）
└── .github/workflows/
    └── update.yml                 # GitHub Actions：定时校验→更新→部署
```

## 本地使用

```bash
python scripts/validate.py
```

- 生成 `sources.json`（机器可读）与 `书单.md`（带状态标记）
- 无需安装任何第三方库（仅用 Python 标准库）

## 在阅读 App 中使用

1. 导入书源：
   - **网络导入**：书源管理 → 右上角菜单 → 网络导入，粘贴书源 JSON 直链：
     `https://<用户名>.github.io/<仓库名>/书源/Gutenberg_公版中文书.json`
   - 或直接在 App 内搜索「红楼梦」「论语」等书名。
2. 打开书后点 **Plain Text UTF-8**，进入纯文本在线阅读。
3. 规则为 v0.1：个别书籍结构特殊时，可在书源管理里微调 `ruleToc.chapterList` / `ruleContent.content`。

## 部署到 GitHub（自动更新 / 自动校验 / 自动部署）

1. 新建一个 **Public** 仓库，把本项目全部文件推送上去。
2. 开启 Pages：仓库 **Settings → Pages → Source** 选择 **GitHub Actions**（不要选 Branch）。
3. Actions 工作流 `update.yml` 会：
   - **每天 10:30（UTC+8）自动运行**（cron `30 2 * * *`，可自行修改）；
   - 运行 `scripts/validate.py` 自动校验每本书的可达性与有效性；
   - 状态有变化时**自动提交并推送**；
   - 自动**部署到 GitHub Pages**。
4. 也可以到 Actions 页面手动点 **Run workflow** 立即触发一次。

> 说明：`git push` 使用仓库自带的 `GITHUB_TOKEN`，无需额外配置密钥。

## 如何增删书单

编辑 `books.json` 的 `books` 数组，`url` 填入 Gutenberg 上公有领域作品的页面地址即可，例如：

```json
{ "title": "红楼梦", "site": "gutenberg", "url": "https://www.gutenberg.org/ebooks/24264", "category": "四大名著" }
```

## 许可

- 项目脚本与配置：MIT（可自由使用、修改）
- 书单指向的文本内容：公有领域或按 Gutenberg 的授权条款

> 使用本项目的书源读取内容时，请自行遵守对应来源站点的服务条款与当地法律法规。
