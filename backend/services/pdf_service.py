import io
from PyPDF2 import PdfReader

class PDFService:
    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text
        except Exception as e:
            raise ValueError(f"Failed to read PDF file: {str(e)}")