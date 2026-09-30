"""
RSS 新闻采集模块
功能：解析RSS源 → 过滤近7天 → 去重 → 返回新闻列表
"""
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict
from difflib import SequenceMatcher


# RSS 源配置（已验证可用 - 2026-09-30）
RSS_SOURCES = [
    # 中文源
    ("Solidot", "https://www.solidot.org/index.rss"),
    ("少数派", "https://sspai.com/feed"),
    # 英文源（国际热点）
    ("NPR News", "https://feeds.npr.org/1001/rss.xml"),
    ("TechCrunch", "https://techcrunch.com/feed/"),
    ("The Verge", "https://www.theverge.com/rss/index.xml"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index"),
    ("Wired", "https://www.wired.com/feed/rss"),
]


def get_news(days: int = 7, max_news: int = 30) -> List[Dict]:
    """
    获取近N天新闻

    Args:
        days: 天数，默认7天
        max_news: 最多返回条数

    Returns:
        新闻列表，每条包含 title, link, summary, published, source
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    all_news = []

    for source_name, url in RSS_SOURCES:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                # 解析发布时间
                published = parse_date(entry.get("published", ""))
                if published and published >= cutoff_date:
                    all_news.append({
                        "title": entry.get("title", ""),
                        "link": entry.get("link", ""),
                        "summary": entry.get("summary", "")[:200],
                        "published": published.strftime("%Y-%m-%d"),
                        "source": source_name,
                    })
        except Exception as e:
            print(f"Error fetching {source_name}: {e}")

    # 去重（标题相似度 > 0.8）
    unique_news = deduplicate_news(all_news)

    # 按时间排序
    unique_news.sort(key=lambda x: x["published"], reverse=True)

    return unique_news[:max_news]


def parse_date(date_str: str) -> datetime:
    """解析 RSS 日期格式，返回 naive datetime（统一时区）"""
    from email.utils import parsedate_to_datetime
    try:
        dt = parsedate_to_datetime(date_str)
        # 转换为 naive datetime（去掉时区信息）
        return dt.replace(tzinfo=None)
    except:
        try:
            dt = datetime.fromisoformat(date_str)
            if dt.tzinfo is not None:
                dt = dt.replace(tzinfo=None)
            return dt
        except:
            return None


def deduplicate_news(news_list: List[Dict], threshold: float = 0.8) -> List[Dict]:
    """基于标题相似度去重"""
    if not news_list:
        return []

    unique = [news_list[0]]

    for news in news_list[1:]:
        is_duplicate = False
        for existing in unique:
            similarity = SequenceMatcher(
                None,
                news["title"],
                existing["title"]
            ).ratio()
            if similarity > threshold:
                is_duplicate = True
                break
        if not is_duplicate:
            unique.append(news)

    return unique


if __name__ == "__main__":
    news = get_news()
    print(f"获取到 {len(news)} 条新闻")
    for n in news[:5]:
        print(f"- {n['title']} ({n['source']})")
