import os
import uvicorn
from dotenv import load_dotenv
from app import create_app

# .env 파일에서 환경 변수 로드
load_dotenv()

config_name = os.getenv('PHASE') or 'development'
app = create_app(config_name)

if __name__ == '__main__':
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=app.config.SERVICE_PORT,
    )
