import os

class Config:
    PHASE = 'default'
    SERVICE_PORT = 8003
    
    # AWS S3 관련 환경 변수 추가
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.environ.get('AWS_REGION')
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

class ProductionConfig(Config):
    PHASE = 'production'

class DevelopmentConfig(Config):
    PHASE = 'development'

config_by_name = dict(
    development=DevelopmentConfig,
    production=ProductionConfig,
)