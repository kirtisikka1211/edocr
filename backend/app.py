# from fastapi import FastAPI, File, UploadFile
# from typing import Dict
# import sys
# import os
# from utils.pdf_parser import PDFParser
# from utils.preprocess_image import ImagePreprocessor
# from ocrengine.table_extractor import ExctractTables
# from ocrengine.text_extractor import TextExtractor
# from utils.prompt_factory import PROMPT_ENIITY_AND_NOTE_EXTRACTION_TEMPLATE
# from llm.llms import LlmInferencer
# from entity_extractor.entity_extractor import ExtractEntity
# import cv2
# import time
# import uvicorn
# import json
# from fastapi.responses import JSONResponse

# parser = PDFParser()
# img_preprocessor = ImagePreprocessor()
# table_extractor = ExctractTables()
# text_extractor = TextExtractor()
# llm_inferencer = LlmInferencer()
# entity_extractor = ExtractEntity()
# app = FastAPI()

# def write_to_file(final_result, filename="output.json"):
#     with open(filename, "w") as json_file:
#         json.dump(final_result, json_file, indent=4)
#     print(f"JSON data successfully written to {filename}")

# @app.post("/extract_info")
# async def extract_information(file: UploadFile = File(...)):
#     """
#     endpoint accept pdf file and return extracted entities
#     """
#     if not file.filename.endswith(".pdf"):
#         return {"error": "Only PDF files are allowed"}
    
#     # Convert PDF to images (without saving)
#     images = await parser.convert_pdf_to_images(file)

#     preprocessed_img = img_preprocessor.preprocess_images(images)

#     start_time = time.time()
#     result = text_extractor.get_text_block(preprocessed_img)
#     end_time = time.time()
#     print(start_time-end_time)
#     llm_response = {}
#     final_result = {}
#     # pass to llm
#     for item in result:
#         for key, ocr_text in item.items():
#             prompt = PROMPT_ENIITY_AND_NOTE_EXTRACTION_TEMPLATE.format(ocr_text=ocr_text)
#             llm_result = llm_inferencer.inference_groq(prompt=prompt)
#             print(llm_result)
#             llm_response[key] = llm_result
#             final_result[key] = entity_extractor.extract_entities(llm_result)
#     write_to_file(final_result)
#     return JSONResponse(content=final_result, status_code=200)
#     """ 
#     # Option 1: Display using OpenCV (opens separate windows)
#     for i, img in enumerate(preprocessed_img):
#         cv2.imshow(f"Page {i+1}", img)
#         cv2.resizeWindow(f"Page {i+1}", 800, 600)  # Set width and height
#     cv2.waitKey(0)  # Wait for key press to close windows
#     cv2.destroyAllWindows()
#     """
# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

# app.py

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
import time
import json
import uvicorn

# Initialize components
parser = PDFParser()
img_preprocessor = ImagePreprocessor()
table_extractor = ExctractTables()
text_extractor = TextExtractor()
llm_inferencer = LlmInferencer()
entity_extractor = ExtractEntity()

app = FastAPI()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Optional: for saving to file for inspection
def write_to_file(final_result, filename="output.json"):
    with open(filename, "w") as json_file:
        json.dump(final_result, json_file, indent=4)
    print(f"JSON data successfully written to {filename}")


@app.post("/extract_info")
async def extract_information(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Accepts a PDF file, extracts information, saves it to DB, and returns extracted entities.
    """
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

    llm_response = {}
    final_result = {}

    # Save PDF entry
    # pdf_content = await file.read()
    # pdf_obj = PDF(name=file.filename, pdf_file=pdf_content)
    # db.add(pdf_obj)
    # db.commit()
    # db.refresh(pdf_obj)

    for idx, item in enumerate(result):
        for key, ocr_text in item.items():
            # Prompt LLM
            prompt = PROMPT_ENIITY_AND_NOTE_EXTRACTION_TEMPLATE.format(ocr_text=ocr_text)
            llm_result = llm_inferencer.inference_groq(prompt=prompt)
            print(f"LLM Response for Page {idx}:", llm_result)

            llm_response[key] = llm_result
            entities = entity_extractor.extract_entities(llm_result)
            print("entities",entities)
            final_result[key] = entities
            print("fina;",final_result)
            entities = json.loads(entities)
            print(final_result)
            page_key = str(idx)  
            page_id = f"{file.filename}_{page_key}"  

            extracted_data = entities.get("ExtractedData", {})

            print("Extracted data:", extracted_data)

            # drawing = Drawing(
            #     page_id=f"{file.filename}_{str(idx)}",
            #     pdf_id=pdf_obj.pdf_id,
            #     productNumber=extracted_data.get("ProductNumber"),
            #     productFamily=extracted_data.get("ProductFamily"),
            #     drawingNumber=extracted_data.get("DrawingNumber"),
            #     engineerName=extracted_data.get("EngineerName"),
            #     revision=extracted_data.get("Revision"),
            #     approvalDate=extracted_data.get("ApprovalDate"),
            #     status=extracted_data.get("Status")
            # )

            # print("Drawing to insert:", drawing.__dict__)
            # db.add(drawing)
            # db.commit()


            # Save Notes (if any)
            notes = extracted_data.get("Notes", {}).get("Note", [])

            
    #         if notes:
    #             note = Note(
    #                 page_id=drawing.page_id,
    #                 noteText=notes  # JSON array
    #             )
    #             db.add(note)
    # db.commit()

    write_to_file(final_result)
    return JSONResponse(content=final_result, status_code=200)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
