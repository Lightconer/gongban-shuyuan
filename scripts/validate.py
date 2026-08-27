#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公版书源自动校验脚本（仅依赖 Python 标准库，零第三方依赖）

功能：
1. 读取 books.json（公有领域书单，按站点标记：wikisource / gutenberg）
2. 按站点做针对性校验：
   - wikisource：页面返回 200、包含正文容器(mw-parser-output)、非"页面不存在"(noarticletext)
   - gutenberg：页面返回 200、包含书目记录区(bibrec)
3. 生成 sources.json（机器可读校验状态，供 GitHub Pages 展示页读取）
4. 生成 书单.md（带状态标记的人类可读清单）

用法：
    python scripts/validate.py

返回码始终为 0，便于 GitHub Actions 无论成败都能提交更新结果。
"""
import json
import os
import sys
import datetime
import urllib.request
import urllib.error
from urllib.parse import quote

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS_JSON = os.path.join(BASE_DIR, "books.json")
OUT_JSON = os.path.join(BASE_DIR, "sources.json")
OUT_MD = os.path.join(BASE_DIR, "书单.md")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
TIMEOUT = 15

SITE_MARKERS = {
    "wikisource": {"require": "mw-parser-output", "absent": "noarticletext"},
    "gutenberg": {"require": "bibrec", "absent": ""},
}
SITE_NAMES = {"wikisource": "维基文库", "gutenberg": "Gutenberg"}


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch(url):
    # 中文路径需做百分号编码，否则 http.client 无法以 ASCII 发送请求行
    url = quote(url, safe="/:?&=#%+,;@~!*'()")
    req = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9"},
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.status, resp.read().decode("utf-8", errors="ignore")


def check_book(book):
    url, title = book["url"], book["title"]
    site = book.get("site", "wikisource")
    base = {"title": title, "url": url, "category": book.get("category", ""), "site": site}
    try:
        code, html = fetch(url)
    except urllib.error.HTTPError as e:
        return {**base, "status": "fail", "http_code": e.code, "reason": "HTTP %s" % e.code}
    except (urllib.error.URLError, OSError) as e:
        return {**base, "status": "fail", "http_code": 0, "reason": str(e)[:80]}
    if code != 200:
        return {**base, "status": "fail", "http_code": code, "reason": "非200响应"}
    marker = SITE_MARKERS.get(site, SITE_MARKERS["wikisource"])
    if marker["absent"] and marker["absent"] in html:
        return {**base, "status": "fail", "http_code": code,
                "reason": "页面不存在(%s)" % marker["absent"]}
    if marker["require"] not in html:
        return {**base, "status": "fail", "http_code": code,
                "reason": "未检测到正文(%s)" % marker["require"]}
    return {**base, "status": "ok", "http_code": code, "reason": ""}


def write_md(results):
    ok = [r for r in results if r["status"] == "ok"]
    fail = [r for r in results if r["status"] != "ok"]
    lines = [
        "# 公版书单（自动校验）",
        "",
        "> 本清单仅收录公有领域 / 开放许可中文文本（维基文库 / Project Gutenberg），自动校验由 GitHub Actions 定时执行。",
        "",
        "- 校验时间：%s（UTC）" % now_iso(),
        "- 正常：%d 本 / 异常：%d 本" % (len(ok), len(fail)),
        "",
        "## 正常书目",
        "",
        "| 书名 | 分类 | 站点 | 链接 |",
        "|---|---|---|---|",
    ]
    for r in ok:
        site = SITE_NAMES.get(r.get("site", ""), r.get("site", ""))
        lines.append("| %s | %s | %s | [打开](%s) |"
                     % (r["title"], r["category"], site, r["url"]))
    if fail:
        lines += ["", "## 异常书目（需关注）", "", "| 书名 | 站点 | 原因 |", "|---|---|---|"]
        for r in fail:
            site = SITE_NAMES.get(r.get("site", ""), r.get("site", ""))
            lines.append("| %s | %s | %s |" % (r["title"], site, r["reason"]))
    lines.append("")
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    with open(BOOKS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    books = data["books"]
    results = []
    print("开始校验 %d 个书源条目..." % len(books))
    for i, book in enumerate(books, 1):
        r = check_book(book)
        results.append(r)
        mark = "OK " if r["status"] == "ok" else "FAIL"
        print("[%02d/%02d] %s %s(%s) %s" % (i, len(books), mark, r["title"],
              r["site"], r["reason"]))
    out = {
        "project": data.get("project", "合规公版书源"),
        "updated_at": now_iso(),
        "summary": {
            "total": len(results),
            "ok": sum(1 for r in results if r["status"] == "ok"),
            "fail": sum(1 for r in results if r["status"] != "ok"),
        },
        "results": results,
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    write_md(results)
    print("\n完成：正常 %d / 异常 %d，已写入 sources.json 与 书单.md"
          % (out["summary"]["ok"], out["summary"]["fail"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
