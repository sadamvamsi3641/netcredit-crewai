# rag/rag_pipeline.py
# NetCredit RAG Pipeline — Policy Document Q&A
# Built by Vamsi Sadam

import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate

# ── Step 1: Load policy documents ─────────────────
print("📄 Loading NetCredit policy documents...")
loader = TextLoader("rag/docs/netcredit_policies.txt")
documents = loader.load()
print(f"   Loaded {len(documents)} document(s)")

# ── Step 2: Split into chunks ─────────────────────
print("✂️  Splitting documents into chunks...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)
print(f"   Created {len(chunks)} chunks")

# ── Step 3: Embed and store in ChromaDB ───────────
print("🗄️  Storing chunks in ChromaDB...")
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="rag/chroma_db"
)
print("   ChromaDB ready!")

# ── Step 4: Build retriever ───────────────────────
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

# ── Step 5: Build Q&A chain ───────────────────────
llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("""
Answer the question based on the context below.
Context: {context}
Question: {question}
Answer:""")

qa_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# ── Step 6: Ask questions ─────────────────────────
print("\n" + "="*50)
print("NetCredit Policy Q&A System Ready!")
print("="*50)

questions = [
    "What is the minimum credit score required for loan approval?",
    "What happens to borrowers with recent bankruptcy?",
    "What is the maximum DTI ratio allowed?",
    "What are the interest rates for different risk tiers?",
    "How long does high risk application processing take?"
]

for question in questions:
    print(f"\n❓ Question: {question}")
    result = qa_chain.invoke(question)
    print(f"💡 Answer: {result}")
    print("-"*40)