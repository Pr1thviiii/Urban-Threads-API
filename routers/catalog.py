from fastapi import APIRouter, Depends , HTTPException , Query
from schemas import ProductResponse , AddProduct , UserRequest ,UpdateRequest
from database import get_db
from sqlalchemy.orm import Session 
from models import UserModel , ProductModel 
from sqlalchemy import select
from typing import Optional
from auth_utils import get_current_user

router = APIRouter(prefix="/products",tags=["Catalog"])

@router.get("/",response_model=list[ProductResponse],status_code=200)
def get_products(category: Optional[str] = Query(default=None),
            in_stock_only : Optional[bool] = Query(default=True),
            db:Session = Depends(get_db)
        ):
    
    query = select(ProductModel)    

    if category is not None:
        query = query.where(ProductModel.category==category)

    if in_stock_only:
        query = query.where(ProductModel.stock_count > 0)

    get_products = db.scalars(query).all()

    return get_products



@router.get("/{id}",status_code=200,response_model=ProductResponse)
def get_single_product(id:int,db:Session = Depends(get_db)):
    product_ = db.get(ProductModel,id)
    if product_ is None:
        raise HTTPException(
            status_code=404,
            detail="id not found"
        )

    return product_


@router.post("/",status_code=201,response_model=ProductResponse)
def add_products(
    data:AddProduct ,
    db:Session = Depends(get_db),
    current_user : UserModel = Depends(get_current_user)
    ):

    if current_user.role != "admin" :
        raise HTTPException(
            status_code=403,
            detail= "Forbidden"
        )
    
    new_product = ProductModel(
        title = data.title , 
        description = data.description , 
        price = data.price ,
        stock_count = data.stock_count ,
        category = data.category
    )
    db.add(new_product)  
    db.commit()   
    db.refresh(new_product)       

    return new_product


@router.patch("/{id}",status_code=200,response_model=ProductResponse)
def update_product(id:int , data:UpdateRequest ,
        db:Session = Depends(get_db),
        current_user : UserModel = Depends(get_current_user)
    ):

    if current_user.role != "admin" :
        raise HTTPException(
            status_code=403,
            detail= "Forbidden"
        )

    product = db.get(ProductModel,id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not exist"
        )

        
    if data.title is not None:
        product.title = data.title
    if data.description is not None:
        product.description = data.description
    if data.price is not None:
        product.price = data.price
    if data.stock_count is not None:
        product.stock_count = data.stock_count
    if data.category is not None:
        product.category = data.category
    db.commit()
    db.refresh(product)
    return product
        

    

@router.delete("/{id}",status_code=204)
def delete_product(id:int,
                   db:Session = Depends(get_db),
                   current_user : UserModel = Depends(get_current_user)
                 ):

    if current_user.role != "admin" :
        raise HTTPException(
            status_code=403,
            detail= "Forbidden"
        )

    product = db.get(ProductModel,id)

    if product is None:
         raise HTTPException(
                status_code=404,
                detail="Product not exist"
            )

    db.delete(product)
    db.commit()
    