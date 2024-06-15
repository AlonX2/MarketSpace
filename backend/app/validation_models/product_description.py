from pydantic import BaseModel, HttpUrl

class ProductDescription(BaseModel):
    """Model for the product description that the client passes
    """
    name: str
    url: HttpUrl