from openai import OpenAI
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
import os

load_dotenv()
API_KEY = os.environ["OPENAI_KEY"]
client = OpenAI(api_key=API_KEY)

with open("./assets/icci-story-1.txt", "r") as fd:
  doc = "\n".join(fd.readlines())
docs = CharacterTextSplitter(
  chunk_size=200,
  chunk_overlap=5,
).split_text(doc)
embed = OpenAIEmbeddings(api_key=API_KEY)
from langchain.vectorstores import Chroma
db = Chroma.from_texts(docs, embed)
ret = db.as_retriever()
rs = db.similarity_search("11月の誕生石は？")
rs[0]