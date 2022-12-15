# Set essential runtime environment variables
import os

def setVariable():
    os.environ['POSTGRES_DB'] = ''
    os.environ['POSTGRES_USER'] = ''
    os.environ['POSTGRES_PASSWORD'] = ''
    os.environ['POSTGRES_HOST'] = ''
    os.environ['POSTGRES_PORT'] = ''
    # os.environ['DJANGO_ALLOWED_HOSTS'] = ''
    os.environ['DEBUG'] = 'True'
    os.environ['DJANGO_SECRET_KEY'] = ''
    os.environ['MAP_API_KEY'] = ''