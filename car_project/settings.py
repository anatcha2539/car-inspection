from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- นี่คือค่าที่เราใช้บน Server ---
SECRET_KEY = 'django-insecure-k29%4al@#4l8a*5=wqfq*&b%aw%(!j3yf71qyfopl#xvk8%x#e' 
# (ถ้าใช้บน VS Code ให้แก้ DEBUG = True และ ALLOWED_HOSTS = [])
DEBUG = True
ALLOWED_HOSTS = ['anatcha.pythonanywhere.com', '127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inspection',
    'inspection.templatetags',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'car_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'inspection.context_processors.notification_processor',
            ],
            'libraries': { # (เพิ่มส่วนนี้)
                'form_filters': 'inspection.templatetags.form_filters',
            }
        },
    },
]

WSGI_APPLICATION = 'car_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    # ... (ส่วนนี้ไม่ต้องแก้) ...
]

LANGUAGE_CODE = 'th'
TIME_ZONE = 'Asia/Bangkok'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles" # สำหรับ Server
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/router/' # (สำคัญมาก)
LOGOUT_REDIRECT_URL = '/admin/login/'