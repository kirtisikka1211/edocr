import io
import cv2
import numpy as np
from typing import List
from paddleocr import PaddleOCR
from utils.log_config import setup_logger
from utils.helper_functions import convert_numpy_images_to_bytes
import os
import sys

# instansiate a logger 
logger = setup_logger(__name__)

class TextExtractor:
    """
    Extract all text from preprocessed images
    """
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Configure as needed
    
    def extract_text(self, img_bytes: io.BytesIO)-> str:
        """
        Extract text from image
        PARAMS:
            img_bytes io.BytesIO: image in bytes
        RETURNS:
            extracted_text str: extracted text            
        """
        try:
            
            extracted_text = ""

            # Convert BytesIO to OpenCV image (numpy array)
            img_bytes.seek(0)
            file_bytes = np.asarray(bytearray(img_bytes.read()), dtype=np.uint8)
            img_np = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            # OCR on the image
            result = self.ocr.ocr(img_np, cls=True)
            for line in result:
                for word in line:
                    extracted_text += word[1][0] + "\n"
        except Exception as e:
            raise Exception(str(e))
        return extracted_text
    
    def get_text_block(self, preprocessed_images: List[io.BytesIO]) -> List[dict]:
        """
        extract text from each preprocessed images
        PARAMS:
            preprocessed_images List[io.BytesIO]: preprocessed images bytes
        RETURNS:
            result List[dict]: text extracted from all pages 
        """
        results = []
        preprocessed_images_bytes = convert_numpy_images_to_bytes(preprocessed_images)
        for page_idx, img in enumerate(preprocessed_images_bytes):
            try:
                text_extracted = self.extract_text(img)
                results.append({page_idx+1: text_extracted})
            except Exception as e:
                logger.error(f"Error extracting text from page {page_idx}: {str(e)}")
        logger.info("text block Extracted from all images")
        return results