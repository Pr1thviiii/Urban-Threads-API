from fastapi import APIRouter, Depends , HTTPException 
from schemas import AddCart ,AddRespone , UpdateQuant
from database import get_db
from sqlalchemy.orm import Session , Query
from models import UserModel , ProductModel , CartModel
from sqlalchemy import select
from typing import Optional
from auth_utils import get_current_user

router = APIRouter(prefix="/cart",tags=["Cart"])

@router.post("/items",status_code=201,response_model=AddRespone)
def add_item(userdata:AddCart,
             db:Session = Depends(get_db),
             current_user:UserModel=Depends(get_current_user)
             ):
    query = select(ProductModel).where(ProductModel.id == userdata.product_id)
    product_ = db.scalars(query).first()

    if product_ is None:
        raise HTTPException(
            status_code=404,
            detail = "Product not found"
        )

    query_ = select(CartModel).where(CartModel.product_id == userdata.product_id ,
                                    CartModel.user_id == current_user.id)
    user_ = db.scalars(query_).first()

    existing_quantity = user_.quantity if user_ else 0
    final_quantity = existing_quantity + userdata.quantity

    if final_quantity > product_.stock_count:
        raise HTTPException(
            status_code=409,
            detail= "not enough quantity"
        )

    if user_ :
       
       user_.quantity = final_quantity
       
    else :
        user_ = CartModel(
            user_id = current_user.id ,
            product_id = userdata.product_id ,
            quantity = final_quantity ,
        )
        db.add(user_)

    db.commit()
    db.refresh(user_)

    return {
        "title" : user_.product_info.title,
        "user_id" : user_.user_id,
        "product_id" : user_.product_id,
        "price" : user_.product_info.price,
        "quantity" : user_.quantity
    }

@router.get("/",status_code=200)
def get_all_items(
    db:Session = Depends(get_db),
    current_user:UserModel=Depends(get_current_user)
    ):

    query = select(CartModel).where(CartModel.user_id == current_user.id)
    cart_list = db.scalars(query).all()
    
    items = []
    grand_total = 0

    for i in cart_list:
        
        cart_item_no = i.id
        product_id = i.product_id
        quantity = i.quantity
        price =   i.product_info.price
        title = i.product_info.title
        item_total = quantity * price

        one_item = {
            "cart_item_id": cart_item_no,
            "title": title,
            "product_id": product_id,
            "quantity": quantity,
            "price": price,
            "subtotal": item_total
        }
        
        items.append(one_item)
        grand_total += item_total

    return {
        "items" : items,
        "grand_total": grand_total
    }


@router.patch("/item/{cart_id}",status_code=200)
def update_quantity(cart_id:int,
                    userdata:UpdateQuant,
                    db:Session = Depends(get_db),
                    current_user:UserModel=Depends(get_current_user)
                    ):

    query = select(CartModel).where(CartModel.user_id == current_user.id,
                                    CartModel.id == cart_id
                                    )
    cart_ = db.scalars(query).first()

    if not cart_:
        raise HTTPException(
            status_code=404,
            detail="Not found"
        )

    if cart_.product_info.stock_count < userdata.quantity :
        raise HTTPException(
            status_code=409,
            detail = "Not enough stock avaiable"
        )
    
    cart_.quantity = userdata.quantity
    db.commit()
    db.refresh(cart_)

    return {"Message":"Quantity updated !"}


@router.delete("/item/{cart_id}",status_code=204)
def delete_one(cart_id:int,
               db:Session = Depends(get_db),
               current_user:UserModel=Depends(get_current_user)
               ):

    query = select(CartModel).where(CartModel.user_id == current_user.id,
                                    CartModel.id == cart_id
                                    )
    cart_ = db.scalars(query).first()

    if not cart_:
        raise HTTPException(
                status_code=404,
                detail="Not found"
            )
    db.delete(cart_)
    db.commit()

    return {"Message":"Cart item deleted"}


@router.delete("/item",status_code=204)
def clear_cart(db:Session = Depends(get_db),
               current_user:UserModel=Depends(get_current_user)
               ):
    query = select(CartModel).where(CartModel.user_id==current_user.id)
    user = db.scalars(query).all()

    for i in user:
        db.delete(i) 

    db.commit()

    return {"Message":"Whole Cart deleted"}

