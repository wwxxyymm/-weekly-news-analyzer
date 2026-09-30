# 每周新闻热点

一个面向高中生的新闻周报生成器，聚合一周重大新闻，生成作文素材。

## 功能

- RSS 聚合：腾讯/网易/新浪/澎湃新闻
- 词云可视化：本周热词一览
- AI 周报：MiniMax 生成简洁摘要 + 作文素材

## 部署

1. Gitee 创建公开仓库，开启 Gitee Pages
2. PythonAnywhere 克隆仓库，安装依赖
3. 配置 MINIMAX_API_KEY 环境变量
4. 设置定时任务：每周日 20:00 执行 `python task_runner.py`

## 技术栈

RSS聚合 · jieba分词 · wordcloud词云 · MiniMax AI
