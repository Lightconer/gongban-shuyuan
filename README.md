# 合规公版书源（GongBan ShuYuan）

一个**只收录公有领域 / 开放许可内容**的阅读 App 书源项目，自带「自动校验 → 自动更新 → 自动部署」流水线（GitHub Actions + GitHub Pages）。

## 合规声明（重要）

本项目**不含**盗版站点、付费墙绕过、需要登录或验证的内容，也**不含成人内容**。
书单与书源规则仅指向两个合规来源：

- **维基文库（zh.wikisource.org）**：公有领域中文古籍、经典与开放许可文本（CC BY-SA 3.0 / 公有领域），章节化，适合整本长篇小说。
- **Project Gutenberg（www.gutenberg.org）**：公有领域电子书（含中文公版典籍），免登录、免费，**国内网络通常可直接访问**。

自动校验脚本只做「内容可达性与有效性」检查，不解析任何受版权保护的内容。

## 网络可达性提示（实测）

| 站点 | 本机（国内网络）实测 | 说明 |
|---|---|---|
| www.gutenberg.org | ✅ 可达 | 可直接用于书源 |
| zh.wikisource.org | ❌ 不可达 | 部分国内网络无法直连，需代理或改用 Gutenberg 书源 |
| GitHub Actions 校验 | ✅ 均可达 | 工作流运行在境外 GitHub 服务器，两类来源都会被正常校验 |

> 如果你无法访问维基文库，直接使用 **Gutenberg 书源** 即可，四大名著、论语、道德经、史记等公版书都在上面。

## 项目结构

```
gongban-shuyuan/
├── books.json                     # 书单（公有领域作品清单，含站点标记，可自行增删）
├── sources.json                   # 校验结果（自动生成）
├── 书单.md                        # 人类可读的校验清单（自动生成）
├── index.html                     # GitHub Pages 展示页（自动读取 sources.json）
├── 书源/
│   ├── 公版古籍_维基文库.json       # 阅读 App 书源：维基文库（章节化小说/古籍）
│   └── Gutenberg_公版中文书.json   # 阅读 App 书源：Gutenberg（国内可达）
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

1. 导入书源（任选或都导入）：
   - **网络导入**：书源管理 → 右上角菜单 → 网络导入，粘贴书源 JSON 直链。
   - 书源直链（部署后）：`https://<用户名>.github.io/<仓库名>/书源/公版古籍_维基文库.json` 或 `.../书源/Gutenberg_公版中文书.json`
2. 使用：
   - 维基文库书源：可搜索书名，或手动添加书籍网址（如 `https://zh.wikisource.org/wiki/紅樓夢`），自动解析章节。
   - Gutenberg 书源：搜索书名（如「红楼梦」），打开后进入「Plain Text UTF-8」纯文本在线阅读。
3. 规则均为 v0.1：个别书籍结构特殊时，可在书源管理里微调 `ruleToc.chapterList` / `ruleContent.content`。

## 部署到 GitHub（自动更新 / 自动校验 / 自动部署）

1. 新建一个 **Public** 仓库，把本项目全部文件推送上去。
2. 开启 Pages：仓库 **Settings → Pages → Source** 选择 **GitHub Actions**（不要选 Branch）。
3. Actions 工作流 `update.yml` 会：
   - **每天 10:30（UTC+8）自动运行**（cron `30 2 * * *`，可自行修改）；
   - 运行 `scripts/validate.py` 按站点自动校验每本书的可达性与有效性；
   - 状态有变化时**自动提交并推送**；
   - 自动**部署到 GitHub Pages**。
4. 也可以到 Actions 页面手动点 **Run workflow** 立即触发一次。

> 说明：`git push` 使用仓库自带的 `GITHUB_TOKEN`，无需额外配置密钥。

## 如何增删书单

编辑 `books.json` 的 `books` 数组，`site` 填 `wikisource` 或 `gutenberg`，`url` 填入对应站点上公有领域作品的页面地址即可，例如：

```json
{ "title": "红楼梦", "site": "gutenberg", "url": "https://www.gutenberg.org/ebooks/24264", "category": "四大名著" }
```

## 许可

- 项目脚本与配置：MIT（可自由使用、修改）
- 书单指向的文本内容：公有领域或按各来源站点自己的授权条款

> 使用本项目的书源读取内容时，请自行遵守对应来源站点的服务条款与当地法律法规。
