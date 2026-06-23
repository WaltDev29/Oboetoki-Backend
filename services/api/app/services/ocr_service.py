import pytesseract
from PIL import Image
import io

def extract_text_from_image(image_bytes: bytes) -> str:
    """
    이미지 바이트 데이터를 받아 Tesseract OCR을 사용하여 텍스트를 추출합니다.
    언어는 한국어, 영어, 일본어를 기본으로 인식합니다.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        # 언어 팩: 한국어, 영어, 일본어 동시 인식
        text = pytesseract.image_to_string(image, lang='kor+eng+jpn')
        return text.strip()
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""
