from pydantic import BaseModel, Field

class AnalysisRequest(BaseModel):
    s3_url: str = Field(..., description="분석할 음성 파일이 저장된 S3 URL")

class AnalysisResponse(BaseModel):
    cognitive_score: float = Field(..., description="인지 건강 분석 점수")
    details: dict = Field({}, description="분석 관련 세부 정보")
