import os
import fitz  # PyMuPDF
from typing import Dict

def extract_and_analyze_image(filename: str, page_number: int) -> str:
    """
    Extracts the first image from a specific page of a PDF document.
    
    Args:
        filename (str): The name of the file stored in the data directory (e.g., 'AI_FreeBook.pdf')
        page_number (int): The 1-indexed page number where the image is located.
        
    Returns:
        str: A message containing the URL of the extracted image if successful, or an error message.
    """
    file_path = os.path.join("data", filename)
    
    if not os.path.exists(file_path):
        return f"Error: File '{filename}' not found."
        
    if not filename.lower().endswith(".pdf"):
        return "Error: Image extraction is only supported for PDF files."

    try:
        pdf_document = fitz.open(file_path)
        
        # Adjust for 0-indexed PyMuPDF pages
        target_page_index = page_number - 1
        
        if target_page_index < 0 or target_page_index >= len(pdf_document):
            return f"Error: Page {page_number} is out of range for this document."
            
        page = pdf_document.load_page(target_page_index)
        image_list = page.get_images(full=True)
        
        if not image_list:
            return f"Error: No images found on page {page_number}."
            
        # Grab the first image on the page
        img_info = image_list[0]
        xref = img_info[0]
        
        extracted_image = pdf_document.extract_image(xref)
        image_bytes = extracted_image["image"]
        image_ext = extracted_image["ext"]
        
        # Ensure images directory exists
        images_dir = os.path.join("data", "images")
        os.makedirs(images_dir, exist_ok=True)
        
        # Save image
        safe_filename = filename.replace(" ", "_").replace(".pdf", "")
        image_filename = f"{safe_filename}_page{page_number}.{image_ext}"
        image_save_path = os.path.join(images_dir, image_filename)
        
        with open(image_save_path, "wb") as f:
            f.write(image_bytes)
            
        pdf_document.close()
        
        image_url = f"http://localhost:8000/api/images/{image_filename}"
        
        return f"SUCCESS! Image extracted. The image URL is: {image_url}"
        
    except Exception as e:
        return f"Error extracting image: {str(e)}"
