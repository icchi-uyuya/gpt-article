import os
from typing import cast

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from streamlit_tags import st_tags

import src.prompt as prompt
from src.web.heading import Heading

load_dotenv()
API_KEY = os.environ["OPENAI_KEY"]
client = OpenAI(api_key=API_KEY)

st.set_page_config(
  layout="centered", page_title="記事生成 v0.2", page_icon="📑"
)

#プロパティ名
SUGGESTED_TITLES = "suggested_titles"
SUGGESTED_HEADINGS = "suggested_headings"
HEADINGS = "headings"
TITLE = "title"

#セッション変数の初期化
if "init" not in st.session_state:
  st.session_state["init"] = True
  st.session_state[SUGGESTED_TITLES] = []
  st.session_state[SUGGESTED_HEADINGS] = []
  st.session_state[HEADINGS] = [] #list[obj]

#基本情報
st.title("記事の生成")
st.info("""
  このWebアプリケーションはWordpressプラグインへ移行するまでの一時的な実装です。
  プラグインが公開され次第、そちらを利用することを検討してください。
""", icon="ℹ")

#キーワード選定
keywords = st_tags(
  text="Enterで追加",
  label="##### キーワード",
  value=["ハンドメイド", "指輪"],
)

st.write("##### ターゲット")
targets = st.text_input(
  label="target_input",
  placeholder="想定される記事の読者を入力してください    (例 カップル)",
  label_visibility="collapsed"
)
st.divider()

#TODO 記事データのカプセル化
#タイトル
titles = st.session_state[SUGGESTED_TITLES]
st.write("##### タイトル")
res = []
if st.button("タイトルを提案💡"):
  with st.spinner(): #TODO 提案するときは分類わけして表示するといいかも
    res = prompt.suggest_titles(client, keywords=keywords, targets=[targets])
    st.session_state[SUGGESTED_TITLES].extend(res)
if len(st.session_state[SUGGESTED_TITLES]) > 0:
  s = st.pills(
    label="キーワードから候補が生成されました",
    options=st.session_state[SUGGESTED_TITLES], 
    )
  st.caption("タイトルは選択した後に編集することもできます")
  if st.button("このタイトルを選択"):
    st.session_state[TITLE] = s
  
title = st.text_input(
  key=TITLE,
  label="title_input",
  label_visibility="collapsed",
  placeholder="タイトルを入力してください"
)
st.caption("キーワードからタイトルの候補を生成することもできます")
st.divider()

st.write("##### 見出し")
#見出しの提案
if st.button("タイトルから見出しを提案💡"):
  with st.spinner():
    arr = prompt.suggest_outlines(client, title=st.session_state["title"],
                          keywords=keywords, targets=[targets])
    st.session_state[SUGGESTED_HEADINGS] = arr
if len(st.session_state[SUGGESTED_HEADINGS]) > 0:
  arr = st.pills(
    label="目次の候補が生成されました",
    options=st.session_state[SUGGESTED_HEADINGS],
    selection_mode="multi",
  )
  st.caption("クリックで選択・選択解除します")
  if len(arr) > 0 and st.button(f"{len(arr)}個の見出しを追加"):
    st.toast("msg: successfully add heading")
    #クラス型に変換
    for h in arr:
      sh = prompt.suggest_subheadings(
        client, 
        title=st.session_state[TITLE],
        heading=h
      )
      st.session_state[HEADINGS].append(Heading(h, sh))

col1, col2 = st.columns([.8, .2], vertical_alignment="bottom")
head = col1.text_input(
  label="label_input",
  key="label_input",
  label_visibility="collapsed",
  placeholder="見出しを入力してください"
)

#見出し追加ボタンが押された時のコールバック関数
def add_heading() -> None:
  sh = prompt.suggest_subheadings(
        client, 
        title=st.session_state[TITLE],
        heading=head
      )
  st.session_state[HEADINGS].append(Heading(head, sh))
  st.session_state["label_input"] = ""

col2.button("追加", on_click=add_heading)
st.divider()

#レイアウト
st.write("##### レイアウト")
st.info("見出しをもとに小見出しをいくつか提案しました。項目は自由に編集できるため、順序の変更や追加・削除、編集などを行ってから記事を生成してください。")
headings = st.session_state[HEADINGS]
for i in range(len(headings)):
  h = cast(Heading, headings[i])
  with st.expander(h.name):
    with st.spinner():
      st.text_area(
        label="sub-headings", 
        label_visibility="collapsed",
        key=f"text-{i}", 
        value="\n".join(h.subs),
        height=250
      )

if st.button("記事を生成", icon="🖨️"):
  bar = st.progress(.0, text="テキストを生成しています...")
  #生成結果をクリアして全て生成
  for i, h in enumerate(st.session_state[HEADINGS]):
    bar.progress(i / len(st.session_state[HEADINGS]), text="テキストを生成しています...")
    h = cast(Heading, h)
    text = prompt.generate_body(
      client,
      title=st.session_state[TITLE],
      heading=h.name,
      subheading=h.subs
    )
    h.contents = text
  bar.empty()
st.divider()
 
#出力結果の表示
st.write("##### 出力結果の確認")
for i, h in enumerate(st.session_state[HEADINGS]):
  h = cast(Heading, h)
  if h.contents is not None:
    st.write(h.contents, unsafe_allow_html=True)
if st.button("htmlとしてコピー"):
  pass #TODO 続き実装
st.divider()


st.caption(f"### gpt-article v0.2 llm={prompt.LLM_MODEL}")
