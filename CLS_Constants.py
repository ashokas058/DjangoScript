DEFAULT_PORT=6000
DJANGO_PORT_CONFIG_DIR="/home/ash/WEBAPP_Config"
DJANGO_PROJECT_DIR="/home/ash/WEBAPP"
DJANGO_BACKUP="/backup"
DJANGO_UPLOAD="/upload"
TEMP_UNZIP="/zipBin/api/"

EXCLUDE_FILES=["bin",".gitignore","pyvenv.cfg","lib"]

DJANGO_LOGGING="/var/log/djangoDeploy-error.log"

NGINX_SITEAVAILABLE="/etc/nginx/sites-available"
NGINX_SITENABLED="/etc/nginx/sites-enabled"

SUPERVISOR_CNF="/etc/supervisor/conf.d"

DJANGO_USER_GROUP= "ash:ash"
DJANGO_OWNER="/home/ash"
DJANGO_NGINX_OWNERSHIP="ash:letsencryptusers"
DJANGO_CERT_LOCATION="/etc/letsencrypt/archive"

PACKAGES = [
    'libpq-dev',
    'python3-dev',
    'build-essential',
    'python3-virtualenv',
    'supervisor',
    'python3-pip',
    'certbot',
    'python3-certbot-nginx',
    'zip'
]

PYTHON_PACKAGE=[
    'simple-term-menu'
]
PORT_POOL="portPool.txt"
PORT_COMMON="port.txt"
TEMPLATE_NGINX="/home/ash/Project/DevOps/beeka/template/nginx.conf"
TEMPLATE_SUPERVISOR="/home/ash/Project/DevOps/beeka/template/supervisor.conf"
TEMPLATE_UWSGI="/home/ash/Project/DevOps/beeka/template/uwsgi-start"


