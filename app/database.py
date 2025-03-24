import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
# Database connection URL
db_name = "edision_api_test"
db_user = "dev"
db_password = "Dev-password"
db_host = "localhost"
port = 5432
DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{port}/{db_name}"

# Create engine
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create DB if not exists
def create_database():
    conn = psycopg2.connect(
        dbname=db_name, user=db_user, password=db_password, host=db_host
    )
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database {db_name} created.")
        else:
            print(f"Database {db_name} already exists.")
    except OperationalError as e:
        print(f"Error while creating database: {e}")
    finally:
        cursor.close()
        conn.close()

# Create all tables (if they do not exist)
def create_tables():
    from app.models import Base
    Base.metadata.create_all(bind=engine)
    print("Tables created if they do not exist.")

# Create DB and Tables
create_database()
create_tables()

# Function to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
