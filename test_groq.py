import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)
output = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content": "こんにちは、元気ですか？"}]
)
print(output.choices[0].message.content)

def summarize(paper):
    output = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "あなたは論文の要約が得意なアシスタントです。"},
            {"role": "user", "content": f"以下の論文を日本語で簡潔に3つのポイントに要約してください。: \n\n{paper['title']}\n{paper['summary']}"}
        ]
    )
    return output.choices[0].message.content

sample = {"title":"...","summary":"..."}
print(summarize(sample))