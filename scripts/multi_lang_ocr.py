import pytesseract
from PIL import Image
import pdf2image
import io
from googletrans import Translator

def extract_and_translate(file):
    file_type = file.type
    translator = Translator()
    
    if "image" in file_type:
        image = Image.open(file)
        extracted_text = pytesseract.image_to_string(image, lang='eng+hin+tam+kan+tel')
    
    elif file_type == "application/pdf":
        images = pdf2image.convert_from_bytes(file.read())
        extracted_text = "\n".join([pytesseract.image_to_string(img, lang='eng+hin+tam+kan+tel') for img in images])
    
    else:
        extracted_text = "Unsupported file format"
    
    translated_text = translator.translate(extracted_text, dest='en').text
    
    return extracted_text, translated_text
