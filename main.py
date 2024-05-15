"""
Main file. 

Start app: uvicorn --reload main:app
To enter into API documentation (default): localhost:8000/api/docs; This url configure in
settings.py.
"""

from fastapi import FastAPI

from settings import setting

app = FastAPI(
    debug=setting.debug,
    
    title=setting.title,
    description=setting.description,
    
    docs_url=setting.docs_url
)
