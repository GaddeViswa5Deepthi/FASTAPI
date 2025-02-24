from fastapi import FastAPI
import PyPDF2
import os  

app = FastAPI()

def extract_pdf_form_fields(pdf_path, output_file):
    """Extract form fields from a PDF, save output to a file."""
    
    if not os.path.exists(pdf_path):
        error_message = f"File not found: {pdf_path}"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(error_message)
        return {"error": error_message}

    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

    
        fields = reader.get_fields()
        if fields:
            form_fields = {
                key: (value.get('/V', 'N/A') if isinstance(value, dict) else 'N/A')
                for key, value in fields.items()
            }

            
            with open(output_file, "w", encoding="utf-8") as file:
                for name, value in form_fields.items():
                    file.write(f"{name}: {value}\n")

            return form_fields
        else:
            message = "No form fields found in the PDF"
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(message)
            return {"message": message}


pdf_file_path =  r"C:\Users\91849\OneDrive\Documents\fastapi\task1\pypdf2.pdf"


output_text_file = r"C:\Users\91849\OneDrive\Documents\fastapi\task1\output1.txt"


fields = extract_pdf_form_fields(pdf_file_path, output_text_file)


print(f"✅ Extracted data saved to: {output_text_file}")
