# Python 3.12-slim을 기반 이미지로 사용
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY ./voice-analysis-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 소스 코드 복사
COPY ./voice-analysis-service/ /app

# 8003 포트 노출
EXPOSE 8003

# 애플리케이션 실행
CMD ["python", "voice_analysis_manage.py"]
