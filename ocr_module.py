import subprocess
import os

def run_ocr(input_pdf, output_pdf):
    print(f"Running OCR on: {input_pdf}")
    print(f"Expected OCR output: {output_pdf}")

    # Check if input PDF exists
    if not os.path.exists(input_pdf):
        raise FileNotFoundError(f"Input PDF file not found at {input_pdf}")

    # Ensure output directory exists
    output_dir = os.path.dirname(output_pdf)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # Run OCRmyPDF
    result = subprocess.run(["ocrmypdf", input_pdf, output_pdf], capture_output=True, text=True)

    # Print OCR output for debugging
    print(f"OCR Output: {result.stdout}")
    print(f"OCR Errors: {result.stderr}")

    if not os.path.exists(output_pdf):
        raise FileNotFoundError(f"OCR process failed to create output file at {output_pdf}")
