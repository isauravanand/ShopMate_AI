import os
from dotenv import load_dotenv

load_dotenv()

DATABASE = {
    'dialect': 'postgresql',
    'driver': 'psycopg2',
    'username': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', '5432'),
    'database': os.getenv('POSTGRES_DB', 'shopmate_db'),
}
