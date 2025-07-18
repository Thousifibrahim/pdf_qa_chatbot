PDF Q&A Chatbot
A simple AI-powered tool to upload PDF documents (e.g., legal docs, contracts, academic papers) and ask questions about their content.
Features

Upload PDF documents via a web interface.
Extract text using PyMuPDF.
Index document content with FAISS for efficient retrieval.
Answer questions using LangChain and a HuggingFace model.
Web UI built with Streamlit.
Dockerized for portability.
Deployed to HuggingFace Spaces via GitHub Actions.

Setup Instructions

Clone the repository:git clone https://github.com/your-username/pdf_qa_chatbot.git
cd pdf_qa_chatbot


Create and activate a virtual environment:python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies (to be created in the next step):pip install -r requirements.txt



Next Steps

Install dependencies.
Implement document processing, Q&A pipeline, and UI.
Add Docker and CI/CD support.
