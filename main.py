from app.database import Base, engine
from app.cli import app

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    app()