# 每周新闻热点

一个面向高中生的新闻周报生成器，聚合一周重大新闻，生成作文素材。

## 功能

- RSS 聚合：腾讯/网易/新浪/澎湃新闻
- 词云可视化：本周热词一览
- AI 周报：MiniMax 生成简洁摘要 + 作文素材

## 部署到 Vercel

### 1. 推送代码到 GitHub

```bash
cd weekly-news-analyzer
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/weekly-news-analyzer.git
git push -u origin master
```

### 2. Vercel 导入

1. 登录 [vercel.com](https://vercel.com)
2. 点击 "New Project"
3. 导入 GitHub 仓库 `weekly-news-analyzer`
4. Framework Preset 选择 "Python"
5. 添加环境变量：
   - `MINIMAX_API_KEY`: 你的 MiniMax API Key
6. 点击 "Deploy"

### 3. API 端点

- `POST /api/generate` - 手动触发周报生成
- `GET /api/latest` - 获取最新周报数据

### 4. 定时任务

已配置每周日 12:00 (UTC) 自动执行 `/api/generate`

## 本地开发

```bash
pip install -r requirements.txt
python task_runner.py
```

## 技术栈

RSS聚合 · jieba分词 · wordcloud词云 · MiniMax AI · Vercel
