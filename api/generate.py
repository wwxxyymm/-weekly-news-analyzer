"""
Vercel Serverless Function: 生成周报
"""
import os
import sys
import json
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def handler(request):
    """Vercel handler - 触发周报生成"""
    from fetch_news import get_news
    from text_analysis import extract_keywords
    from llm_report import generate_weekly_report

    week_date = datetime.now().strftime("%Y-%m-%d")

    # 1. 抓取新闻
    news = get_news(days=7, max_news=30)

    if len(news) < 5:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Not enough news", "count": len(news)}, ensure_ascii=False)
        }

    # 2. 提取关键词
    keywords = extract_keywords(news, top_n=50)

    # 3. 生成周报
    report = generate_weekly_report(news)

    # 4. 返回结果
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "date": week_date,
            "news_count": len(news),
            "keywords": keywords[:20],
            "report": report
        }, ensure_ascii=False)
    }
