# 📄 PDF AI Assistant

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-orange?logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-Enabled-6E40C9)
![HuggingFace](https://img.shields.io/badge/HuggingFace-API-FFAE00?logo=huggingface)
![License](https://img.shields.io/badge/License-MIT-green)

A sleek, interactive AI web app built with **Streamlit** to let you upload PDFs and chat with their content — styled with a premium **glassmorphic UI**, dark mode by default, and deployable with **Docker**.

## ✨ Features

- 🧠 **Ask Questions** – Powered by LangChain + Hugging Face models.
- 🌫 **Glass UI** – Blurred, translucent design with dark/light mode toggle.
- 🖼 **Custom Background** – Add your own `assets/background.jpg`.
- 🐳 **Docker Support** – Easy local or cloud deployment.
- 📱 **Responsive** – Optimized for mobile and desktop.
- 🔐 **.env Secured** – Secure API key handling.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Docker (Optional)
- Git
- Hugging Face Token → [Create Token](https://huggingface.co/settings/tokens)

## ⚙️ Installation

**Clone & Setup**

```bash
git clone https://github.com/Thousifibrahim/pdf_qa_chatbot.git
cd pdf_qa_chatbot
```

### Option 1: Run Locally with Python

1.  **Install dependencies**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
2.  **Run the app**:
    ```bash
    streamlit run app.py
    ```
    Open [http://localhost:8501](http://localhost:8501) in your browser.

---

### Option 2: Run with Docker

1.  **Build the Docker image**:
    ```bash
    docker build -t pdf-ai-assistant:latest .
    ```
2.  **Run with Docker Compose**:
    ```bash
    docker-compose up
    ```
    Or run directly:
    ```bash
    docker run -p 8501:8501 pdf-ai-assistant:latest
    ```
    Access at [http://localhost:8501](http://localhost:8501).

---
I apologize for the misunderstanding. You want the content of the `README.md` file *without* any additional conversational text, just the raw markdown that you can directly copy and paste into a file.

Here is the entire `README.md` content in a single block, ready for you to copy and paste:

````markdown
# 📄 PDF AI Assistant

A modern, interactive web app built with Streamlit that lets you upload PDFs and chat with their content using AI-powered question-answering. Features a sleek glassmorphic UI with dark mode by default, customizable background, and Docker support for easy deployment.

---

✨ **Features**

* **Upload & Chat**: Upload a PDF and ask questions about its content, powered by LangChain and Hugging Face.
* **Glassmorphic UI**: Beautiful, translucent design with dark mode (default) and light mode toggle.
* **Custom Background**: Supports a customizable background image (`assets/background.jpg`).
* **Dockerized**: Run locally or deploy to the cloud with Docker and Docker Compose.
* **Responsive Design**: Optimized for desktop and mobile.
* **Secure**: Uses environment variables for sensitive data (e.g., Hugging Face API token).

---

🚀 **Getting Started**

### Prerequisites

* **Python 3.9**: Install from [python.org](https://www.python.org/).
* **Docker**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) for containerized setup.
* **Git**: For cloning the repository.
* **Hugging Face Account**: Get an API token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) for model access.

### Installation

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/Thousifibrahim/pdf_qa_chatbot.git](https://github.com/Thousifibrahim/pdf_qa_chatbot.git)
    cd pdf-ai-assistant
    ```

2.  **Set Up Environment Variables**:
    Create a `.env` file in the project root:
    ```
    HUGGINGFACEHUB_API_TOKEN=your-huggingface-token
    ```
    Replace `your-huggingface-token` with your Hugging Face API token.

3.  **Add Background Image**:
    Place a high-resolution image (e.g., `background.jpg`) in the `assets/` folder.
    Example: Download a free abstract image from [Unsplash](https://unsplash.com/).

---

### Option 1: Run Locally with Python

1.  **Install dependencies**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
2.  **Run the app**:
    ```bash
    streamlit run app.py
    ```
    Open [http://localhost:8501](http://localhost:8501) in your browser.

---

### Option 2: Run with Docker

1.  **Build the Docker image**:
    ```bash
    docker build -t pdf-ai-assistant:latest .
    ```
2.  **Run with Docker Compose**:
    ```bash
    docker-compose up
    ```
    Or run directly:
    ```bash
    docker run -p 8501:8501 pdf-ai-assistant:latest
    ```
    Access at [http://localhost:8501](http://localhost:8501).

---

### Project Structure

````

pdf\_qa\_chatbot/
├── assets/
│   └── background.jpg            \# Custom background image
├── app.py                        \# Main Streamlit app
├── qa\_chain.py                   \# LangChain Q\&A logic
├── document\_processor.py         \# PDF processing logic
├── requirements.txt              \# Python dependencies
├── .gitignore                    \# Git ignore file
├── Dockerfile                    \# Docker configuration
├── docker-compose.yml            \# Docker Compose configuration
├── .env                          \# Environment variables (not committed)

````

### Dependencies

See `requirements.txt` for the full list:

* `streamlit==1.38.0`
* `langchain==0.3.0`
* `pymupdf==1.24.9`
* `faiss-cpu==1.8.0`
* `sentence-transformers==3.1.1`
* `transformers==4.44.2`
* `torch==2.4.1`
* `python-dotenv==1.0.1`
* `langchain-huggingface==0.1.0`
* `langchain-community==0.3.0`

---

🌐 **Deployment**

Deploy your app to a free platform for public access. The following options are recommended:

### Option 1: Render (Docker-Based, Free Tier)

1.  **Push to Docker Hub**:
    * Create an account at [hub.docker.com](https://hub.docker.com/).
    * Log in:
        ```bash
        docker login
        ```
    * Tag and push the image:
        ```bash
        docker tag pdf-ai-assistant:latest yourusername/pdf-ai-assistant:latest
        docker push yourusername/pdf-ai-assistant:latest
        ```

2.  **Create Render Service**:
    * Sign up at [render.com](https://render.com/).
    * Create a new Web Service > Docker > Select `yourusername/pdf-ai-assistant:latest`.
    * Configure:
        * **Port**: `8501`
        * **Environment Variables**:
            * `STREAMLIT_SERVER_PORT=8501`
            * `STREAMLIT_SERVER_ADDRESS=0.0.0.0`
            * `HUGGINGFACEHUB_API_TOKEN=your-huggingface-token`
        * **Instance Type**: `Free`
    * Deploy and access the provided URL https://pdf-ai-assistant.onrender.com/.

---

### Option 2: Streamlit Community Cloud (Non-Docker, Free Tier)

1.  **Push to GitHub**:
    * Create a public repository:
        ```bash
        git remote add origin [https://github.com/Thousifibrahim/pdf_qa_chatbot.git]
        git push -u origin main
        ```
2.  **Deploy**:
    * Sign up at [streamlit.io/cloud](https://streamlit.io/cloud).
    * Create a new app, select your repository, and set:
        * **Main File**: `app.py`
        * **Environment Variable**: `HUGGINGFACEHUB_API_TOKEN=your-huggingface-token`
    * Deploy and access the provided URL.

---

🛠️ **Troubleshooting**

* Check browser console (F12) for 404 errors.

### Hugging Face API Errors:

* Verify `HUGGINGFACEHUB_API_TOKEN` is set in `.env` (local) or platform environment variables (cloud).
* Get a token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).

### Docker Issues:

* Ensure Docker Desktop is running (Windows: check system tray).
* Run `docker info` to verify the daemon.
* Increase Docker resources (Settings > Resources > 4GB RAM, 2 CPUs).

---

📜 **License**

This project is licensed under the MIT License - see the `LICENSE` file for details.

---

🙌 **Contributing**

Contributions are welcome! Please:

* Fork the repository.
* Create a feature branch (`git checkout -b feature/YourFeature`).
* Commit changes (`git commit -m "Add YourFeature"`).
* Push to the branch (`git push origin feature/YourFeature`).
* Open a pull request.

---

📬 **Contact**

Developed by Your Name - SMD-Thousif

Powered by Streamlit, LangChain, and Hugging Face
````

