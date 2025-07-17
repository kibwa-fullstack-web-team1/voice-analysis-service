from fastapi import APIRouter, Depends
from app.schemas.analysis_schema import AnalysisRequest, AnalysisResponse
from app.core.analysis_service import VoiceAnalysisService, voice_analysis_service

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_voice_endpoint(
    request: AnalysisRequest,
    service: VoiceAnalysisService = Depends(lambda: voice_analysis_service)
):
    """
    음성 파일의 S3 URL을 받아 인지 건강 점수를 분석하고 반환합니다.
    """
    score = service.analyze_voice(request.s3_url)
    return AnalysisResponse(cognitive_score=score, details={"model_version": "0.1.0-mock"})
