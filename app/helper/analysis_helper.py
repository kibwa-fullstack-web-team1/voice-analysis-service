import numpy as np
import librosa
from skimage.transform import resize
from app.core.analysis_service import voice_analysis_service

# 모델 및 이미지 설정 (전처리 일관성을 위해 유지)
IMG_WIDTH, IMG_HEIGHT = 128, 256
CLASS_LABELS = ['AD', 'MCI', 'NC']

def preprocess_audio_to_spectrogram(audio_bytes_io):
    """
    오디오 바이트 스트림을 모델 입력에 맞는 스펙트로그램으로 변환합니다.
    """
    y, sr = librosa.load(audio_bytes_io, sr=None)
    S = librosa.feature.melspectrogram(y=y, sr=sr)
    S_DB = librosa.power_to_db(S, ref=np.max)

    img_array = (S_DB - S_DB.min()) / (S_DB.max() - S_DB.min())
    img_array = np.stack([img_array] * 3, axis=-1)
    img_array_resized = resize(img_array, (IMG_WIDTH, IMG_HEIGHT), anti_aliasing=True)
    
    processed_spectrogram = np.expand_dims(img_array_resized, axis=0).tolist()
    return {"inputs": {"keras_tensor": processed_spectrogram}}

def calculate_cognitive_score(predictions):
    """
    TensorFlow Serving의 예측 결과를 인지 건강 점수로 변환합니다.
    """
    predicted_class_index = np.argmax(predictions)
    predicted_class_label = CLASS_LABELS[predicted_class_index]
    confidence = np.max(predictions)

    details = {
        "predicted_class": predicted_class_label,
        "confidence": round(confidence * 100, 2),
        "raw_predictions": predictions
    }

    if predicted_class_label == 'NC':
        cognitive_score = 80 + (confidence * 20)
    elif predicted_class_label == 'MCI':
        cognitive_score = 40 + (confidence * 39)
    else:  # AD
        cognitive_score = 0 + (confidence * 39)
    
    cognitive_score = round(min(max(cognitive_score, 0), 100), 2)

    return {"cognitive_score": cognitive_score, "details": details}

def run_analysis_pipeline(s3_url: str) -> dict:
    """
    전체 음성 분석 파이프라인을 실행합니다.
    """
    try:
        # 1. Core Service를 통해 S3에서 오디오 다운로드
        audio_bytes_io = voice_analysis_service.download_audio_from_s3(s3_url)

        # 2. Helper에서 오디오 데이터 전처리
        input_data = preprocess_audio_to_spectrogram(audio_bytes_io)

        # 3. Core Service를 통해 TF Serving에서 예측 가져오기
        predictions = voice_analysis_service.get_prediction_from_tf_serving(input_data)

        # 4. Helper에서 점수 계산
        result = calculate_cognitive_score(predictions)
        
        print(f"Analysis pipeline complete for {s3_url}. Score: {result['cognitive_score']}")
        return result

    except Exception as e:
        print(f"Error in analysis pipeline for {s3_url}: {e}")
        # 실제 프로덕션에서는 더 상세한 에러 처리가 필요합니다.
        return {"error": str(e), "cognitive_score": 0}
