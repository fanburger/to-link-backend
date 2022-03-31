import os

# 数据库配置:
DB_HOST: str = os.getenv('DB_HOST')
DB_PORT: str = os.getenv('DB_PORT')
DB_NAME: str = os.getenv('DB_NAME')
DB_USER: str = os.getenv('DB_USER')
DB_USER_PASSWORD: str = os.getenv('DB_USER_PASSWORD')
DATABASE_URL: str = f'mysql+pymysql://{DB_USER}:{DB_USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# 小程序配置:
MINIPROGRAM_APPID: str = os.getenv('MINIPROGRAM_APPID')
MINIPROGRAM_SECRET: str = os.getenv('MINIPROGRAM_SECRET')
CODE2SESSION_URL: str = 'https://api.weixin.qq.com/sns/jscode2session'

# JWT(Json Web Token) 配置:
JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY')  # openssl rand -hex 32
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS: int = 30
