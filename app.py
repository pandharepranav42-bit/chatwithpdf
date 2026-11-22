import os
import sys
import subprocess

# --------------------------------------------------
# ENVIRONMENT AUTO-FIX & REDIRECT
# Ensures the application runs seamlessly under the project's venv
# --------------------------------------------------
_script_dir = os.path.dirname(os.path.abspath(__file__))
_venv_python = os.path.join(_script_dir, "venv", "Scripts", "python.exe")
_venv_streamlit = os.path.join(_script_dir, "venv", "Scripts", "streamlit.exe")

if os.path.exists(_venv_python) and os.path.normcase(sys.executable) != os.path.normcase(_venv_python):
    if os.path.exists(_venv_streamlit):
        print(f"[DocuMind AI] Switching execution to virtual environment: {_venv_python}")
        cmd = [_venv_streamlit, "run", os.path.abspath(__file__)] + sys.argv[1:]
        sys.exit(subprocess.call(cmd))

import streamlit as st
from pdf_processor import load_and_split_pdf
from rag_pipeline import create_vector_store, ask_question


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="DocuMind AI · Intelligent Document Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# MODERN STYLISH CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* Global Reset & Base Typography */
* {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

code, pre {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Background & Canvas */
.stApp {
    background: radial-gradient(circle at 15% 15%, #0f172a 0%, #090d16 100%);
    color: #e2e8f0;
}

.block-container {
    max-width: 1250px;
    padding-top: 1.8rem;
    padding-bottom: 4rem;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: #090d18;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

section[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

section[data-testid="stSidebar"] .stCaption {
    color: #94a3b8;
}

/* Futuristic Brand Header in Sidebar */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 4px 18px 4px;
}

.brand-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: linear-gradient(135deg, #6366f1, #06b6d4);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
}

.brand-title {
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #ffffff 40%, #a5b4fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1.2;
}

.brand-subtitle {
    font-size: 11px;
    color: #06b6d4;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 700;
}

/* Pulse Live Status Pill */
.status-pill-online {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    color: #10b981;
}

.pulse-dot {
    width: 7px;
    height: 7px;
    background-color: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 10px #10b981;
    animation: pulse-glow 2s infinite;
}

@keyframes pulse-glow {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 7px rgba(16, 185, 129, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

/* Modern Gradient Buttons */
.stButton button {
    background: linear-gradient(135deg, #4f46e5 0%, #6366f1 50%, #4338ca 100%);
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 11px !important;
    padding: 0.6rem 1.2rem !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    box-shadow: 0 4px 15px rgba(79, 70, 229, 0.25) !important;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.45) !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
    background: linear-gradient(135deg, #6366f1 0%, #818cf8 100%) !important;
}

/* File Uploader Glow */
div[data-testid="stFileUploader"] {
    background: rgba(15, 23, 42, 0.6);
    border: 1px dashed rgba(99, 102, 241, 0.4);
    border-radius: 14px;
    padding: 14px;
    transition: border-color 0.2s;
}

div[data-testid="stFileUploader"]:hover {
    border-color: #06b6d4;
}

/* Glassmorphic Hero Banner */
.hero-banner {
    position: relative;
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 20px;
    padding: 34px 40px;
    margin-bottom: 28px;
    box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.6);
    overflow: hidden;
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #06b6d4, #a855f7);
}

.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #a5b4fc;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 14px;
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -1px;
    line-height: 1.15;
    margin: 0 0 12px 0;
    background: linear-gradient(135deg, #ffffff 30%, #c7d2fe 70%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    color: #94a3b8;
    font-size: 16px;
    line-height: 1.6;
    margin: 0;
    max-width: 820px;
}

/* Telemetry Stats Card */
.stat-card {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    transition: transform 0.2s, border-color 0.2s;
}

.stat-card:hover {
    transform: translateY(-2px);
    border-color: rgba(99, 102, 241, 0.4);
}

.stat-icon {
    width: 44px;
    height: 44px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}

.stat-icon.groq { background: rgba(249, 115, 22, 0.15); color: #f97316; border: 1px solid rgba(249, 115, 22, 0.3); }
.stat-icon.faiss { background: rgba(14, 165, 233, 0.15); color: #0ea5e9; border: 1px solid rgba(14, 165, 233, 0.3); }
.stat-icon.ocr { background: rgba(168, 85, 247, 0.15); color: #a855f7; border: 1px solid rgba(168, 85, 247, 0.3); }

.stat-label {
    font-size: 11px;
    color: #64748b;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 0.8px;
    margin-bottom: 2px;
}

.stat-value {
    font-size: 15px;
    font-weight: 700;
    color: #f1f5f9;
}

.stat-desc {
    font-size: 11px;
    color: #94a3b8;
}

/* Feature Preview Cards (Empty State) */
.feature-card {
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 16px;
    padding: 24px;
    height: 100%;
    transition: all 0.25s ease;
}

.feature-card:hover {
    border-color: rgba(99, 102, 241, 0.4);
    box-shadow: 0 10px 30px -10px rgba(99, 102, 241, 0.2);
    transform: translateY(-3px);
}

.feature-icon-badge {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #818cf8;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    margin-bottom: 16px;
}

.feature-title {
    font-size: 17px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 8px;
}

.feature-desc {
    font-size: 13px;
    color: #94a3b8;
    line-height: 1.6;
}

/* Active Document Badge in Chat */
.active-doc-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(6, 182, 212, 0.3);
    border-radius: 14px;
    padding: 12px 20px;
    margin-bottom: 24px;
}

.doc-info {
    display: flex;
    align-items: center;
    gap: 12px;
}

.doc-icon {
    font-size: 22px;
}

.doc-name {
    font-weight: 700;
    color: #f8fafc;
    font-size: 15px;
}

.doc-meta {
    font-size: 12px;
    color: #06b6d4;
    font-weight: 600;
}

/* Chat Messages */
div[data-testid="stChatMessage"] {
    background: rgba(15, 23, 42, 0.75) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    padding: 16px 20px !important;
    margin-bottom: 16px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
}

/* Chat Input Styling */
div[data-testid="stChatInput"] {
    background: rgba(15, 23, 42, 0.9) !important;
    border: 1px solid rgba(99, 102, 241, 0.35) !important;
    border-radius: 16px !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
}

div[data-testid="stChatInput"]:focus-within {
    border-color: #06b6d4 !important;
    box-shadow: 0 0 20px rgba(6, 182, 212, 0.3) !important;
}

/* Sidebar Document Card */
.sidebar-doc-card {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 12px;
    padding: 14px;
    margin: 10px 0;
}

.sidebar-doc-title {
    font-size: 13px;
    font-weight: 700;
    color: #f1f5f9;
    word-break: break-all;
}

.sidebar-doc-stats {
    display: flex;
    gap: 12px;
    font-size: 11px;
    color: #10b981;
    font-weight: 600;
    margin-top: 6px;
}

/* Footer Styling */
.app-footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    padding: 30px 0 10px 0;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None

if "uploaded_file_id" not in st.session_state:
    st.session_state.uploaded_file_id = None

if "doc_pages" not in st.session_state:
    st.session_state.doc_pages = 0

if "doc_chunks" not in st.session_state:
    st.session_state.doc_chunks = 0


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="brand-icon">⚡</div>
            <div>
                <div class="brand-title">DocuMind AI</div>
                <div class="brand-subtitle">Intelligent RAG System</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="margin-bottom: 16px;">
            <span class="status-pill-online">
                <span class="pulse-dot"></span> System Engine Ready
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 📤 Upload Document")

    uploaded_file = st.file_uploader(
        "Upload PDF file",
        type=["pdf"],
        help="Upload textbook, research paper, report, or notes to analyze.",
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        file_id = f"{uploaded_file.name}_{uploaded_file.size}"

        if st.session_state.uploaded_file_id != file_id:
            st.session_state.pdf_processed = False
            st.session_state.uploaded_filename = None
            st.session_state.messages = []
            st.session_state.uploaded_file_id = file_id

        file_size_kb = uploaded_file.size / 1024
        size_str = f"{file_size_kb:.1f} KB" if file_size_kb < 1024 else f"{(file_size_kb/1024):.2f} MB"

        st.caption(f"📁 **Selected:** `{uploaded_file.name}` ({size_str})")

        if st.button("⚡ Process & Index Document", use_container_width=True):
            os.makedirs("data", exist_ok=True)
            pdf_path = os.path.join("data", "uploaded_document.pdf")

            try:
                with st.spinner("🔍 Extracting text, running OCR, and generating embeddings..."):
                    with open(pdf_path, "wb") as file:
                        file.write(uploaded_file.getvalue())

                    pages, chunks = load_and_split_pdf(pdf_path)

                    if not chunks:
                        st.error("No readable text found in this PDF.")
                        st.stop()

                    create_vector_store(chunks)

                    st.session_state.messages = []
                    st.session_state.pdf_processed = True
                    st.session_state.uploaded_filename = uploaded_file.name
                    st.session_state.doc_pages = len(pages)
                    st.session_state.doc_chunks = len(chunks)

                st.success(f"Indexed successfully! {len(pages)} pages · {len(chunks)} chunks.")
                st.rerun()

            except Exception as e:
                st.error(f"Processing error: {e}")

    st.markdown("---")

    st.markdown("### 📑 Document Status")

    if st.session_state.pdf_processed:
        st.markdown(
            f"""
            <div class="sidebar-doc-card">
                <div class="sidebar-doc-title">📄 {st.session_state.uploaded_filename}</div>
                <div class="sidebar-doc-stats">
                    <span>📃 {st.session_state.doc_pages} Pages</span>
                    <span>🧩 {st.session_state.doc_chunks} Chunks</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.caption("No document currently loaded. Upload a PDF above to begin.")

    st.markdown("---")

    st.markdown("### ⚙️ Session Controls")

    col_c1, col_c2 = st.columns(2)
    with col_c1:
        if st.button("🗑️ Clear", use_container_width=True, help="Clear chat history"):
            st.session_state.messages = []
            st.rerun()

    with col_c2:
        if st.session_state.messages:
            chat_text = "\n\n".join(
                f"{msg['role'].upper()}:\n{msg['content']}"
                for msg in st.session_state.messages
            )
            st.download_button(
                "📥 Export",
                data=chat_text,
                file_name="documind_chat.txt",
                mime="text/plain",
                use_container_width=True,
                help="Export conversation as text"
            )

    st.markdown(
        """
        <div style="font-size: 11px; color: #475569; margin-top: 30px; text-align: center;">
            Groq LPU™ · LangChain · FAISS · PyMuPDF
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# MAIN WORKSPACE
# --------------------------------------------------

# Modern Hero Banner
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-tag">✨ Advanced Document Intelligence v2.0</div>
        <h1 class="hero-title">Chat with any PDF document.</h1>
        <p class="hero-description">
            Extract insights, verify facts, summarize dense chapters, and ask complex questions.
            Powered by high-precision vector embeddings and ultra-low-latency Groq inference.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# High-Tech Telemetry Bar
col_t1, col_t2, col_t3 = st.columns(3)

with col_t1:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-icon groq">⚡</div>
            <div>
                <div class="stat-label">LLM Engine</div>
                <div class="stat-value">Groq LPU™</div>
                <div class="stat-desc">openai/gpt-oss-20b</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_t2:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-icon faiss">🧬</div>
            <div>
                <div class="stat-label">Vector Database</div>
                <div class="stat-value">FAISS Index</div>
                <div class="stat-desc">all-MiniLM-L6-v2</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_t3:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-icon ocr">👁️</div>
            <div>
                <div class="stat-label">Extraction Core</div>
                <div class="stat-value">Dual Engine</div>
                <div class="stat-desc">PyMuPDF + Tesseract OCR</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")


# --------------------------------------------------
# CHAT OR ONBOARDING WORKSPACE
# --------------------------------------------------
if not st.session_state.pdf_processed:
    st.markdown("### 🚀 How It Works")

    feat1, feat2, feat3 = st.columns(3)

    with feat1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon-badge">📤</div>
                <div class="feature-title">1. Upload Any PDF</div>
                <div class="feature-desc">
                    Supports digital books, research articles, reports, and scanned physical pages with embedded OCR.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with feat2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon-badge">⚡</div>
                <div class="feature-title">2. Semantic Vector Index</div>
                <div class="feature-desc">
                    Documents are split into contextual chunks and indexed into a dense FAISS vector database for instant retrieval.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with feat3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon-badge">💬</div>
                <div class="feature-title">3. Hallucination-Free Q&A</div>
                <div class="feature-desc">
                    Answers are strictly derived from source text with page citations and structured academic clarity.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

else:
    # Active Document Status Bar
    st.markdown(
        f"""
        <div class="active-doc-bar">
            <div class="doc-info">
                <span class="doc-icon">📄</span>
                <div>
                    <div class="doc-name">{st.session_state.uploaded_filename}</div>
                    <div class="doc-meta">● {st.session_state.doc_pages} Pages Indexed · {st.session_state.doc_chunks} Chunks in Vector Space</div>
                </div>
            </div>
            <span class="status-pill-online">Ready for queries</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Prompt Suggestion Cards (Shown when chat is empty)
    if not st.session_state.messages:
        st.markdown("##### 💡 Suggested Questions to Explore:")

        sug_cols = st.columns(4)

        suggestions = [
            ("📋 Executive Summary", "Summarize the key points of this document with bulleted takeaways."),
            ("🎯 Key Definitions", "Explain the most important concepts, formulas, or definitions."),
            ("📝 Study Guide", "Create a quick revision study guide and practice exam questions."),
            ("🔍 Critical Analysis", "What are the core conclusions and recommendations in this document?")
        ]

        for i, (label, prompt_text) in enumerate(suggestions):
            with sug_cols[i]:
                if st.button(label, use_container_width=True, key=f"sug_btn_{i}"):
                    st.session_state.pending_question = prompt_text
                    st.rerun()

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input Handling
    prompt_from_input = st.chat_input("Ask any question about your document...")

    pending_prompt = st.session_state.get("pending_question", None)
    if pending_prompt:
        active_question = pending_prompt
        del st.session_state["pending_question"]
    else:
        active_question = prompt_from_input

    if active_question:
        st.session_state.messages.append({
            "role": "user",
            "content": active_question
        })

        with st.chat_message("user"):
            st.markdown(active_question)

        with st.chat_message("assistant"):
            with st.spinner("🧠 Scanning vector database and synthesizing answer with Groq LPU..."):
                try:
                    answer = ask_question(active_question)
                    st.markdown(answer)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })
                except Exception as e:
                    err_msg = f"❌ Unable to generate answer: {e}"
                    st.error(err_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": err_msg
                    })


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    <div class="app-footer">
        <b>DocuMind AI</b> · Intelligent Retrieval-Augmented Generation Architecture
        <br>
        Engineered with Python · Streamlit · LangChain · FAISS · Groq LPU™
    </div>
    """,
    unsafe_allow_html=True
)
