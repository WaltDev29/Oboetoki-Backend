import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

def parse_ocr_text_to_words(raw_text: str) -> list[dict]:
    """
    OCR로 추출된 텍스트를 LLM에 전달하여 단어와 뜻 쌍으로 구성된 딕셔너리 리스트를 반환합니다.
    """
    if not raw_text or not raw_text.strip():
        return []

    prompt = f"""
다음은 사용자가 외국어 단어장을 사진으로 찍어서 OCR로 추출한 텍스트입니다.
텍스트에는 원어(영어, 일본어 등)와 한국어 뜻이 섞여있거나 오타가 있을 수 있습니다.
이 텍스트를 분석하여 원어와 한국어 뜻의 쌍을 추출해 주세요.

추출된 데이터는 반드시 아래의 JSON 배열 형식으로만 응답해 주세요. (추가 설명이나 마크다운 백틱 없이 순수 JSON만 반환)
[
  {{"original": "단어", "translated": "한국어 뜻"}},
  ...
]

[추출할 텍스트]
{raw_text}
"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that parses raw OCR text of vocabulary books into clean JSON arrays containing original words and their translations. You must return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
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
        print(f"LLM Parsing Error: {e}")
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
