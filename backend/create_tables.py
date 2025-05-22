# create_tables.py

from db import engine, Base
from models import PDF, Drawing, Note 

Base.metadata.drop_all(bind=engine) 
Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully.")
