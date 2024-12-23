from openai import OpenAI
from pydantic import BaseModel

class TitleSuggestion(BaseModel):
  titles: list[str]

#入力されたキーワードをもとにタイトルの候補を生成します
def suggest_title_from_keyword(client: OpenAI, keywords: list[str]) -> list[str]:
  #目次を生成
  completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    #TODO システムプロンプトはファイルに書いたが楽かも
    messages=[ #TODO プロンプトへの入力は関数でまとめる
        {"role": "system", "content": f"入力されたSEOキーワードのリストに関連する、クリックされるブログのタイトルを提案してください。"},
        {"role": "user", "content": " ".join(keywords)}
    ],
    response_format=TitleSuggestion
  )

  res = completion.choices[0].message.parsed
  if (res is None):
    raise RuntimeError("can't parse to json")
  return res.titles

class KeywordSuggestion(BaseModel):
  keywords: list[str]

#検索欄の候補に表示されるようなキーワード候補をタイトルから考案します
#TODO 数の指定・追加で生成できるようにしたい
def suggest_seo_keywords(client: OpenAI, title: str) -> list[str]:
  #目次を生成
  completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": f"入力されたタイトルに関連するSEOキーワードを10個特定してください。"},
        {"role": "user", "content": title}
    ],
    response_format=KeywordSuggestion
  )

  res = completion.choices[0].message.parsed
  if (res is None):
    raise RuntimeError("can't parse to json")
  return res.keywords

#class OutlineSuggestion(BaseModel):


def suggest_outlines(client: OpenAI, title: str) -> list[str]:
  #目次を生成
  completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": f"あなたはSEOに精通したテクニカルライターと仮定します。初心者を対象とした親しみやすく助けになる雰囲気で、入力された要件に合ったステップバイステップガイドの詳しいブログ記事のアウトラインを作成してください。"},
        {"role": "user", "content": f"タイトル: {title}"}
    ],
  )

  res = completion.choices[0].message.content
  return res
  

