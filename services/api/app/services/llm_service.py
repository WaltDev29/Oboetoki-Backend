import os
import json
import base64
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

def parse_image_to_words(image_bytes: bytes) -> list[dict]:
    """
    이미지 바이트 데이터를 OpenAI Vision API(gpt-4o 등)로 바로 전송하여
    단어와 뜻 쌍으로 구성된 딕셔너리 리스트를 반환합니다. Tesseract를 대체합니다.
    """
    if not image_bytes:
        return []

    # 이미지를 base64로 인코딩
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    prompt = """
사용자가 외국어 단어장을 사진으로 찍어 올렸습니다.
이 이미지에 있는 텍스트를 분석하여 원어(영어, 일본어 등)와 한국어 뜻의 쌍을 완벽하게 추출해 주세요.

추출된 데이터는 반드시 아래의 JSON 배열 형식으로만 응답해 주세요. (추가 설명이나 마크다운 백틱 없이 순수 JSON만 반환)
[
  {"original": "단어", "translated": "한국어 뜻"},
  ...
]
"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.1,
            max_tokens=1500,
        )
        content = response.choices[0].message.content.strip()
        # 혹시라도 마크다운 코드 블록이 섞여 있다면 제거
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
            
        parsed_data = json.loads(content.strip())
        return parsed_data
    except Exception as e:
        print(f"OpenAI Vision Parsing Error: {e}")
        return []

def get_quote_of_the_day() -> str:
    """
    외국어 학습에 동기부여가 되는 오늘의 한 마디를 생성합니다.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a motivational assistant for language learners."},
                {"role": "user", "content": "외국어 학습에 동기부여가 되는 짧고 인상 깊은 명언이나 한 마디를 한국어로 하나만 말해줘. 1~2문장 내외로."}
            ],
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"LLM Quote Error: {e}")
        return "꾸준함이 모든 것을 이깁니다. 오늘도 화이팅!"
