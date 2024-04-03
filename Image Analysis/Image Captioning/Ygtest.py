##모델관련 중요 링크
# https://yg-progress-goodluck.notion.site/moondream-Vision-model-e31a9121b17d48b283b605ae89af6b1e?pvs=4


#requirements.txt 패키지를 설치해야함

from transformers import AutoModelForCausalLM, AutoTokenizer 
from PIL import Image

from google.cloud import translate_v3 as translate
import time
import os
from tqdm import tqdm

model_id = "vikhyatk/moondream2"
revision = "2024-03-06"
model = AutoModelForCausalLM.from_pretrained(
    model_id, trust_remote_code=True, revision=revision
)
tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)


# Json Key 인증 파일 설정
# setx GOOGLE_APPLICATION_CREDENTIALS C:\python_key\zippy-starlight-406115-7c5443d2be77.json
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\python_key\zippy-starlight-406115-7c5443d2be77.json"
# Google Cloud 프로젝트 ID 설정
project_id = "zippy-starlight-406115" 


def translate_text_with_google(source_text, source_language, target_language):
    ##우띠~~!!! 이넘의 자격인증 키를 이용하는 것이 까다로워 예처리 구문이 필요하네 ㅠㅠ
    try:
        # 환경 변수에서 Google Cloud 자격 증명 설정
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        
        #인증키 정보 출력
        #print(f'key information: {credentials_path}')
        
        if not credentials_path:
            raise ValueError("환경 변수에 Google Cloud 자격 증명이 설정되어 있지 않습니다")
        
        client = translate.TranslationServiceClient()

        parent = f"projects/{project_id}/locations/global"

        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [source_text],
                "mime_type": "text/plain",
                "source_language_code": source_language,
                "target_language_code": target_language
            }
        )
        return response.translations[0].translated_text
    
    except Exception as e:
        print(f"오류 발생: {e}")
        return None


# 이미지 파일 목록을 가져오기
def get_image_files(folder_path):
    supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    return [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in supported_formats]

# 이미지 분석 결과를 파일로 저장 
def save_results(filename, results):
    with open(filename, 'w', encoding='utf-8') as file:
        for result in results:
            file.write(result + "\n")

# 메인 로직
def main():

    source_lang = 'en'  # 소스 언어 영어
    target_lang = 'ko'  # 타겟 언어 코드 (한국어)


    image_files = get_image_files('./assets')  # 'assets' 폴더에서 이미지 파일 목록 읽기
    results = []  # 결과를 저장할 리스트

    for image_file in tqdm(image_files):
        try:
            image_path = os.path.join('./assets', image_file)
            image = Image.open(image_path)
            enc_image = model.encode_image(image)
            text1 = model.answer_question(enc_image, "Describe this image.", tokenizer)
            translated_text = translate_text_with_google(text1, source_lang, target_lang)

            # 결과 문자열을 생성합니다.
            result_str = f"이미지: {image_file}\n번역 전 이미지해석: {text1}\n번역 후 이미지해석: {translated_text}\n------------------------------------"
            results.append(result_str)
        except Exception as e:
            print(f"오류 발생: {e}")

    # 결과를 파일에 저장합니다.
    save_results('result.txt', results)

# 메인 함수 실행
if __name__ == "__main__":
    main()


