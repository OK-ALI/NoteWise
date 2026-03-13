# NoteWise — Project Overview

## 📌 What is NoteWise?

NoteWise is an AI-powered study assistant that transforms handwritten or digital notes into interactive learning material. Upload your notes (images, PDFs, PowerPoint, or text), and NoteWise will extract, summarize, and generate practice questions — all powered by **Google Gemini 2.0 Flash**.

---

## 🏗️ Architecture

```
NoteWise/
├── main.py                          # Entry point — configures Streamlit, checks API key
├── app/
│   └── dashboard.py                 # 726-line Streamlit UI (4 pages)
├── core/
│   ├── ocr/
│   │   └── gemini_extractor.py      # Image/handwriting OCR via Gemini Vision
│   ├── summarizer/
│   │   └── gemini_summarizer.py     # Text summarization (short/standard/long/bullet)
│   ├── question_gen/
│   │   └── gemini_generator.py      # MCQ / True-False / Short Answer generation
│   ├── storage/
│   │   └── simple_storage.py        # JSON-based local persistence
│   └── exports/
│       └── enhanced_exporter.py     # PDF & text export with academic formatting
├── user_data/                       # Runtime JSON storage (gitignored)
├── requirements.txt                 # Python dependencies
├── .env                             # API keys & config (gitignored)
└── .gitignore
```

---

## 🔄 Application Flow

```
┌──────────────┐     ┌──────────────────┐     ┌───────────────────┐
│  Upload File │────▶│  Text Extraction │────▶│  Smart Summary    │
│ (PDF/IMG/PPT)│     │  (Gemini Vision) │     │  (Gemini Flash)   │
└──────────────┘     └──────────────────┘     └───────────────────┘
                              │                         │
                              ▼                         ▼
                     ┌──────────────────┐     ┌───────────────────┐
                     │  Manual Text     │     │  Question Gen     │
                     │  Input           │     │  (MCQ/TF/Short)   │
                     └──────────────────┘     └───────────────────┘
                                                        │
                                                        ▼
                                              ┌───────────────────┐
                                              │  Export (PDF/TXT)  │
                                              └───────────────────┘
```

---

## 🧩 Core Modules

### 1. `gemini_extractor.py` — OCR & Text Extraction
- Uses **Gemini 2.0 Flash** Vision API for image-based OCR
- Handles handwritten notes, tables, equations, and mixed layouts
- Returns extracted text + content analysis metadata

### 2. `gemini_summarizer.py` — Summarization
- Three length modes: **Short**, **Standard**, **Long**
- Bullet-point summary option
- Context-aware — understands document structure before summarizing

### 3. `gemini_generator.py` — Question Generation
- Generates **Multiple Choice**, **True/False**, and **Short Answer** questions
- User selects question types and count per type
- Each question includes answer + explanation
- Output organized by category

### 4. `simple_storage.py` — Persistence
- JSON-based local storage in `user_data/`
- Stores sessions, summaries, and question sets
- Session management with unique IDs and timestamps

### 5. `enhanced_exporter.py` — Export
- **PDF export** via ReportLab with academic styling
- **Text export** with clean formatting
- **Combined export** (summary + questions in one PDF)

### 6. `dashboard.py` — UI (Streamlit)
- **4 pages**: Text Extraction → Smart Summary → Practice Questions → History
- Sidebar with API key config, summary length, and question count controls
- File upload supporting PDF, PNG, JPG, JPEG, PPTX, PPT, TXT
- Download buttons for all export formats

---

## ⚙️ Tech Stack

| Layer          | Technology                        |
|----------------|-----------------------------------|
| AI Engine      | Google Generative AI (Gemini 2.0) |
| Web Framework  | Streamlit 1.37.1                  |
| PDF Parsing    | PDFplumber 0.11.7                 |
| PPTX Parsing   | python-pptx 0.6.23               |
| PDF Generation | ReportLab 4.4.3                   |
| Image Handling | Pillow ≥ 10.4.0                   |
| Environment    | python-dotenv 1.1.1               |

---

## 🚀 Running Locally

```bash
# 1. Create & activate virtual environment
python -m venv notewise_env
.\notewise_env\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key in .env
GEMINI_API_KEY=your_key_here

# 4. Launch
streamlit run main.py
```

App opens at `http://localhost:8501`.

---

## 📂 Key Design Decisions

1. **Gemini-only stack** — No local ML models. All AI processing uses the Gemini API, keeping the app lightweight and dependency-free for GPU.
2. **JSON storage** — Simple file-based persistence instead of a database, making the app portable and zero-config.
3. **Modular core** — Each capability (OCR, summarization, question gen, export) is a self-contained module under `core/`, making it easy to swap implementations.
4. **Graceful degradation** — Every import in `dashboard.py` is wrapped in try/except. If a module isn't available, the app still loads with reduced functionality.
