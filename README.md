# NoteWise 🧠 - Smart Study Assistant (Gemini 2.0 Edition)

NoteWise is an intelligent study companion that transforms your handwritten or digital notes into interactive learning material using Google's cutting-edge Gemini 2.0 Flash AI technology.

## 🚀 Features

### 🤖 **Gemini 2.0 Flash Integration**
- **Superior Text Extraction**: Advanced OCR using Google's latest Gemini 2.0 Flash API
- **Handwriting Recognition**: Excellent accuracy with handwritten notes
- **Complex Layout Understanding**: Handles tables, equations, and mixed content
- **Context-Aware Processing**: AI understands document structure and meaning

### 📝 **Intelligent Content Processing**
- **Smart Summarization**: High-quality summaries using Gemini 2.0 Flash
- **Flexible Question Generation**: Choose question types and get exact counts per type, organized by category
  - Multiple Choice Questions (MCQ)
  - True/False Questions
  - Short Answer Questions
- **Content Analysis**: Automatic difficulty assessment and topic identification
- **Multi-format Support**: PDFs, PowerPoint presentations (PPTX/PPT), images (PNG, JPG, JPEG), and text files

### 💾 **Enhanced Storage & Export**
- **Session Management**: Automatic saving of sessions, summaries, and questions
- **Professional PDF Export**: Well-formatted PDF exports with academic styling
- **Text Export**: Clean text file exports
- **Data Persistence**: Local JSON-based storage system

### 🎯 **User Experience**
- **Interactive Dashboard**: Clean, intuitive Streamlit interface
- **Real-time Processing**: Fast AI-powered analysis with Gemini 2.0
- **Flexible Question Control**: Select any combination of question types
- **Export Options**: Download summaries and questions in multiple formats

## 🛠️ Technology Stack

- **AI Engine**: Google Generative AI (Gemini 2.0 Flash)
- **Vision Processing**: Gemini 2.0 Flash for superior text extraction
- **Web Framework**: Streamlit 1.37.1 for interactive dashboard
- **Document Processing**: PDFplumber for PDF text extraction
- **PDF Generation**: ReportLab for professional PDF exports
- **Image Processing**: Pillow for image handling
- **Package Management**: UV for fast, reliable dependency installation
- **Environment Management**: python-dotenv for configuration

## 🏗️ Project Structure

```
NoteWise/
├── app/                    # Streamlit dashboard and UI
│   └── dashboard.py       # Main application interface
├── core/                   # Core business logic
│   ├── ocr/               # Text extraction modules
│   │   └── gemini_extractor.py  # Gemini 2.0 extraction
│   ├── summarizer/        # Text summarization
│   │   └── gemini_summarizer.py # Gemini 2.0 summarization
│   ├── question_gen/      # Question generation
│   │   └── gemini_generator.py  # Gemini 2.0 question generation
│   ├── storage/           # Data persistence
│   │   └── simple_storage.py    # Local JSON storage
│   └── exports/           # Export functionality
│       └── enhanced_exporter.py # PDF/Text export
├── user_data/             # Application data storage
│   ├── sessions.json      # User sessions
│   ├── summaries.json     # Generated summaries
│   └── questions.json     # Generated questions
├── main.py               # Application entry point
├── requirements.txt      # Project dependencies
└── .env                 # Environment configuration
```

## 🚀 Quick Start

### 1. **Get Gemini API Key**
- Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- Create a free API key
- Add it to your `.env` file: `GEMINI_API_KEY=your_actual_key_here`

### 2. **Setup Environment**
```bash
# Create virtual environment (already done)
python -m venv notewise_env

# Activate environment
.\notewise_env\Scripts\Activate.ps1

# Install dependencies with UV (fast)
uv pip install -r requirements.txt
```

### 3. **Run Application**
```bash
# Run through main entry point
streamlit run main.py

# Or directly run dashboard
streamlit run app/dashboard.py
```

### 4. **Access Application**
Open your browser to `http://localhost:8501`

## ⚡ System Requirements

- **Python**: 3.11+ (3.12 recommended)
- **Internet Connection**: Required for Gemini 2.0 Flash API calls
- **RAM**: 2GB minimum (4GB recommended)
- **Storage**: 500MB for application and dependencies

## � Troubleshooting

### **API Key Issues**
- Ensure valid Gemini API key in `.env`
- Check API quota and billing at [Google AI Studio](https://makersuite.google.com/app/apikey)
- Verify internet connection

### **Import Errors**
- Activate virtual environment: `.\notewise_env\Scripts\Activate.ps1`
- Reinstall dependencies: `uv pip install -r requirements.txt`

### **Streamlit Issues**
- Update Streamlit: `uv pip install -U streamlit`
- Clear cache: Delete `.streamlit/` folder
- Check port availability: Try different port with `--server.port 8502`

### **Question Generation Issues**
- Verify API key is valid and has quota
- Check if all question types are selected (at least one required)
- Ensure text content is sufficient for question generation

## 🎯 Key Improvements in This Version

- **✅ Latest AI Model**: Upgraded to Gemini 2.0 Flash for superior performance
- **✅ PowerPoint Support**: Added PPTX/PPT file processing with slide-by-slide extraction
- **✅ Organized Question Output**: Questions grouped by type (MCQ → Short Answer → True/False)
- **✅ Flexible Question Types**: Choose any combination of question types
- **✅ Exact Count Control**: Get precisely the number of questions requested per type
- **✅ Enhanced Export**: Professional PDF exports with academic formatting
- **✅ Data Persistence**: Automatic saving of sessions and generated content
- **✅ UV Package Manager**: Faster, more reliable dependency management
- **✅ Clean Codebase**: Removed unused files and optimized structure

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## � Acknowledgments

- **Google Generative AI** for providing powerful Gemini models
- **Streamlit** for the excellent web framework
- **Open Source Community** for tools and libraries

- Python 3.11+ (3.12 recommended)
- NVIDIA GPU with CUDA support (optional but recommended)
- 8GB+ RAM
- Windows/Linux/macOS

## 📖 Usage

1. **Upload Notes**: Drag and drop your notes (images/PDFs) into the upload area
2. **Extract Text**: OCR will automatically process your notes
3. **Generate Summary**: Choose summary length and get AI-powered summaries
4. **Practice Questions**: Access auto-generated questions for self-assessment

## 🔧 Development

- **Testing**: Run `pytest tests/` for unit tests
- **Code Formatting**: Use `black .` for code formatting
- **Linting**: Use `flake8 .` for code analysis

## � Future Roadmap

- [ ] Multi-language support for international students
- [ ] Advanced question types (Fill-in-the-blank, Essay prompts)
- [ ] Collaborative study features and sharing
- [ ] Mobile app development
- [ ] Integration with popular learning management systems
- [ ] Offline mode for basic text processing

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing & Support

### **How to Contribute**
1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### **Development Guidelines**
- Follow PEP 8 Python style guide
- Add docstrings to all functions
- Update README for new features
- Test with multiple file types before submitting

### **Need Help?**
- 📋 Create an [Issue](https://github.com/yourusername/notewise/issues) for bugs or feature requests
- 💬 Join our community discussions
- 📖 Check the troubleshooting section above

---

**Built with ❤️ for students and educators worldwide**

*Transform your study materials into interactive learning experiences with NoteWise - Your AI-powered study companion!*
