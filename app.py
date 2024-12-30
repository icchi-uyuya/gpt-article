import streamlit as st
from streamlit_tags import st_tags
import src.prompt as prompt
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ["OPENAI_KEY"]
client = OpenAI(api_key=API_KEY)

st.set_page_config(
  layout="centered", page_title="記事生成 v0.1", page_icon="📑"
)

#セッション変数の初期化
if "init" not in st.session_state:
  st.session_state["init"] = True
  st.session_state["suggested_titles"] = []
  st.session_state["headings"] = []
  st.session_state["subheadings"] = [] #list[list[str]]

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
  label="target",
  placeholder="想定される記事の読者を入力してください    (例 カップル)",
  label_visibility="collapsed"
)
st.divider()

#TODO 記事データのカプセル化
#タイトル
titles = st.session_state["suggested_titles"]
st.write("##### タイトル")
res = []
if st.button("タイトルを提案"):
  with st.spinner():
    res = prompt.suggest_titles(client, keywords=keywords, targets=[targets])
    st.session_state["suggested_titles"].extend(res)
if len(st.session_state["suggested_titles"]) > 0:
  s = st.pills(
    label="キーワードから候補が生成されました",
    options=st.session_state["suggested_titles"], 
    )
  if s is not None:
    st.session_state["title"] = s
  st.caption("タイトルをクリックして選択・編集ができます")

ref = st.empty()
title = st.text_input(
  key="title",
  label="title",
  label_visibility="collapsed",
  placeholder="タイトルを入力してください"
)
st.caption("キーワードからタイトルの候補を生成することもできます")
st.divider()

st.write("### 見出し")
if st.button("タイトルから見出しを生成"):
  with st.spinner():
    arr = prompt.suggest_outlines(client, title=st.session_state["title"],
                          keywords=keywords, targets=[targets])
    st.session_state["headings"] = arr
if len(st.session_state["headings"]) > 0:
  heads = st.pills(
    label="目次の候補が生成されました",
    options=st.session_state["headings"],
    selection_mode="multi",
  )
  st.caption("クリックで選択・選択解除します")
  if st.button("記事を生成"):
    with st.spinner():
      print(title)
      print(heads)
      prompt.suggest_subheadings(client, title=title, heading=heads[0])
      bodies = []
      print("記事を生成しています...")
      for i in range(len(heads)):
        con = prompt.generate_body(client, title=title, 
                                   heading=heads[i], subheading=[])
        bodies.append(con)
        st.write(con, unsafe_allow_html=True)
#小見出し
#本文



st.caption(f"### gpt-article v0.1 llm={prompt.LLM_MODEL}")
