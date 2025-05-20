# 📚 Chatbot Theme Identifier

## 🔍 Overview
A powerful web-based research assistant that processes large document sets, identifies themes across documents, and provides detailed responses with citations. Perfect for researchers, analysts, and knowledge workers dealing with extensive document collections.

## ✨ Key Features
- **Bulk Document Processing**: Upload and process 75+ documents simultaneously
- **Multi-Format Support**: Works with PDFs, scanned images (PNG, JPG, TIFF)
- **Advanced OCR**: Extracts text from scanned documents using Tesseract
- **Semantic Search**: Find relevant information across your document collection
- **Theme Identification**: AI-powered analysis of common themes across documents
- **Detailed Citations**: All responses include document and page references
- **Interactive UI**: Clean, responsive Streamlit interface

## 🛠️ Tech Stack
- **Frontend**: Streamlit (Python-based UI framework)
- **Document Processing**: 
  - Tesseract OCR (image text extraction)
  - PDFPlumber (PDF text extraction)
  - OpenCV (image preprocessing)
- **Vector Database**: ChromaDB (document embedding storage)
- **Embeddings**: HuggingFace Sentence Transformers
- **LLM Integration**: Groq API (using Gemma 2 9B model)
- **Containerization**: Docker support

## 📂 Project Structure
```
chatbot_theme_identifier/
├── backend/
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Document processing logic
│   │   ├── models/        # LLM integration
│   │   ├── services/      # Vector DB services
│   │   ├── data/          # Storage for uploads and DB
│   │   ├── main.py        # Main Streamlit application
│   │   └── config.py      # Configuration settings
│   ├── Dockerfile         # Container definition
│   └── requirements.txt   # Dependencies
├── docs/                  # Documentation
├── tests/                 # Test files
└── README.md              # Project documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Tesseract OCR installed (for image processing)
- Groq API key (for LLM access)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/chatbot-theme-identifier.git
   cd chatbot-theme-identifier/backend
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Configure your API key:
   - Open `backend/app/config.py`
   - Replace `"ENTER-YOUR-API-KEY-HERE"` with your Groq API key

4. Run the application:
   ```bash
   streamlit run backend/app/main.py
   ```

### Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t chatbot-theme-identifier ./backend
   ```

2. Run the container:
   ```bash
   docker run -p 8501:8501 chatbot-theme-identifier
   ```

3. Access the application at `http://localhost:8501`

## 💡 Usage

1. **Upload Documents**: Use the sidebar to upload PDFs or images
2. **Process Documents**: Click "Process Uploaded Documents" to extract and index content
3. **Ask Questions**: Use the chat interface to query your document collection
4. **Review Results**: See individual document hits and synthesized themes in responses

## 🔮 Future Enhancements
- Multi-language support
- Additional document format support (DOCX, TXT, etc.)
- User authentication and document permissions
- Advanced visualization of document relationships
- Integration with additional LLM providers

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements
- [Streamlit](https://streamlit.io/) for the interactive UI framework
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for text extraction
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [Groq](https://groq.com/) for LLM API access