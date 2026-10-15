import requests
import feedparser
import os
from dotenv import load_dotenv
from groq import Groq
import time

URL="https://export.arxiv.org/api/query"
PARAMS={
    "search_query": "cat:cs.AI",
    "sortBy": "submittedDate",
    "sortOrder": "descending",
    "max_results": "5"}

def fetch_papers():
    for attempt in range(3):
        try:
            response = requests.get(
                URL,
                params=PARAMS,
                timeout=30,
                headers={"User-Agent":"arxiv-slack-bot"}
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException:
            if attempt == 2:
                raise
            else:
                time.sleep(5)

def parse_papers(response):
    feed = feedparser.parse(response.text)
    papers = []
    for entry in feed.entries:
        paper = {
            "title": entry.title,
            "summary": entry.summary,
            "url": entry.link,
        }
        papers.append(paper)
    return papers

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

def summarize(paper):
    output = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": """あなたは論文の要約が得意なアシスタントです。
            ・日本語で１行でポイントを簡潔にまとめて、それを３つ用意してください。,
            ・数字は、算用数字のままで。,
            ・専門用語は、英語のままでいいです。,
            ・与えられた概要に書かれていないことは、書かないでください。,
            ・前置きや見出しは書かないでください。
            ・複数の名前を並べるときは、「、」で区切る"""},
            {"role": "user", "content": f"以下の論文を記号は使わずに以下の要件を満たすように要約してください。: \n\n{paper['title']}\n{paper['summary']}"}
        ]
    )
    return output.choices[0].message.content

def send_slack(text):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    response = requests.post(webhook_url, json={"text": text}, timeout=30)
    print(response.status_code)

result = fetch_papers()
papers = parse_papers(result)
for paper in papers[:1]:
   send_slack(f"{paper['title']}\n{summarize(paper)}\n{paper['url']}")


    