"""
定时任务入口
每周执行一次：抓新闻 → 分析 → 生成周报 → 生成网页 → 推送Gitee
"""
import os
import sys
import subprocess
from datetime import datetime

# 确保项目根目录在 Python 路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fetch_news import get_news
from text_analysis import extract_keywords, generate_wordcloud
from llm_report import generate_weekly_report
from generate_site import generate_html, save_history


def run():
    print(f"=== 开始执行周报生成任务 {datetime.now()} ===")

    # 1. 抓取新闻
    print("\n[1/6] 抓取新闻...")
    news = get_news(days=7, max_news=30)
    print(f"    获取到 {len(news)} 条新闻")

    if len(news) < 5:
        print("    新闻数量不足，跳过生成")
        return

    # 2. 提取关键词
    print("\n[2/6] 提取关键词...")
    keywords = extract_keywords(news, top_n=50)
    print(f"    提取到 {len(keywords)} 个关键词")

    # 3. 生成词云
    print("\n[3/6] 生成词云...")
    week_date = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("output/wordcloud", exist_ok=True)
    wordcloud_path = f"output/wordcloud/{week_date}.png"
    generate_wordcloud(keywords, wordcloud_path)

    # 4. 生成周报
    print("\n[4/6] 生成周报...")
    report = generate_weekly_report(news)
    print(f"    周报长度: {len(report)} 字符")

    # 5. 生成网页
    print("\n[5/6] 生成静态网页...")
    history = []  # 简化版，暂不加载历史
    generate_html(report, news, keywords, week_date, history)
    save_history(report, news, week_date, keywords)

    # 保存最新数据
    import json
    with open("output/data.json", "w", encoding="utf-8") as f:
        json.dump({
            "date": week_date,
            "news_count": len(news),
            "keywords": keywords[:20],
        }, f, ensure_ascii=False, indent=2)

    # 6. 推送到 Gitee
    print("\n[6/6] 推送到 Gitee...")
    try:
        subprocess.run(["git", "add", "output/"], check=True)
        subprocess.run(["git", "commit", "-m", f"feat: update weekly report {week_date}"], check=True)
        subprocess.run(["git", "push", "origin", "master"], check=True)
        print("    推送成功!")
    except subprocess.CalledProcessError as e:
        print(f"    Git 操作失败: {e}")

    print(f"\n=== 任务完成 {datetime.now()} ===")


if __name__ == "__main__":
    run()
