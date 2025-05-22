from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db import SessionLocal
from models import PDF, Drawing, Note
from utils.pdf_parser import PDFParser
from utils.preprocess_image import ImagePreprocessor
from ocrengine.table_extractor import ExctractTables
from ocrengine.text_extractor import TextExtractor
from utils.prompt_factory import PROMPT_ENIITY_AND_NOTE_EXTRACTION_TEMPLATE
from llm.llms import LlmInferencer
from entity_extractor.entity_extractor import ExtractEntity
from pydantic import BaseModel
from typing import Dict, Any
import time
import json
import uvicorn

# ----- Pydantic Model for Request -----
class SaveRequest(BaseModel):
    filename: str
    extracted_entities: Dict[str, Any]

# ----- Initialize FastAPI and Components -----
app = FastAPI()

parser = PDFParser()
img_preprocessor = ImagePreprocessor()
table_extractor = ExctractTables()
text_extractor = TextExtractor()
llm_inferencer = LlmInferencer()
entity_extractor = ExtractEntity()

# ----- DB Dependency -----
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----- Optional JSON Writer -----
def write_to_file(final_result, filename="output.json"):
    with open(filename, "w") as json_file:
        json.dump(final_result, json_file, indent=4)
    print(f"JSON data successfully written to {filename}")

# ----- PDF Upload and Info Extraction -----
@app.post("/extract_info")
async def extract_information(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".pdf"):
        return JSONResponse(content={"error": "Only PDF files are allowed"}, status_code=400)

    # Convert PDF to images
    images = await parser.convert_pdf_to_images(file)
    preprocessed_img = img_preprocessor.preprocess_images(images)

    # Extract OCR text blocks
    start_time = time.time()
    result = text_extractor.get_text_block(preprocessed_img)
    end_time = time.time()
    print("Text extraction time:", end_time - start_time)

    final_result = {}

    # Save PDF entry
    pdf_content = await file.read()
    pdf_obj = PDF(name=file.filename, pdf_file=pdf_content)
    db.add(pdf_obj)
    db.commit()
    db.refresh(pdf_obj)

    for idx, item in enumerate(result):
        for key, ocr_text in item.items():
            prompt = PROMPT_ENIITY_AND_NOTE_EXTRACTION_TEMPLATE.format(ocr_text=ocr_text)
            llm_result = llm_inferencer.inference_groq(prompt=prompt)

            print(f"LLM Response for Page {idx}:", llm_result)

            extracted_entities = entity_extractor.extract_entities(llm_result)
            print("Extracted Entities:", extracted_entities)

            # Store result
            final_result[str(idx)] = extracted_entities

    write_to_file(final_result)

    return JSONResponse(
        content={
            "filename": file.filename,
            "extracted_entities": final_result
        },
        status_code=200
    )

# ----- Save Extracted Data to DB -----
@app.post("/save_db")
async def save_extracted_data(data: SaveRequest, db: Session = Depends(get_db)):
    try:


        
        filename = data.filename
        extracted_entities = data.extracted_entities

        if not filename or not extracted_entities:
            return JSONResponse(content={"error": "Missing filename or extracted_entities"}, status_code=400)

        # Fetch PDF entry
        pdf_obj = db.query(PDF).filter(PDF.name == filename).first()
        if not pdf_obj:
            return JSONResponse(content={"error": "PDF not found in database"}, status_code=404)

        for page_num, entity_str in extracted_entities.items():
            try:
                entities = json.loads(entity_str) if isinstance(entity_str, str) else entity_str
                extracted_data = entities.get("ExtractedData", {})

                drawing = Drawing(
                    page_id=f"{filename}_{page_num}",
                    pdf_id=pdf_obj.pdf_id,
                    productNumber=extracted_data.get("ProductNumber"),
                    productFamily=extracted_data.get("ProductFamily"),
                    drawingNumber=extracted_data.get("DrawingNumber"),
                    engineerName=extracted_data.get("EngineerName"),
                    revision=extracted_data.get("Revision"),
                    approvalDate=extracted_data.get("ApprovalDate"),
                    status=extracted_data.get("Status")
                )
                db.add(drawing)
                db.commit()

                notes = extracted_data.get("Notes", {}).get("Note", [])
                if notes:
                    note_text = notes if isinstance(notes, str) else "\n".join(notes)
                    note = Note(page_id=drawing.page_id, noteText=note_text)
                    db.add(note)
                    db.commit()

            except Exception as e:
                print(f"Error processing page {page_num}: {e}")
                continue

        return JSONResponse(content={"message": "Data saved successfully"}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": f"Server error: {str(e)}"}, status_code=500)

# ----- Uvicorn Entrypoint -----
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
