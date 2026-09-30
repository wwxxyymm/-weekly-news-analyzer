"""
文本分析模块
功能：分词 → 词频统计 → 生成词云
"""
import jieba
from collections import Counter
from wordcloud import WordCloud
from typing import List, Dict


# 停用词表（常见无意义词）
STOPWORDS = set([
    "的", "了", "是", "在", "我", "有", "和", "就", "不", "人",
    "都", "一", "一个", "上", "也", "很", "到", "说", "要",
    "去", "你", "会", "着", "没有", "看", "好", "自己", "这",
    "那", "他", "她", "它", "们", "这个", "那个", "什么",
    "可以", "可能", "已经", "如果", "因为", "所以", "但是",
    "还", "又", "而", "与", "或", "等", "被", "把", "让",
    "对", "从", "向", "比", "更", "最", "非常", "当", "于",
    "中", "为", "之", "以", "及", "其", "所", "然后", "然而",
    "如何", "是否", "有些", "这些", "那些", "其中", "另外",
    "记者", "报道", "表示", "称", "据悉", "电", "日",
    "月", "年", "时", "分", "秒",
])


def extract_keywords(news_list: List[Dict], top_n: int = 50) -> List[tuple]:
    """
    从新闻列表提取关键词

    Args:
        news_list: 新闻列表
        top_n: 返回前N个关键词

    Returns:
        [(关键词, 频次), ...]
    """
    # 合并所有标题和摘要
    all_text = " ".join([
        n.get("title", "") + " " + n.get("summary", "")
        for n in news_list
    ])

    # 分词
    words = jieba.cut(all_text)

    # 过滤停用词和单字
    filtered = [
        w for w in words
        if w.strip() and len(w) >= 2 and w not in STOPWORDS
    ]

    # 词频统计
    counter = Counter(filtered)

    return counter.most_common(top_n)


def generate_wordcloud(keywords: List[tuple], output_path: str):
    """
    生成词云图片

    Args:
        keywords: [(词, 频次), ...]
        output_path: 保存路径
    """
    if not keywords:
        print("关键词为空，跳过词云生成")
        return

    # 转换为词频字典
    freq_dict = dict(keywords)

    # 创建词云（不指定字体，使用默认）
    wc = WordCloud(
        background_color="white",
        max_words=100,
        max_font_size=150,
        random_state=42,
        width=800,
        height=400,
    )

    wc.generate_from_frequencies(freq_dict)

    # 保存
    wc.to_file(output_path)
    print(f"词云已保存: {output_path}")


if __name__ == "__main__":
    # 测试
    from fetch_news import get_news

    news = get_news()
    keywords = extract_keywords(news)
    print(f"提取到 {len(keywords)} 个关键词")
    print("TOP10:", keywords[:10])
