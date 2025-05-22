import fitz  # PyMuPDF
import numpy as np
import cv2
from typing import List
from fastapi import UploadFile
from utils.log_config import setup_logger

# initialise loger object
logger = setup_logger(__name__)

class PDFParser:
    def __init__(self, scale_factor: float = 3.0):
        """
        Initializes the PDF parser with a scale factor for high-resolution rendering.
        """
        self.scale_factor = scale_factor  # Scale for better image quality

    async def convert_pdf_to_images(self, file: UploadFile) -> List[np.ndarray]:
        """
        Converts a PDF file object into a list of images (one per page).
        
        :param file: UploadFile (FastAPI file object)
        :return: List of NumPy arrays representing each page as an image
        """
        try:
            # Read PDF bytes
            pdf_bytes = await file.read()

            # Open the PDF from bytes
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")

            images = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]

                # Render page as a high-resolution image
                pix = page.get_pixmap(matrix=fitz.Matrix(self.scale_factor, self.scale_factor))

                # Convert to NumPy array
                img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)

                # Convert RGB to BGR (OpenCV format)
                if pix.n == 3:
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                elif pix.n == 4:
                    img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)

                images.append(img)
        except Exception as e:
            logger.error(f"Error parsing pdf :{str(e)}")
        logger.info("All Images extracted from pdf")
        return images
