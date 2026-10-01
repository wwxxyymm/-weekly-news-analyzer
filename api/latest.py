"""
Vercel Serverless Function: 获取最新周报
"""
import os
import json
from datetime import datetime


def handler(request):
    """Vercel handler - 获取最新周报"""
    data_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "output",
        "data.json"
    )

    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "news_count": 0,
            "keywords": [],
            "message": "No data available. Run POST /api/generate first."
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(data, ensure_ascii=False, indent=2)
    }
