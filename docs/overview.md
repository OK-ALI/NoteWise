# NoteWise — Project Overview

## 📌 What is NoteWise?

NoteWise is an AI-powered study assistant that transforms handwritten or digital notes into interactive learning material. Upload your notes (images, PDFs, PowerPoint, or text), and NoteWise will extract, summarize, and generate practice questions — all powered by **Google Gemini 2.0 Flash**.

Built as a modular Streamlit web application with a clean separation between UI, AI processing, storage, and export layers.

---

## 🚀 Features & Functionality

### 📄 Multi-Format Text Extraction

NoteWise extracts text from a wide variety of input formats, each handled by a specialized processing pipeline:

| Format | Method | Details |
|--------|--------|---------|
| **Images** (PNG, JPG, JPEG, BMP, TIFF, WebP) | Gemini 2.0 Flash Vision API | AI-powered OCR with handwriting recognition |
| **PDFs** | PDFplumber + Gemini Vision fallback | Text PDFs parsed directly; scanned/image PDFs fall back to Vision API |
| **PowerPoint** (PPTX, PPT) | python-pptx | Slide-by-slide extraction including shape text and speaker notes |
| **Text Files** (TXT) | Direct read | UTF-8 encoded plain text |
| **Manual Input** | Dashboard text area | Paste or type text directly into the app |

#### Three OCR Extraction Modes

The Gemini Vision extractor supports three prompt-tuned modes depending on the content type:

- **Comprehensive** (default) — Extracts all readable text including math equations, tables, bullet points, and handwritten notes. Flags unclear text as `[unclear: possible_text]`.
- **Structured** — Reorganizes extracted content with proper headers, grouping, and clean formatting. Optimized for creating study-ready notes.
- **Handwritten** — Specialized mode for handwritten content with emphasis on character disambiguation, context-based interpretation, and recognition of crossed-out corrections.

#### Content Analysis

After extraction, NoteWise can automatically analyze the content and report:

- Content type classification (lecture notes, textbook, handwritten, etc.)
- Main topics covered
- Difficulty level (beginner / intermediate / advanced)
- Key concepts and terms
- Structural observations (formatting, layout patterns)

#### Batch Extraction

The `GeminiExtractor` supports batch processing of multiple files in a single call, returning a dictionary mapping each file path to its extracted text.

---

### 📝 AI Summarization

The summarizer uses Gemini 2.0 Flash with tuned generation parameters (`temperature=0.3`, `top_p=0.8`, `top_k=40`) for focused, high-quality output.

#### Summary Modes

| Mode | Target Length | Max Tokens | Description |
|------|---------------|------------|-------------|
| **Short** | ~1/15th of source | 100 | Main points only, minimal detail |
| **Standard** | ~1/8th of source | 200 | Balanced coverage of key points and important details |
| **Long** | ~1/4th of source | 400 | Comprehensive overview with context and supporting details |
| **Bullet Points** | 5 key points | 300 | Concise bullet-point format (• style) |

#### Post-Processing Pipeline

All summaries pass through automatic post-processing:

- Removes residual markdown formatting artifacts
- Strips any prompt echoing from the model output
- Ensures proper sentence-ending punctuation
- Normalizes whitespace

#### Key Insights Extraction

A separate `get_key_insights()` method extracts 3–5 high-level takeaways from the text, focusing on the most important concepts, implications, or actionable information. Uses a slightly higher temperature (`0.4`) for more creative analysis.

---

### ❓ Question Generation

The question generator produces exam-style practice questions in three types, each with dedicated prompts and structured JSON output parsing.

#### Question Types

**Multiple Choice (MCQ)**

- 4 options per question (A/B/C/D)
- Plausible distractors that are clearly incorrect
- Correct answer with letter mapping and index tracking
- Detailed explanation for each answer

**True/False**

- Clear, definitive statements derived from the source text
- Balanced mix of true and false answers
- Each answer includes an explanation of why the statement is true or false

**Short Answer**

- Concise questions targeting specific facts, names, dates, or concepts
- Model answers are 2–4 words or short phrases
- Explanation provides additional context

#### Generation Controls

- **Selectable types** — Any combination of MCQ, True/False, and Short Answer
- **Per-type count** — Set the exact number of questions per type (3–15 via slider)
- **Organized output** — Questions are grouped by type in a fixed order: MCQ → Short Answer → True/False
- **Fallback handling** — If JSON parsing fails, the generator retries with a simplified prompt format to ensure questions are always returned

#### Structured Output

All questions follow a consistent schema:

```json
{
  "type": "Multiple Choice | True/False | Short Answer",
  "question": "Question text",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "answer": "Correct answer text",
  "correct_index": 1,
  "explanation": "Why this is the correct answer"
}
```

---

### 💾 Session & Data Management

NoteWise uses a lightweight JSON-based storage system (`SimpleStorage`) that persists all user activity locally without requiring a database.

#### What Gets Stored

| Data Type | File | Contents |
|-----------|------|----------|
| **Sessions** | `sessions.json` | Session ID, user ID, timestamps, status |
| **Summaries** | `summaries.json` | Summary text, type, word count, original text preview (first 500 chars), linked session |
| **Questions** | `questions.json` | Full question sets with all metadata, linked session |

#### Session Features

- **Auto-creation** — A new session is created automatically on app launch
- **UUID tracking** — Every session, summary, and question set gets a unique UUID
- **Timestamping** — Created and updated timestamps on all records
- **Session filtering** — Retrieve all summaries/questions for a specific session
- **History browsing** — View and reload any previously generated summaries or question sets from the History page

#### Data Cleanup

Built-in `delete_old_sessions()` method removes sessions older than a configurable number of days (default: 30), cascading the deletion to associated summaries and questions.

---

### 📤 Export System

The enhanced exporter supports multiple output formats with professional styling.

#### Export Formats

**Text Export (`.txt`)**

- Markdown-formatted text files
- Includes metadata header (timestamp, type, tool name)
- Clean formatting for both summaries and questions
- Original text preview appended to summary exports

**PDF Export (`.pdf`)**

- Professional academic styling via ReportLab
- Custom color-coded typography:
  - **Titles**: Dark blue, 18pt, centered
  - **Section headings**: Dark green, 14pt
  - **Body text**: 11pt with left indent
  - **Questions**: Dark blue, 12pt
  - **Answers**: Dark red, 10pt with deep indent
- Metadata table with generation timestamp
- A4 page size with proper margins

**Combined PDF Export**

- Single document containing both the summary and all practice questions
- Ideal for creating complete study packages
- Same professional styling as individual exports

#### Dynamic Filenames

Export filenames are automatically generated based on the question types present in the session:

- `NoteWise_MCQ.pdf` — MCQ only
- `NoteWise_MCQ_TrueFalse.pdf` — MCQ + True/False
- `NoteWise_MCQ_ShortAnswer_TrueFalse.pdf` — All three types

---

### 🎛️ Dashboard UI

The Streamlit dashboard provides a 4-page interactive interface:

#### Page 1: Text Extraction

- Drag-and-drop file uploader (PDF, PNG, JPG, JPEG, PPTX, PPT, TXT)
- Manual text input area as alternative
- Extracted text preview (first 500 characters)
- Word count display
- Content analysis expandable panel (for image uploads)
- Slide breakdown panel for PowerPoint files (slide count + average words per slide)

#### Page 2: Smart Summary

- Side-by-side layout: Original text | Generated summary
- Summary length selector (Short / Standard / Long)
- Bullet-point summary option
- Three export buttons: Text, PDF, Combined PDF (if questions exist)
- Auto-saves to storage after generation

#### Page 3: Practice Questions

- Checkbox selectors for question types (MCQ, True/False, Short Answer)
- Per-type question count slider (3–15)
- Total question count preview before generation
- Expandable question cards with question, options, answer, and explanation
- Export buttons: Text file and PDF
- Dynamic filenames based on selected types

#### Page 4: Session History

- Current session stats (word count, summary status, question count)
- Stored summaries browser (last 5, with load button)
- Stored questions browser (last 5, with load button)
- Clear session button
- Branded footer

#### Sidebar

- Page navigation dropdown
- API key input (password-masked, pre-filled from `.env`)
- Context-sensitive controls (summary length / question count based on active page)
- Gradient-styled NoteWise branding card

---

### 🛡️ Resilience & Error Handling

The application is designed with multiple layers of fault tolerance:

- **Graceful imports** — Every module import in `dashboard.py` is wrapped in try/except with availability flags. The app still loads if any module is missing, just with reduced functionality.
- **API validation** — The entry point (`main.py`) validates the Gemini API key on startup and blocks launch with helpful setup instructions if invalid.
- **JSON fallback** — Question generation has two-tier fallback: if structured JSON parsing fails, it retries with a simplified text prompt.
- **Error boundaries** — The main dashboard call is wrapped in a top-level try/except that catches and displays any unhandled errors with a recovery suggestion.
- **Safety settings** — Gemini Vision calls set all harm categories to `BLOCK_NONE` to prevent content filtering from blocking educational material extraction.

---

## 🏗️ Architecture

```text
NoteWise/
├── main.py                          # Entry point — configures Streamlit, validates API key
├── app/
│   └── dashboard.py                 # 726-line Streamlit UI (4 pages)
├── core/
│   ├── ocr/
│   │   └── gemini_extractor.py      # 285 lines — GeminiExtractor class
│   ├── summarizer/
│   │   └── gemini_summarizer.py     # 226 lines — GeminiTextSummarizer class
│   ├── question_gen/
│   │   └── gemini_generator.py      # 368 lines — GeminiQuestionGenerator class
│   ├── storage/
│   │   └── simple_storage.py        # 210 lines — SimpleStorage class
│   └── exports/
│       └── enhanced_exporter.py     # 355 lines — EnhancedExporter class
├── user_data/                       # Runtime JSON storage (gitignored)
├── docs/
│   └── overview.md                  # This file
├── requirements.txt                 # Python dependencies
├── .env                             # API keys & config (gitignored)
└── .gitignore
```

**Total codebase**: ~2,170 lines of Python across 8 source files.

---

## 🔄 Application Flow

```text
┌──────────────┐     ┌──────────────────┐     ┌───────────────────┐
│  Upload File │────▶│  Text Extraction │────▶│  Smart Summary    │
│ (PDF/IMG/PPT)│     │  (Gemini Vision) │     │  (Gemini Flash)   │
└──────────────┘     └──────────────────┘     └───────────────────┘
                              │                         │
                              ▼                         ▼
                     ┌──────────────────┐     ┌───────────────────┐
                     │  Content Analysis│     │  Question Gen     │
                     │  (Type/Topics/   │     │  (MCQ/TF/Short)   │
                     │   Difficulty)    │     └───────────────────┘
                     └──────────────────┘              │
                                                       ▼
                                              ┌───────────────────┐
                                              │  Export            │
                                              │  (PDF/TXT/Combined)│
                                              └───────────────────┘
                                                       │
                                                       ▼
                                              ┌───────────────────┐
                                              │  Session Storage   │
                                              │  (JSON persistence)│
                                              └───────────────────┘
```

---

## ⚙️ Tech Stack

| Layer              | Technology                          | Version    |
|--------------------|-------------------------------------|------------|
| AI Engine          | Google Generative AI (Gemini 2.0)   | 0.8.5      |
| AI Model           | gemini-2.0-flash-exp                | —          |
| Web Framework      | Streamlit                           | 1.37.1     |
| PDF Parsing        | PDFplumber                          | 0.11.7     |
| PPTX Parsing       | python-pptx                         | 0.6.23     |
| PDF Generation     | ReportLab                           | 4.4.3      |
| Image Handling     | Pillow                              | ≥ 10.4.0   |
| Environment Config | python-dotenv                       | 1.1.1      |
| Text Processing    | regex                               | 2024.7.24  |

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

1. **Gemini-only stack** — No local ML models. All AI processing uses the Gemini API, keeping the app lightweight (~500MB install) with no GPU requirement.
2. **JSON storage** — Simple file-based persistence instead of a database, making the app portable and zero-config. All data lives in `user_data/`.
3. **Modular core** — Each capability (OCR, summarization, question gen, export) is a self-contained class under `core/`, making it trivial to swap implementations or add new backends.
4. **Graceful degradation** — Every import in `dashboard.py` is wrapped in try/except. If a module isn't available, the app still loads with reduced functionality.
5. **Prompt engineering** — Each AI feature uses carefully crafted prompts with specific formatting instructions and JSON output schemas, with fallback prompts for reliability.
6. **Tuned generation config** — Temperature, top_p, top_k, and max_output_tokens are individually tuned per use case (low temperature for summarization, slightly higher for insights extraction).
