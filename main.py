import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import src.prompt as prompt

class Heading(BaseModel):
  name: list[str]

# APIキーをenvファイルから取得
load_dotenv()
API_KEY = os.environ["OPENAI_KEY"]
client = OpenAI(api_key=API_KEY)

#必要な情報
#FIXME 検証のための初期値を削除
TITLE = "初めての自作PC! 初心者必見のマザーボードの選び方を徹底解説"
REFER_URL = ["https://www.sofmap.com/contents/?id=nw_ps_select&sid=mb"]
TARGETS = ["カップル"]
KEYWORDS = ["自作PC", "マザーボード"]

KEYWORDS = input("キーワードを入力して下さい: ").split(",")
TARGETS = input("読者のターゲットを入力して下さい: ").split(",")
titles = prompt.suggest_titles(client, keywords=KEYWORDS, targets=TARGETS)

for i in range(len(titles)):
  print(f"{i}: {titles[i]}")
num = int(input("タイトルの番号を入力してください: "))
TITLE = titles[num]

seo = prompt.suggest_seo_keywords(client, title=TITLE)
print(f"関連キーワード: {",".join(seo)}")

res = prompt.suggest_outlines(client, title=TITLE, keywords=KEYWORDS, targets=TARGETS)
for i in range(len(res)):
  print(f"{i}: {res[i]}")
idx = input("採用する見出しを順に入力してください: ").split(",")
heads = [res[int(x)] for x in idx]

print("次に子見出しを選択して下さい")
arr = []
for i in range(len(heads)):
  print(f"# {heads[i]}")
  subs = prompt.suggest_subheadings(client, title=TITLE, heading=heads[i])
  for j in range(len(subs)):
    print(f"{j}: {subs[j]}")
  idx = input("採用する子見出しを順に入力してください: ").split(",") #TODO 小見出しの生成は任意にする
  arr.append([subs[int(x)] for x in idx])

bodies = []
print("記事を生成しています...")
for i in range(len(heads)):
  con = prompt.generate_body(client, title=TITLE, 
                             heading=heads[i], subheading=arr[i])
  bodies.append(con)
  print(con, "\n")

ccl = prompt.generate_conclusion(client, body="\n".join(bodies))
print(ccl)