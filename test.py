from openai import OpenAI
from dotenv import load_dotenv
import os
from src import prompt

load_dotenv()
API_KEY = os.environ["OPENAI_KEY"]
client = OpenAI(api_key=API_KEY)

#SEOキーワード
def dump_seokey(kws: list[str], trg: list[str]):
  print(kws, trg)
  res = prompt.suggest_seo_keywords(
    client, 
    keywords=kws,
  )
  for v in res:
    print(v)
  print()

#dump_seokey(kws=["ピンキーリング", "人気"], trg=["カップル"])
#「指輪」をつけると対象がぼやける、なぜ？
#dump_seokey(kws=["ピンキーリング", "指輪"], trg=["カップル"])
#dump_seokey(kws=["ピンキーリング"], trg=["カップル"])

#アウトライン
def dump_outline(ttl: str, kws: list[str], trg: list[str]):
  res = prompt.suggest_outlines(
    client,
    title=ttl,
    keywords=kws,
    targets=trg,
    )
  print(ttl, kws, trg)
  for v in res:
    print(v)
  print()

dump_outline(ttl="カップル必見！人気ピンキーリングで愛を深める方法｜選び方ガイド", 
             kws=["ピンキーリング", "人気"], 
             trg=["カップル"])

