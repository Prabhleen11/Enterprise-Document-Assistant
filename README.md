# 📄 Enterprise Document Assistant

An AI-powered multi-document question-answering system built using Retrieval-Augmented Generation (RAG).

The application allows users to upload multiple PDF documents and ask natural-language questions about their content. Relevant document chunks are retrieved using semantic search and passed to a Groq-powered LLM to generate accurate answers.

## 🚀 Features

* 📄 Upload multiple PDF documents
* 🔍 Semantic document search
* 🧠 Retrieval-Augmented Generation (RAG)
* 🤖 LLM-powered question answering
* 📚 Source document citations
* 📖 Page-number citations
* 💬 Conversational chat history
* ⚡ FAISS vector database
* 🔐 Environment-based API key management
* 🖥️ Interactive Streamlit interface

## 🏗️ Architecture

```text
PDF Documents
      ↓
PyMuPDF Text Extraction
      ↓
Page-Level Processing
      ↓
Recursive Text Chunking
      ↓
HuggingFace Embeddings
      ↓
FAISS Vector Database
      ↓
Similarity Search
      ↓
Relevant Context Retrieval
      ↓
Groq LLM
      ↓
AI-Generated Answer
      ↓
Source + Page Citations
```

## 🛠️ Tech Stack

* Python
* Streamlit
* LangChain
* FAISS
* HuggingFace Sentence Transformers
* Groq API
* PyMuPDF

## 📁 Project Structure

```text
Enterprise-Document-Assistant/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
└── utils/
    ├── __init__.py
    ├── pdf_reader.py
    ├── rag.py
    └── groq.py
```

## ⚙️ Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate into the project:

```bash
cd Enterprise-Document-Assistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Run the application:

```bash
streamlit run app.py
```

## 🔐 Environment Variables

The project requires:

```text
GROQ_API_KEY
```

## 🧠 How RAG Works

The application follows a Retrieval-Augmented Generation pipeline:

1. Users upload PDF documents.
2. Text is extracted page by page.
3. Documents are divided into smaller chunks.
4. Chunks are converted into vector embeddings.
5. Embeddings are stored in a FAISS vector database.
6. User questions are converted into embeddings.
7. The most relevant document chunks are retrieved.
8. Retrieved context is sent to the Groq LLM.
9. The LLM generates an answer grounded in the documents.
10. Source filenames and page numbers are displayed to the user.

## 🔮 Future Improvements

* Persistent vector database storage
* OCR support for scanned PDFs
* Streaming responses
* User authentication
* Document deletion and management
* Hybrid keyword + semantic search
* Conversation-aware retrieval
* Cloud deployment

## 👩‍💻 Author

**Prabhleen Kaur**

Computer Science Engineering Student
Artificial Intelligence & Machine Learning

## ⭐ If you found this project useful

Feel free to explore, fork, and improve the project.
