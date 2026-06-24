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

[요구사항]
1. `source_language`: 각 단어의 원본 언어를 판별하여 ISO 언어 코드(예: 'ja' (일본어), 'en' (영어) 등)로 작성하세요.
2. `original`에는 한국어가 들어갈 수 없습니다.
3. `reading`: 원어가 일본어 한자처럼 읽는 법(요미가나, 발음 기호 등)이 따로 표기되어 있거나 필요한 경우, 이 필드에 작성하세요. 영어의 경우 발음 기호를 입력하고, 발음 표기가 불필요한 언어라면 null로 설정하세요.
4. `translated`: 한국어 뜻을 작성하세요.
5. `original`과 `translated`에는 같은 언어를 입력하지 마세요.

추출된 데이터는 반드시 아래의 JSON 배열 형식으로만 응답해 주세요. (추가 설명이나 마크다운 백틱 없이 순수 JSON만 반환)
[
  {"original": "단어", "reading": "요미가나 혹은 발음기호", "translated": "한국어 뜻", "source_language": "ja"},
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
