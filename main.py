import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import prompt

class Heading(BaseModel):
  name: list[str]

# APIキーをenvファイルから取得
load_dotenv()
API_KEY = os.environ["OPENAI_KEY"]

client = OpenAI(api_key=API_KEY)

#必要な情報
TITLE = "初めての自作PC! 初心者必見のマザーボードの選び方を徹底解説"
REFER_URL = ["https://www.sofmap.com/contents/?id=nw_ps_select&sid=mb"]
TARGET = ["高校生"]
KEYWORD = ["自作PC", "マザーボード"]

titles = prompt.suggest_title_from_keyword(client, input("keywords? ").split(","))
for i in range(len(titles)):
  print(f"{i}: {titles[i]}")

res = prompt.suggest_outlines(client, titles[int(input("idx? "))])
print(res)