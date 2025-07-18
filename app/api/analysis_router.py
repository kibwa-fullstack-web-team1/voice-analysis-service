from fastapi import APIRouter
from app.schemas.analysis_schema import AnalysisRequest, AnalysisResponse
from app.helper.analysis_helper import run_analysis_pipeline

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_voice_endpoint(
    request: AnalysisRequest
):
    """
    음성 파일의 S3 URL을 받아 인지 건강 점수를 분석하고 반환합니다.
    """
    analysis_result = run_analysis_pipeline(request.s3_url)
    return AnalysisResponse(
        cognitive_score=analysis_result.get("cognitive_score", 0.0),
        details=analysis_result.get("details", {})
    )
