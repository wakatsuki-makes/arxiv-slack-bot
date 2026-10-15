# arxiv-slack-bot
- arXivからAIに関する論文を要約してSlackに持ってくるもの

## 仕組み
- arXivAPIを使ってarXivから特定の分野の論文を引っ張ってきてAPIを使って日本語に要約し、この結果をSlackに送る

## 使っている技術

- 言語: Python
- ライブラリ: requests(通信)、feedparser(arXiv の返事を読む)、python-dotenv(.env を読む)、groq(Groq API を使う)
- 外部サービス: arXiv API(論文の取得)、Groq API(LLM による要約)、Slack Incoming Webhook(配信)

## 工夫した点
- arXivから論文がもらえない場合でも3回まで、5秒おきにやり直すようにした
- AIの要約を、元の概要と照らして確認して、プロンプトを直した

## つまずいた点と解決
- GeminiAPIが動かないという問題が発生し、新しくAPIを作成したが解決しなかったためGroqに切り替えた

## 開発の進め方
- 開発では Claude を家庭教師として使い、ヒントをもらいながら自分でコードを書きました。
