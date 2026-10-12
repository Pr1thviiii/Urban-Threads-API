from pydantic import BaseModel , Field , ConfigDict
from typing import Optional

class UserRequest(BaseModel):
    email : str = Field(max_length=255)
    password : str = Field(max_length=255,min_length=8)

class UserResponse(BaseModel):
    id : int 
    email : str
    role : str
    
class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    title : str
    description : Optional[str]
    price : float
    stock_count : int
    category : str


class AddProduct(BaseModel):
    title : str
    description : Optional[str]
    price : float = Field(gt=0)
    stock_count : int = Field(ge=1)
    category : str


class UpdateRequest(BaseModel):
    title : Optional[str]
    description : Optional[str]
    stock_count : Optional[int] = Field(ge=1)
    price : Optional[float] = Field(gt=0)
    category : Optional[str]

class AddCart(BaseModel):
    product_id : int
    quantity : int = Field(ge=1)

class AddRespone(BaseModel):
    title : str
    user_id : int
    product_id : int
    price : float
    quantity : int

class UpdateQuant(BaseModel):
    quantity : int = Field(ge=1)
    

