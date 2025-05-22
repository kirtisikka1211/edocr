import re
import cv2
import io
import numpy as np
from typing import List
import xml.etree.ElementTree as ET

def convert_numpy_images_to_bytes(images: List[np.ndarray], format: str = ".png") -> List[io.BytesIO]:
    """
    Convert list of NumPy image arrays to BytesIO objects.
    Args:
        images: List of NumPy image arrays (BGR format, e.g., from OpenCV)
        format: Image encoding format (default is PNG)
    
    Returns:
        List of BytesIO image objects
    """
    image_bytes_list = []
    for id, img in enumerate(images):
        try:
            success, encoded_image = cv2.imencode(format, img)
            if success:
                image_bytes = io.BytesIO(encoded_image.tobytes())
                image_bytes_list.append(image_bytes)
            else:
                raise Exception(f"Image encoding failed for page {id +1 }")
        except Exception as e:
            raise Exception(f"numpy to bytes image conversion failed: {str(e)}")
    return image_bytes_list

def get_xml_from_text(text: str)-> ET.Element:
    """
    Extract xml from text
    PARAMS:
        text str: text from xml to be extracted
    Returns:
        xml_data ET.Element:
    """
    try:
        # Regex pattern to capture everything between the ```xml and ``` markers
        pattern = r'```xml\n(.*?)\n```'
        # Extracting XML string using regex with re.DOTALL to handle multiline XML
        match = re.search(pattern, text, re.DOTALL)
        if match:
            xml_str = match.group(1)
            try:
                # Parsing the extracted XML string into an ElementTree object
                xml_data = ET.fromstring(xml_str)
            except ET.ParseError as e:
                raise Exception(f"Parsing xml string to Elementtree failed : {str(e)}")
    except Exception as e:
       raise Exception(f"xml Parsing error: {str(e)}")
    return xml_data