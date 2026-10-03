"""
MiniMax API 调用模块
功能：组装prompt → 调用API → 生成周报
"""
import os
import requests
from typing import List, Dict


MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "").strip()
MINIMAX_BASE_URL = "https://api.minimax.chat/v1"


def generate_weekly_report(news_list: List[Dict]) -> str:
    """
    调用 MiniMax API 生成新闻周报

    Args:
        news_list: 新闻列表

    Returns:
        周报内容 (Markdown 格式)
    """
    if not MINIMAX_API_KEY:
        raise ValueError("MINIMAX_API_KEY 环境变量未设置")

    # 组装新闻素材
    news_text = "\n".join([
        f"- {n['title']} ({n['source']}, {n['published']})"
        for n in news_list
    ])

    # Prompt
    prompt = f"""你是一个高中作文辅导老师。请根据以下新闻素材，
生成一份简洁的新闻周报，包含：

1. 【本周热点 TOP5】：5条最重要新闻，每条用一句话概括
2. 【作文素材】：从新闻中提炼3-5个可用素材
   每个素材格式：
   - 事件：[一句话事件描述]
   - 适用主题：[1-2个高考常考主题，如"坚持"、"创新"、"环保"、"青春"、"责任"]
   - 延伸思考：[1句话启发]

素材：
{news_text}

要求：
- 语言简洁，适合高中生阅读
- 素材主题标注准确
- 总字数控制在800字以内"""

    # 调用 API
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "abab6.5s-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000,
    }

    response = requests.post(
        f"{MINIMAX_BASE_URL}/text/chatcompletion_v2",
        headers=headers,
        json=payload,
        timeout=60,
    )

    if response.status_code != 200:
        raise Exception(f"API调用失败: {response.status_code} - {response.text}")

    result = response.json()
    return result["choices"][0]["message"]["content"]


if __name__ == "__main__":
    # 测试
    from fetch_news import get_news

    news = get_news(max_news=10)
    report = generate_weekly_report(news)
    print(report)
