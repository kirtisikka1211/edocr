# EDOCR

**Document Extraction & Search Platform**



---

## Description

EDOCR is a  platform designed to handle engineering drawings pdfs uploads, extract structured data from them, and enable fast, efficient search over extracted content. 

---

## Features
-  **Upload**  
Upload engineering drawings  PDFs for automated data extraction.

- **Extract**  
Automatically extract structured data like tables, text, and entities from your documents.

- **Search**  
Easily search and retrieve data from your extracted document information.

---

## Folder Structure

```bash
edocr/
│-- backend/
│   │-- app.py
│   │-- entity_extractor/
│   │   └── entity_extractor.py
│   │-- gdts/
│   │   └── extract_dimension.py
│   │-- llm/
│   │   └── llms.py
│   │-- ocrengine/
│   │   ├── table_extractor.py
│   │   └── text_extractor.py
│   │-- scripts/
│   │   ├── create_tables.py
│   │   ├── models.py
│   │   └── schema.py
│   │-- utils/
│   │   ├── __init__.py
│   │   ├── helper_functions.py
│   │   ├── log_config.py
│   │   ├── pdf_parser.py
│   │   ├── preprocess_image.py
│   │   └── prompt_factory.py
│-- frontend/
│   └── app.py
│-- .env
│-- .gitignore
│-- README.md
│-- requirements.txt
```


---
##  API Endpoints

- `POST /extract_info/`  
  Extract text, tables, and metadata from uploaded PDFs.

- `POST /save_db`  
  Save extracted information to the database.

- `POST /preprocess_and_extract_dimensions`  
  Run preprocessing on images and extract GD&T dimensions.

## 🔧 Installation




### Clone the Repository

```bash
git clone <url>
cd edocr
```

### Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```


### Configure Environment Variables

Create a `.env` file in the root directory and define the following variables:

```env
LOG_ROLE_DAYS=""
LOG_DIR="logs"
GROQ_API_KEY=""
```

### Set Up the Database

```bash
python backend/scripts/schema.py
```

---

## 🚀 Running the Application

### Backend

```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
streamlit run app.py
```

---

## 🔍 How It Works

1. **Upload PDFs**  
   Users upload engineering PDFs via the frontend interface.

2. **OCR & Parsing**  
   The system extracts text, tables, and entities using a combination of OCR and custom parsing.

3. **Data Storage**  
   Extracted data is stored in a structured PostgreSQL database.

4. **Search Interface**  
   Users can search and filter extracted information via a simple search UI.

---

