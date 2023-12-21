from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
import os
from ocr_module import run_ocr
from text_extraction_module import extract_text_and_formatting, perform_ner, create_docx_with_ner
from image import pdf_to_images  
from object_detection_module import object_detection

app = FastAPI()

model_path = 'yolov8n.pt'  # Path to your YOLO model

upload_dir = "uploaded_files"
os.makedirs(upload_dir, exist_ok=True)

@app.post("/upload/")
async def upload_pdf(file: UploadFile):
    file_location = os.path.join(upload_dir, file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())

    # Process the PDF
    docx_path = process_pdf(file_location)

    # Return the processed DOCX file
    return FileResponse(docx_path, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', filename=os.path.basename(docx_path))

import os

# Assuming other imports and function definitions are here

def process_pdf(pdf_path: str):
    # Check if the input PDF file exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Input PDF file not found at {pdf_path}")
    print(f"Processing PDF: {pdf_path}")  # Debug print

    # Step 1: Run OCR to generate a new PDF
    ocr_pdf_path = os.path.join('uploaded_files', os.path.basename(pdf_path).replace('.pdf', '_ocr.pdf'))
    print(f"OCR PDF Path: {ocr_pdf_path}")  # Debug print
    run_ocr(pdf_path, ocr_pdf_path)

    # Verify OCR PDF exists
    if not os.path.exists(ocr_pdf_path):
        raise FileNotFoundError(f"OCR PDF file not found at {ocr_pdf_path}")

    # Step 2: Convert OCR PDF to images for object detection
    images = pdf_to_images(ocr_pdf_path)

    # Step 3: Perform object detection on the images
    detection_data = object_detection(images, model_path)

    # Step 4: Extract text and perform NER
    extracted_data = extract_text_and_formatting(ocr_pdf_path)
    ner_results = perform_ner(extracted_data)

    # Step 5: Create a DOCX file
    docx_path = pdf_path.rsplit('.', 1)[0] + '.docx'
    create_docx_with_ner(ner_results, docx_path)

    return docx_path

# Your FastAPI route and other logic

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
