import pytesseract
from PIL import Image
import pdf2image
import docx
import io

def extract_text(file):
    file_type = file.type
    
    if "image" in file_type:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
    
    elif file_type == "application/pdf":
        images = pdf2image.convert_from_bytes(file.read())
        text = "\n".join([pytesseract.image_to_string(img) for img in images])
    
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(io.BytesIO(file.read()))
        text = "\n".join([para.text for para in doc.paragraphs])
    
    else:
        text = "Unsupported file format"
    
    return text
