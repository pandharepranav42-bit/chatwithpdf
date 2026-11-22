
import os
from functools import lru_cache

from dotenv import load_dotenv
from groq import Groq

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

GROQ_MODEL = "openai/gpt-oss-20b"
VECTORSTORE_PATH = "vectorstore"

# Set True if you want to inspect retrieved PDF content
DEBUG_RETRIEVAL = False


# ==========================================
# 2. INITIALIZE EMBEDDING MODEL
# ==========================================

@lru_cache(maxsize=1)
def get_embedding_model():

    print("Loading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Embedding model loaded successfully!")

    return embeddings


# ==========================================
# 3. CREATE FAISS VECTOR DATABASE
# ==========================================

def create_vector_store(chunks):

    print("Creating FAISS vector database...")

    embeddings = get_embedding_model()

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    os.makedirs(VECTORSTORE_PATH, exist_ok=True)

    vector_store.save_local(VECTORSTORE_PATH)

    # Clear cached database after rebuilding
    load_vector_store.cache_clear()

    print("FAISS database created successfully!")

    return vector_store


# ==========================================
# 4. LOAD EXISTING FAISS DATABASE
# ==========================================

@lru_cache(maxsize=1)
def load_vector_store():

    index_path = os.path.join(
        VECTORSTORE_PATH,
        "index.faiss"
    )

    if not os.path.exists(index_path):

        raise FileNotFoundError(
            "FAISS database not found. "
            "Please process your PDF first."
        )

    print("Loading FAISS database...")

    embeddings = get_embedding_model()

    vector_store = FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("FAISS database loaded successfully!")

    return vector_store


# ==========================================
# 5. RETRIEVE RELEVANT PDF CHUNKS
# ==========================================

def retrieve_documents(vector_store, question):

    print("Searching relevant PDF content...")

    documents = vector_store.similarity_search(
        question,
        k=5
    )

    return documents


# ==========================================
# 6. GENERATE DETAILED ANSWER USING GROQ
# ==========================================

@lru_cache(maxsize=1)
def get_groq_client():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            pass

    if not api_key:

        raise ValueError(
            "Groq API key not found. "
            "Please add GROQ_API_KEY to your .env file or Streamlit Secrets."
        )

    return Groq(api_key=api_key)


def generate_answer(question, documents):

    client = get_groq_client()

    # Prepare PDF context
    context = ""

    for document in documents:

        page_number = (
            document.metadata.get("page", 0) + 1
        )

        context += (
            f"\n\n[Source Page: {page_number}]\n"
            f"{document.page_content}"
        )

    # Detailed system prompt
    system_prompt = """
You are an intelligent and detailed PDF Question
Answering Assistant designed to help college students.

Your responsibility is to explain concepts using
the information retrieved from the uploaded PDF.

STRICT KNOWLEDGE RULES:

1. Answer using ONLY the supplied PDF context.
2. Never invent facts, definitions, examples or sources.
3. Do not use outside knowledge to fill missing information.
4. If the answer cannot be found in the context, respond:
   "The answer was not found in the uploaded PDF."
5. If only partial information is available, clearly
   explain what information is available and what is missing.

ANSWER STYLE:

1. Start with a clear definition or direct answer.
2. Explain the concept in detail using simple language.
3. Organize answers with meaningful headings.
4. Use bullet points and numbered lists wherever appropriate.
5. Explain important technical terms.
6. Include examples from the PDF when available.
7. For comparison questions, use a comparison table
   when sufficient information is available.
8. For questions about types, features or advantages,
   explain each point separately.
9. Avoid unnecessarily short answers.
10. Do not repeat the same information.

ANSWER LENGTH:

- Definition questions: Give a clear definition and
  supporting explanation.
- Explain questions: Provide a detailed explanation
  with relevant points and examples.
- Comparison questions: Explain the differences clearly.
- List questions: Explain each listed item.
- Broad questions: Organize the answer into sections.

Do not make an answer artificially long if the PDF
contains only limited information.

SOURCE REFERENCES:

1. Mention the original PDF page numbers.
2. Cite the pages supporting the explanation.
3. Never invent page numbers.

Your goal is to help students understand concepts
clearly and prepare for academic examinations.
"""

    # Send request to Groq
    response = client.chat.completions.create(

        model=GROQ_MODEL,

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"""
PDF CONTEXT:

{context}

STUDENT QUESTION:

{question}

Provide a detailed, well-structured answer
using only the supplied PDF context.
"""
            }
        ],

        temperature=0.2,

        max_completion_tokens=1500
    )

    answer = response.choices[0].message.content

    return answer


# ==========================================
# 7. COMPLETE RAG PIPELINE
# ==========================================

def ask_question(question):

    if not question or not question.strip():

        return "Please enter a valid question."

    try:

        # Load FAISS database
        vector_store = load_vector_store()

        # Retrieve relevant documents
        documents = retrieve_documents(
            vector_store,
            question
        )

        if not documents:

            return (
                "No relevant information was found "
                "in the uploaded PDF."
            )

        print(f"Retrieved {len(documents)} relevant chunks.")

        # Optional retrieval debugging
        if DEBUG_RETRIEVAL:

            print("\n========== RETRIEVED CONTENT ==========")

            for i, document in enumerate(
                documents,
                start=1
            ):

                page_number = (
                    document.metadata.get("page", 0) + 1
                )

                print(f"\nChunk {i}")
                print(f"Page: {page_number}")
                print(document.page_content)

        # Generate detailed AI answer
        print("\nGenerating detailed answer using Groq...")

        answer = generate_answer(
            question,
            documents
        )

        return answer

    except Exception as e:

        print(f"\nRAG Pipeline Error: {e}")

        return (
            "Sorry, something went wrong while "
            "processing your question. Please try again."
        )
