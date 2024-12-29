from openai import OpenAI
from pydantic import BaseModel
from typing import overload

LLM_MODEL = "gpt-4o-mini"
#LLM_MODEL = "gpt-4o-2024-11-20"

# 単一の文字列配列のみを持つ構造
class StringArray(BaseModel):
  array: list[str]

@overload
def request[T : BaseModel](client: OpenAI, system_msg: str, user_msg: str, format: type[T]) -> T: ...

@overload
def request(client: OpenAI, system_msg: str, user_msg: str, format: None = None) -> str: ...

# APIを通して文章を生成します。formatにクラスを渡すことで構造化された結果が得られます
def request[T : BaseModel](client: OpenAI, system_msg: str, user_msg: str, format: type[T] | None = None) -> T | str:
  #フォーマットが指定されなかった時は構造化を利用しない
  if format is None:
    completion = client.chat.completions.create(
      model=LLM_MODEL,
      messages=[
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg}
      ],
    )
    res = completion.choices[0].message.content
    if res is None:
      raise RuntimeError("can't parse to json")
    return res
    
  #構造化出力を利用する
  else:
    # プロンプトを問い合わせる
    completion = client.beta.chat.completions.parse(
      model=LLM_MODEL,
      messages=[
          {"role": "system", "content": system_msg},
          {"role": "user", "content": user_msg}
      ],
      response_format=format
    )
    res = completion.choices[0].message.parsed
    if res is None:
      raise RuntimeError("can't parse to json")
    return res
  
# 入力されたキーワードをもとにタイトルの候補を生成します
#TODO プロンプトは変更しやすいようにtxtファイルに分離する
def suggest_titles(client: OpenAI, *, keywords: list[str], targets: list[str]) -> list[str]:
  system = "入力された要件に合うような、SEO最適化されたブログのタイトルを10個提案してください。"
  user = f"""
    キーワード: 「{", ".join(keywords)}」
    ターゲット: 「{", ".join(targets)}」
    """
  res = request(client, system, user, StringArray)
  return res.array

#検索欄の候補に表示されるようなキーワード候補をタイトルから考案します
#TODO 数の指定・追加で生成できるようにしたい
def suggest_seo_keywords(client: OpenAI, *, title: str) -> list[str]:
  system = "入力されたタイトルに関連するSEOキーワードを10個特定してください。"
  user = f"記事のタイトル: 「{title}」"
  res = request(client, system, user, StringArray)
  return res.array

def suggest_outlines(client: OpenAI, *, title: str, keywords: list[str], targets: list[str]) -> list[str]:
  system = "入力された項目を参考にして、ブログ記事のアウトラインの例を10個考えてください。"
  user = f"""
    記事のタイトル: 「{title}」
    キーワード: 「{", ".join(keywords)}」
    ターゲット: 「{", ".join(targets)}」
    """
  res = request(client, system, user, StringArray)
  return res.array

def suggest_subheadings(client: OpenAI, *, title: str, heading: str) -> list[str]:
  system = "入力された小見出しに合うような、さらに内側の見出しの例を10個提案してください。"
  user = f"""
    タイトル: 「{title}」
    見出し: 「{heading}」
  """
  res = request(client, system, user, StringArray)
  return res.array

def generate_body(client: OpenAI, *, 
                     title: str, heading: str, subheading: list[str]) -> str:
  system = """
    初心者を対象とした親しみやすく助けになる雰囲気で、SEOを意識した記事の本文を書いてください。
    文章は指定されたアウトラインの内容のみ書いてください。

    視点: 記事のライターとして、優しく親しみを得やすい文章を書く。

    出力: 
    - タグはマークアップ形式で出力してください。
    - 段落ごとに「p」タグで区切ってください。
    - 「##」の代わりに「h2」タグを、「###」の代わりに「h3」タグを使用してください。
    - マーカーを引きたいときは「strong」タグで囲ってください。
    """
  sh = "\n".join([f"### {x}" for x in subheading])
  user = f"""
    記事のタイトル: 「{title}」
    アウトライン:
    ## {heading}
    {sh}
    """
  res = request(client, system, user)
  return res

def generate_conclusion(client: OpenAI, *, body: str) -> str:
  system = "入力された文章のクロージングコピーを考案して下さい。"
  res = request(client, system, body)
  return res
