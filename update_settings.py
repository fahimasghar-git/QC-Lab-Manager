import re

path = '/Users/fahimasghar/Documents/QC-Lab-Manager/lims_core/settings.py'
with open(path, 'r') as f:
    content = f.read()

# Add WhiteNoise Middleware
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in content:
    content = content.replace(
        "'django.middleware.security.SecurityMiddleware',",
        "'django.middleware.security.SecurityMiddleware',\n    'whitenoise.middleware.WhiteNoiseMiddleware',"
    )

# Add import os and dj_database_url if not there
if 'import dj_database_url' not in content:
    content = 'import os\nimport dj_database_url\n' + content

# Update ALLOWED_HOSTS
content = re.sub(r"ALLOWED_HOSTS = \[.*?\]", "ALLOWED_HOSTS = ['*']", content)

# Update DATABASES
db_pattern = r'DATABASES = \{\s*"default": \{\s*"ENGINE": "django\.db\.backends\.sqlite3",\s*"NAME": BASE_DIR / "db\.sqlite3",\s*\}\s*\}'
new_db = """DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}"""
content = re.sub(db_pattern, new_db, content, flags=re.DOTALL)

# Update STATIC_ROOT
if 'STATIC_ROOT' not in content:
    content += "\nSTATIC_ROOT = BASE_DIR / 'staticfiles'\n"
else:
    content = re.sub(r"STATIC_ROOT = .*", "STATIC_ROOT = BASE_DIR / 'staticfiles'", content)

with open(path, 'w') as f:
    f.write(content)

