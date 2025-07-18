import streamlit as st
import os

def set_custom_style():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_title():
    st.title("📄 PDF AI Assistant")
    st.markdown("##### Upload your PDF and ask anything — powered by AI.")

def render_upload_section(temp_pdf_path):
    st.header("1. Upload Document")
    uploaded_file = st.file_uploader("Drag & drop your PDF here or click to browse:", type="pdf")

    if uploaded_file:
        file_id = f"{uploaded_file.name}-{uploaded_file.size}"
        if st.session_state.get("current_pdf_id") != file_id:
            st.session_state.qa_history = []
            st.session_state.pdf_processed = False
            st.session_state.current_pdf_id = file_id

        if not st.session_state.pdf_processed:
            with open(temp_pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("✨ Processing PDF..."):
                try:
                    chunk_count = st.session_state.qa_chain.load_document(temp_pdf_path)
                    st.success(f"✅ Document loaded with {chunk_count} chunks.")
                    st.session_state.pdf_processed = True
                    os.remove(temp_pdf_path)
                except Exception as e:
                    st.error(f"Error: {e}")
                    os.remove(temp_pdf_path)
        else:
            st.info(f"📄 '{uploaded_file.name}' is currently active.")

def render_question_section():
    st.header("2. Ask a Question")

    with st.form("question_form", clear_on_submit=True):
        user_question = st.text_input(
            "Enter your question:",
            placeholder="e.g., What are the key points?",
        )
        submit_button = st.form_submit_button("Get Answer")

        if submit_button:
            if not st.session_state.pdf_processed:
                st.warning("Please upload a PDF first.")
            elif not user_question.strip():
                st.warning("Please enter a valid question.")
            else:
                with st.spinner("🔍 Searching..."):
                    try:
                        response = st.session_state.qa_chain.ask_question(user_question)
                        st.session_state.qa_history.append({
                            "question": user_question,
                            "answer": response.get("answer", "No answer found."),
                            "sources": response.get("source_documents", [])
                        })
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

def render_qa_history():
    st.header("3. Conversation History")
    qa_container = st.container(height=450, border=False)

    with qa_container:
        if not st.session_state.qa_history:
            st.info("Your questions and answers will appear here.")
        else:
            for entry in reversed(st.session_state.qa_history):
                st.markdown(f'<div class="question-block">🤔 <strong>Question:</strong> {entry["question"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="answer-block">💡 <strong>Answer:</strong> {entry["answer"]}</div>', unsafe_allow_html=True)

                if entry.get("sources"):
                    with st.expander("🔗 View Supporting Snippets"):
                        st.markdown('<div class="source-header">Relevant Document Passages:</div>', unsafe_allow_html=True)
                        for i, source in enumerate(entry["sources"]):
                            snippet = source[:300] + "..." if len(source) > 300 else source
                            st.markdown(f"**Snippet {i+1}:**")
                            st.markdown(f'<div class="source-code-block">{snippet}</div>', unsafe_allow_html=True)
                            st.markdown("---")
