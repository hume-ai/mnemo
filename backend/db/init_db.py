
import os 
import sys
# print(sys.path)

sys.path.append(os.getcwd())
# print(os.getcwd())


from backend.db.database import engine, Base
from backend.db.models import Project, Session, Interaction

def init_db():
     Base.metadata.create_all(bind=engine)
     print("Initialized the database.")

if __name__ == "__main__":
     init_db()