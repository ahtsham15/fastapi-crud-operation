from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:admin@localhost:5433/fast_api",echo=True)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# postgresql+psycopg2://postgres:admin@localhost:5433/fast_api