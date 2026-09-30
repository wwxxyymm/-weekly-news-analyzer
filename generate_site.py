"""
静态网页生成模块
功能：读取周报数据 → 渲染HTML模板
"""
import json
import os
from datetime import datetime
from typing import List, Dict
from markdown import markdown


def load_latest_data(data_dir: str = "output") -> Dict:
    """加载最新周报数据"""
    data_path = os.path.join(data_dir, "data.json")
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_history(data_dir: str = "output") -> List[Dict]:
    """获取历史周报列表"""
    history_path = os.path.join(data_dir, "weekly")
    if not os.path.exists(history_path):
        return []

    history = []
    for filename in os.listdir(history_path):
        if filename.endswith(".json"):
            with open(os.path.join(history_path, filename), "r", encoding="utf-8") as f:
                history.append(json.load(f))

    history.sort(key=lambda x: x.get("date", ""), reverse=True)
    return history


def generate_html(
    report_content: str,
    news_list: List[Dict],
    keywords: List[tuple],
    week_date: str,
    history: List[Dict],
    output_dir: str = "output"
) -> str:
    """
    生成静态网页

    Args:
        report_content: 周报内容 (Markdown)
        news_list: 新闻列表
        keywords: 关键词列表
        week_date: 周报日期
        history: 历史周报列表
        output_dir: 输出目录

    Returns:
        生成的HTML文件路径
    """
    # 转换 Markdown 为 HTML
    report_html = markdown(report_content)

    # 关键词列表（前20个）
    keyword_tags = " ".join([f"<span class='keyword'>{k[0]}</span>" for k in keywords[:20]])

    # 最新词云路径
    wordcloud_path = f"wordcloud/{week_date}.png"
    wordcloud_exists = os.path.exists(os.path.join(output_dir, wordcloud_path))
    wordcloud_html = f"<img src='{wordcloud_path}' alt='词云' class='wordcloud' />" if wordcloud_exists else ""

    # 历史周报列表
    history_html = "".join([
        f"<a href='weekly/{h['date']}.html' class='history-item'>{h.get('date', '未知')}</a>"
        for h in history[:10]
    ])

    # 渲染模板
    template_path = os.path.join("templates", "index.html")
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    html = template.replace("{{report_content}}", report_html)
    html = html.replace("{{week_date}}", week_date)
    html = html.replace("{{keyword_tags}}", keyword_tags)
    html = html.replace("{{wordcloud_html}}", wordcloud_html)
    html = html.replace("{{history_html}}", history_html)

    # 保存 index.html
    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)

    return index_path


def save_history(
    report_content: str,
    news_list: List[Dict],
    week_date: str,
    keywords: List[tuple],
    output_dir: str = "output"
):
    """保存历史周报"""
    weekly_dir = os.path.join(output_dir, "weekly")
    os.makedirs(weekly_dir, exist_ok=True)

    # 保存为 JSON
    data = {
        "date": week_date,
        "report": report_content,
        "news_count": len(news_list),
        "keywords": keywords[:20],
    }

    json_path = os.path.join(weekly_dir, f"{week_date}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 保存为 HTML（方便直接访问）
    html_content = markdown(report_content)
    html_path = os.path.join(weekly_dir, f"{week_date}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(f"<html><body><h1>{week_date} 周报</h1>{html_content}</body></html>")

    return json_path, html_path


if __name__ == "__main__":
    # 测试
    with open("test_report.md", "r") as f:
        report = f.read()

    week = datetime.now().strftime("%Y-%m-%d")
    generate_html(report, [], [("测试", 10)], week, [])
    print("HTML 生成成功")
