from collections import defaultdict
import xml.etree.ElementTree as ET
import json
import re

class ExtractEntity:
    """
    Extract entity info from llm reposne
    """
    def __init__(self):
        pass
    def get_xml_from_text(self, text):
        """
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
                    return xml_data
                except ET.ParseError as e:
                    print(f"Error parsing XML: {e}")
                    return None
        except Exception as e:
            print(e)
            return None
    def xml_to_json(self, xml_data: ET):
        """
        """
        def recurse(elem):
            children = list(elem)
            if not children:
                return elem.text.strip() if elem.text and elem.text.strip() else None
            
            result = defaultdict(list)
            for child in children:
                child_result = recurse(child)
                result[child.tag].append(child_result)
        
            # Flatten lists with one item
            return {tag: vals[0] if len(vals) == 1 else vals for tag, vals in result.items()}
    
        return json.dumps({xml_data.tag: recurse(xml_data)}, indent=4)
    def extract_entities(self, llm_respone: str):
        """
        """
        try:
            entity_xml = self.get_xml_from_text(llm_respone)
            print(entity_xml)
            entity_json = self.xml_to_json(entity_xml)
            return entity_json
        except Exception as e:
            print(e)
