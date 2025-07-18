import os
import httpx
import boto3
import io
from app.config.config import Config

# TensorFlow Serving 엔드포인트 설정
TF_SERVING_URL = os.getenv("TF_SERVING_URL", "http://localhost:8501/v1/models/dementia_classification_model:predict")

class VoiceAnalysisService:
    def __init__(self):
        """
        외부 서비스(S3, TensorFlow Serving)와의 통신을 담당하는 서비스
        """
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_REGION
        )
        print("VoiceAnalysisService initialized for external communications.")

    def download_audio_from_s3(self, s3_url: str) -> io.BytesIO:
        """
        S3에서 음성 파일을 다운로드하여 메모리 내 바이트 스트림으로 반환합니다.
        """
        print(f"Downloading voice from {s3_url}...")
        try:
            bucket_name = s3_url.split('//')[1].split('/')[0]
            key = '/'.join(s3_url.split('//')[1].split('/')[1:])
            
            audio_bytes_io = io.BytesIO()
            self.s3.download_fileobj(bucket_name, key, audio_bytes_io)
            audio_bytes_io.seek(0)
            
            print(f"Successfully downloaded from S3.")
            return audio_bytes_io
        except Exception as e:
            print(f"S3 download failed: {e}")
            raise RuntimeError(f"S3_DOWNLOAD_FAILED: {e}")

    def get_prediction_from_tf_serving(self, instances: list) -> list:
        """
        전처리된 데이터를 TensorFlow Serving에 보내고 예측 결과를 받습니다.
        """
        print(f"Requesting prediction from TensorFlow Serving: {TF_SERVING_URL}")
        try:
            headers = {"content-type": "application/json"}
            json_request = {"instances": instances}
            
            response = httpx.post(TF_SERVING_URL, headers=headers, json=json_request, timeout=30.0)
            response.raise_for_status()
            
            predictions = response.json()["predictions"][0]
            print("Successfully received prediction.")
            return predictions
        except httpx.RequestError as e:
            print(f"TF Serving request failed: {e}")
            raise RuntimeError(f"TF_SERVING_REQUEST_FAILED: {e}")
        except httpx.HTTPStatusError as e:
            print(f"TF Serving response error: {e.response.status_code} - {e.response.text}")
            raise RuntimeError(f"TF_SERVING_RESPONSE_ERROR: {e.response.status_code}")

# 싱글톤 인스턴스 생성
voice_analysis_service = VoiceAnalysisService()