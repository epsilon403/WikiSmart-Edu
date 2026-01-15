# Article schemas: ArticleCreate, ArticleResponse, ArticleHistory
# schemas.py
from pydantic import BaseModel, HttpUrl, field_validator

class WikiRequest(BaseModel):
    url: HttpUrl

    @field_validator('url')
    def validate_wiki_url(cls, v):
        if "wikipedia.org" not in str(v):
            raise ValueError("L'URL doit provenir de Wikipedia")
        return v