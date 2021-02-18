import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    # SECRET KEY
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A-VERY-LONG-SECRET-KEY'

    # SECRET RECAPTCHA KEY
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or 'A-VERY-LONG-RECAPTCHA-PUBLIC-KEY'
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY') or 'A-VERY-LONG-RECAPTCHA-PRIVATE-KEY'

    # database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Flask Gmail Config
    MAIL_SERVER = 'smtp.live.com'
    MAIL_PROT = 465
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('GMAIL_USERNAME') or 'MAIL_USERNAME'
    MAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD') or 'MAIL_PASSWORD'


