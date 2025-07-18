import streamlit as st
import os
from datetime import datetime
import shutil # Import shutil for file operations

# Import QAChain from your module (adjust the import path as needed)
from qa_chain import QAChain

# --- Constants & Paths ---
TEMP_PDF_PATH = "temp_uploaded_document.pdf"

# --- Page Configuration ---
st.set_page_config(
    page_title="PDF AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Theme Management ---
def get_theme_styles(theme):
    # Common styles for both themes
    common_styles = """
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
        }
        .stButton>button {
            border-radius: 12px;
            font-weight: 600;
            padding: 0.75em 1.5em;
            font-size: 1em;
            border: none;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            transition: all 0.2s ease-in-out;
        }
        .stButton>button:hover {
            transform: translateY(-1px);
        }
        .stTextInput>div>div>input {
            border-radius: 12px;
            padding: 0.9em 1.2em;
            font-size: 1.05em;
            transition: 0.3s ease;
        }
        .stTextInput>div>div>input:focus {
            box-shadow: 0 0 0 3px rgba(0, 221, 235, 0.25);
        }
        .stFileUploader>div>button {
            border-radius: 12px;
            padding: 0.7em 1.5em;
            font-size: 1em;
            font-weight: 600;
            border: none;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
        }
        .qa-container {
            border-radius: 18px;
            padding: 1rem;
            box-shadow: inset 0 1px 5px rgba(0, 0, 0, 0.1);
            overflow-y: auto;
            max-height: 450px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px); /* For Safari */
        }
        .question-block {
            border-radius: 12px;
            padding: 12px 16px;
            margin-bottom: 10px;
            font-weight: 600;
            max-width: 70%;
            margin-left: auto;
        }
        .answer-block {
            border-radius: 12px;
            padding: 16px 20px;
            margin-top: 5px;
            margin-bottom: 25px;
            font-size: 1.1em;
            max-width: 70%;
            margin-right: auto;
        }
        .timestamp {
            font-size: 0.8em;
            margin-top: 5px;
            opacity: 0.8;
        }
        .source-header {
            font-weight: 600;
            margin-top: 12px;
        }
        .source-code-block {
            border-radius: 10px;
            padding: 1rem;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            max-height: 180px;
            overflow-y: auto;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px); /* For Safari */
        }
        details summary {
            font-weight: 600;
            cursor: pointer;
        }
        footer {
            text-align: center;
            margin-top: 3em;
            font-size: 0.85em;
        }
    """

    if theme == "dark":
        return common_styles + """
            .stApp {
                background: linear-gradient(rgba(26, 26, 46, 0.7), rgba(22, 33, 62, 0.7)), url('/assets/background.jpg') no-repeat center center fixed;
                background-size: cover;
                color: #e0e0e0;
            }
            .main .block-container {
                background: rgba(30, 30, 50, 0.3);
                border-radius: 24px;
                padding: 3rem;
                margin-top: 3rem;
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(15px);
                -webkit-backdrop-filter: blur(15px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                max-width: 860px;
            }
            h1 {
                color: #ffffff;
                font-size: 2.6em;
                font-weight: 800;
                letter-spacing: -0.02em;
                text-align: center;
                margin-bottom: 0.3em;
            }
            h2 {
                color: #e0e0e0;
                font-size: 1.4em;
                font-weight: 700;
                border-left: 4px solid #00ddeb;
                padding-left: 12px;
                margin-top: 2em;
                margin-bottom: 1em;
            }
            .stButton>button {
                background: rgba(0, 221, 235, 0.8);
                color: #000;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            }
            .stButton>button:hover {
                background: rgba(0, 221, 235, 1);
            }
            .stTextInput>div>div>input {
                border: 1px solid rgba(255, 255, 255, 0.2);
                background: rgba(50, 50, 70, 0.4);
                color: #e0e0e0;
            }
            .stTextInput>div>div>input:focus {
                border-color: #00ddeb;
            }
            .stFileUploader>div>button {
                background: rgba(0, 221, 235, 0.8);
                color: #000;
                box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
            }
            .stFileUploader>div>button:hover {
                background: rgba(0, 221, 235, 1);
            }
            .qa-container {
                background: rgba(50, 50, 70, 0.3);
                box-shadow: inset 0 1px 5px rgba(0, 0, 0, 0.2);
            }
            .question-block {
                background-color: rgba(0, 221, 235, 0.1);
                color: #00ddeb;
                border: 1px solid rgba(0, 221, 235, 0.3);
            }
            .answer-block {
                background-color: rgba(48, 209, 88, 0.1);
                color: #30d158;
                border: 1px solid rgba(48, 209, 88, 0.3);
            }
            .timestamp {
                color: #aaaaaa;
            }
            .source-header {
                color: #aaaaaa;
            }
            .source-code-block {
                background: rgba(50, 50, 70, 0.5);
                color: #e0e0e0;
            }
            details summary {
                color: #00ddeb;
            }
            details[open] summary {
                color: #00b7c2;
            }
            footer {
                color: #aaaaaa;
            }
        """
    else:  # Light mode
        return common_styles + """
            .stApp {
                background: linear-gradient(rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.7)), url('/assets/background.jpg') no-repeat center center fixed;
                background-size: cover;
                color: #111;
            }
            .main .block-container {
                background: rgba(255, 255, 255, 0.35);
                border-radius: 24px;
                padding: 3rem;
                margin-top: 3rem;
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(15px);
                -webkit-backdrop-filter: blur(15px);
                border: 1px solid rgba(255, 255, 255, 0.18);
                max-width: 860px;
            }
            h1 {
                color: #111;
                font-size: 2.6em;
                font-weight: 800;
                letter-spacing: -0.02em;
                text-align: center;
                margin-bottom: 0.3em;
            }
            h2 {
                color: #333;
                font-size: 1.4em;
                font-weight: 700;
                border-left: 4px solid #007aff;
                padding-left: 12px;
                margin-top: 2em;
                margin-bottom: 1em;
            }
            .stButton>button {
                background: rgba(0, 122, 255, 0.8);
                color: white;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }
            .stButton>button:hover {
                background: rgba(10, 132, 255, 1);
            }
            .stTextInput>div>div>input {
                border: 1px solid rgba(0, 0, 0, 0.1);
                background: rgba(255, 255, 255, 0.5);
                color: #111;
            }
            .stTextInput>div>div>input:focus {
                border-color: #007aff;
            }
            .stFileUploader>div>button {
                background: rgba(100, 100, 255, 0.8);
                color: white;
                box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
            }
            .stFileUploader>div>button:hover {
                background: rgba(80, 80, 240, 1);
            }
            .qa-container {
                background: rgba(255, 255, 255, 0.3);
                box-shadow: inset 0 1px 5px rgba(0, 0, 0, 0.1);
            }
            .question-block {
                background-color: rgba(0, 122, 255, 0.07);
                color: #007aff;
                border: 1px solid rgba(0, 122, 255, 0.3);
            }
            .answer-block {
                background-color: rgba(48, 209, 88, 0.07);
                color: #1f7d38;
                border: 1px solid rgba(48, 209, 88, 0.3);
            }
            .timestamp {
                color: #666;
            }
            .source-header {
                color: #888;
            }
            .source-code-block {
                background: rgba(240, 240, 240, 0.6);
                color: #222;
            }
            details summary {
                color: #007aff;
            }
            details[open] summary {
                color: #0051cc;
            }
            footer {
                color: #888;
            }
        """

# Initialize theme in session state (dark mode as default)
if 'theme' not in st.session_state:
    st.session_state.theme = "dark"

# Sidebar for theme toggle and clear history
with st.sidebar:
    st.header("Settings")
    theme_toggle = st.toggle("Dark Mode", value=st.session_state.theme == "dark")
    if theme_toggle:
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "light"
    
    # Add a button to reset the entire app state
    if st.button("Reset App & Clear History", help="Clears all chat history and unloads the current PDF."):
        st.session_state.qa_history = []
        st.session_state.pdf_processed = False
        st.session_state.qa_chain = None # Reset the QAChain instance
        # Clean up temporary PDF if it exists
        if os.path.exists(TEMP_PDF_PATH):
            os.remove(TEMP_PDF_PATH)
        st.rerun() # Rerun to re-initialize everything cleanly

# Apply theme styles
st.markdown(f"<style>{get_theme_styles(st.session_state.theme)}</style>", unsafe_allow_html=True)

# --- Session State Initialization (Revised) ---
# Check if qa_chain needs to be initialized or re-initialized
if 'qa_chain' not in st.session_state or st.session_state.qa_chain is None:
    with st.spinner("⏳ Loading AI models... This might take a moment."):
        try:
            st.session_state.qa_chain = QAChain()
            # No st.success here to keep it clean, user sees the input fields become active
        except Exception as e:
            st.error(f"❌ Failed to load AI models. Please check your setup and try again. Error: {e}")
            st.stop() # Stop the app if models cannot be loaded

if 'qa_history' not in st.session_state:
    st.session_state.qa_history = []

if 'pdf_processed' not in st.session_state:
    st.session_state.pdf_processed = False

# --- Title & Description ---
st.title("📄 PDF AI Assistant")
st.markdown("##### Upload a PDF and chat with it like a friend!")

# --- Document Upload Section ---
st.header("1. Upload Document")
uploaded_file = st.file_uploader(
    "Drag & drop your PDF here or click to browse:",
    type="pdf",
    key="pdf_uploader_main"
)

if uploaded_file is not None:
    # Generate a unique ID for the file based on its name and size
    file_id = f"{uploaded_file.name}-{uploaded_file.size}"

    # Check if a new file is uploaded or if the existing one needs re-processing
    if 'current_pdf_id' not in st.session_state or st.session_state.current_pdf_id != file_id:
        st.session_state.pdf_processed = False # Mark for reprocessing
        st.session_state.current_pdf_id = file_id # Update current file ID
        st.session_state.qa_history = [] # Clear history for a new document

    if not st.session_state.pdf_processed:
        # Save the uploaded file temporarily
        try:
            with open(TEMP_PDF_PATH, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner(f"✨ Analyzing '{uploaded_file.name}'... This may take a moment."):
                chunk_count = st.session_state.qa_chain.load_document(TEMP_PDF_PATH)
                st.session_state.pdf_processed = True
                st.success(f"✅ Document loaded! Ready to chat about '{uploaded_file.name}'.")
                
        except Exception as e:
            st.error(f"❌ Could not process PDF. Please ensure it's a valid PDF and try again. Error: {e}")
            st.session_state.pdf_processed = False
        finally:
            # Always attempt to remove the temporary file
            if os.path.exists(TEMP_PDF_PATH):
                os.remove(TEMP_PDF_PATH)
    else:
        st.info(f"📄 Document '{uploaded_file.name}' is ready to chat!")

# --- Question Answering Section ---
st.header("2. Chat with Your Document")

# Use a form to allow clearing the text input after submission
with st.form("question_form", clear_on_submit=True):
    user_question = st.text_input(
        "Ask away:",
        placeholder="e.g., What's the main point of this document?",
        key="question_input_form" # Unique key for the input widget inside the form
    )

    col1, col2 = st.columns([1, 4]) # Use columns for button alignment
    with col1:
        submit_button = st.form_submit_button("Send", use_container_width=True)
    with col2:
        st.empty() # Placeholder column for spacing

    if submit_button:
        if not st.session_state.pdf_processed:
            st.warning("Please upload a PDF first to enable chat.")
        elif not user_question.strip():
            st.warning("Please enter a question before clicking 'Send'.")
        else:
            with st.spinner("🔍 Thinking..."):
                try:
                    response = st.session_state.qa_chain.ask_question(user_question)
                    answer = response.get("answer", "I couldn't find a relevant answer in the document.")
                    source_docs = response.get("source_documents", [])

                    # Store the Q&A in history, including timestamp
                    st.session_state.qa_history.append({
                        "question": user_question,
                        "answer": answer,
                        "sources": source_docs,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })

                except Exception as e:
                    # Generic error for the user, full detail printed to console for developer
                    st.error("❌ An error occurred while generating the answer. Please try again or check the console for details.")
                    print(f"Error in main app during ask_question: {e}") # Debug print

# --- Conversation History Display ---
st.header("3. Chat History")
qa_history_container = st.container(height=450, border=False)

with qa_history_container:
    if not st.session_state.qa_history:
        st.info("Your chat history will appear here once you start asking questions.")
    else:
        # Display history in reverse chronological order (latest answer on top)
        for entry in reversed(st.session_state.qa_history):
            st.markdown(
                f'<div class="question-block">👤 <strong>You:</strong> {entry["question"]}<br><span class="timestamp">{entry["timestamp"]}</span></div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="answer-block">🤖 <strong>AI:</strong> {entry["answer"]}<br><span class="timestamp">{entry["timestamp"]}</span></div>',
                unsafe_allow_html=True
            )

            if entry.get("sources"):
                with st.expander("🔗 View Supporting Document Snippets"):
                    st.markdown('<div class="source-header">Relevant passages from the document:</div>', unsafe_allow_html=True)
                    for i, source in enumerate(entry["sources"]):
                        # Truncate to a reasonable length for display
                        display_source = source[:500] + "..." if len(source) > 500 else source # Adjusted truncation length
                        st.markdown(f"**Snippet {i+1}:**")
                        st.markdown(f'<div class="source-code-block">{display_source}</div>', unsafe_allow_html=True)
                        st.markdown("---") # Visual separator between sources
            st.markdown("<br>", unsafe_allow_html=True) # Extra space between Q&A pairs

# --- Footer ---
st.markdown("---")
st.markdown("Developed by Your Name | Powered by LangChain & Hugging Face")