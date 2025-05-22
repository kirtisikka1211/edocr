import io
import json
from typing import List
from img2table.document import Image
from img2table.ocr import PaddleOCR
from utils.log_config import setup_logger
from utils.helper_functions import convert_numpy_images_to_bytes

# instansiate a logger 
logger = setup_logger(__name__)

class ExctractTables:
    """
    extract tables from preproceesd images
    """
    def __init__(self):
        self.ocr = PaddleOCR(lang="en")

    def convert_to_json(self, table, table_index)->dict:
        """
        Convert extracted table into a structured JSON format.
        PARAMS:
            table ExtractedTable: table extracted
            table_index int: table index
        Returns:
            table_data dict: table data
        """
        try:
            table_data = {
                "table_index": table_index,
                "cells": []
                }
            for row_idx, row in enumerate(table.content.values()):
                for col_idx, cell in enumerate(row):
                    cell_info = {
                        "row": row_idx,
                        "col": col_idx,
                        "value": cell.value.strip() if cell.value else "",  # Cleaned value
                        #"bbox": [cell.bbox.x1, cell.bbox.y1, cell.bbox.x2, cell.bbox.y2]
                    }
                    table_data["cells"].append(cell_info)
        except Exception as e:
            raise Exception(str(e)) 
        return table_data

    def get_tables(self, preprocessed_images: List[io.BytesIO]) -> List[dict]:
        """
        Accepts a list of preprocessed images in BytesIO format and extracts tables.
        PARAMS:
            preprocessed_images List[io.BytesIO]: all preprocessed images
        RETURNS:
            all_tables List[dict]: 
        """
        all_tables = []
        preprocessed_images_bytes = convert_numpy_images_to_bytes(preprocessed_images)
        for page_idx, image_bytes in enumerate(preprocessed_images_bytes):
            try:
                # Load image from BytesIO
                doc = Image(image_bytes)

                # Extract tables
                tables = doc.extract_tables(
                    ocr=self.ocr,
                    implicit_rows=False,
                    implicit_columns=False,
                    borderless_tables=False,
                    min_confidence=50
                )

                structured_tables = {
                    "page": page_idx + 1,
                    "tables": [self.convert_to_json(table, table_idx + 1) for table_idx, table in enumerate(tables)]
                }

                all_tables.append(structured_tables)
            except Exception as e:
                logger.error(f"Exception in extracting tables from page {page_idx + 1}:", e)
                continue
        logger.info("All tables extracted from all pages")
        return all_tables
