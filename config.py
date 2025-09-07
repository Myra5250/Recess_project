class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/customer_db"
    SECRET_KEY = "your_super_secret_key"
    JWT_SECRET_KEY = "your_jwt_secret_key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV  = "production"






