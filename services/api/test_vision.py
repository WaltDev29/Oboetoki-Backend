import sys
import os
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv

# .env.api 파일 경로를 찾아 환경 변수 로드 (OPENAI_API_KEY 적용을 위해)
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../docker/env/.env.api'))
load_dotenv(env_path)

try:
    from app.services.llm_service import parse_image_to_words
except ImportError as e:
    print("모듈을 불러오지 못했습니다. 이 스크립트는 'services/api/' 폴더 안에서 실행해야 합니다.")
    print(e)
    sys.exit(1)

def main():
    # Tkinter를 사용해 파일 선택 다이얼로그 열기
    root = tk.Tk()
    root.withdraw() # 빈 창 숨기기
    
    # 윈도우 환경을 위한 최상단 노출 속성
    root.attributes('-topmost', True)
    
    print("이미지 파일을 선택해주세요 창이 열립니다...")
    file_path = filedialog.askopenfilename(
        title="단어장 이미지 선택",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    
    if not file_path:
        print("파일 선택이 취소되었습니다. 종료합니다.")
        return
        
    print(f"\n[진행 1/2] 선택된 파일: {file_path}")
    
    try:
        with open(file_path, "rb") as f:
            image_bytes = f.read()
            
        print("[진행 2/2] OpenAI GPT-4o Vision을 통해 이미지 분석 및 단어 추출 중...")
        
        parsed_words = parse_image_to_words(image_bytes)
        
        print("\n=== [최종 LLM 파싱 결과 (JSON)] ===")
        import json
        print(json.dumps(parsed_words, ensure_ascii=False, indent=2))
        print("===================================")
        
    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")

if __name__ == "__main__":
    main()
