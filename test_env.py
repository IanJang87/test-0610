import os
from dotenv import load_dotenv

print("=== Testing Environment Variable Loading ===\n")

# dashboard.py와 동일한 방식으로 로드
env_file_path = os.path.join(os.path.dirname(__file__), '.env')
print(f"env_file_path: {env_file_path}")
print(f"File exists: {os.path.exists(env_file_path)}")

# .env 파일 로드
load_dotenv(env_file_path)

# 환경변수 읽기
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_model = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

print(f"\n=== Loaded Values ===")
print(f"GEMINI_API_KEY: {gemini_api_key}")
print(f"GEMINI_MODEL: {gemini_model}")

print(f"\n=== Condition Checks ===")
print(f"gemini_api_key is not None: {gemini_api_key is not None}")
print(f"gemini_api_key value check: '{gemini_api_key}'")
print(f"gemini_api_key != 'your_gemini_api_key_here': {gemini_api_key != 'your_gemini_api_key_here'}")

# 조건 확인
condition_result = gemini_api_key and gemini_api_key != "your_gemini_api_key_here"
print(f"Both conditions (should be True): {condition_result}")

# genai 테스트
print(f"\n=== Gemini API Configuration ===")
try:
    import google.generativeai as genai
    if gemini_api_key and gemini_api_key != "your_gemini_api_key_here":
        genai.configure(api_key=gemini_api_key)
        print("[SUCCESS] genai.configure() called successfully")
    else:
        print("[WARNING] Condition check failed - genai.configure() not called")
except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")

print("\n=== Test Complete ===")
