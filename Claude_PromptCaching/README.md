# Prompt Caching 실제 활용 소스

## 1. AD_class_labeling_v2.ipynb
  - Prompt Caching 적용 전 파일
  
## 2. AD_class_labeling_v2_caching.ipynb
  - Prompt Caching 적용 후 파일

## 3. class.txt
  - Caching을 적용한 Input Token(위 2번 코드에서 읽어 들어 캐싱화함)

## 4. 기타 추가 구현  참조사항
  1) 50개 데이터 기준 Checkpoint 저장하여 프로세스 중단 후 다시 재개해도 자동으로 이어서 저장
  2) Claude API 사용 한계 초과 오류 코드 발생 시 프로세스를 중단 시키는 코드를 추가(오류가 나고 코드실행 중단됨)
  3) Claude API 서버 오류 시 5번까지 재시도 코드 추가

   
