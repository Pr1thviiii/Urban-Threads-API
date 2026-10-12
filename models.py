from sqlalchemy.orm import Mapped ,mapped_column , relationship
from sqlalchemy import Integer, String ,Numeric ,CheckConstraint ,ForeignKey , UniqueConstraint
from database import Base , engine
from typing import Optional
from decimal import Decimal

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    email : Mapped[str] = mapped_column(String(255),nullable=False,unique=True)
    password : Mapped[str] = mapped_column(String(255),nullable=False)
    role : Mapped[str] = mapped_column(String(100),default="customer")

    cart_items_info : Mapped[list["CartModel"]] = relationship(
        back_populates="user_info",
        cascade= "all , delete-orphan"
    )

class ProductModel(Base):
    __tablename__ = "Products"

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    title : Mapped[str] = mapped_column(String(200),nullable=False)
    description : Mapped[Optional[str]] = mapped_column(String(200),nullable=True)
    price : Mapped[Decimal] = mapped_column(Numeric(10,2),nullable=False)
    stock_count : Mapped[int] = mapped_column(Integer,nullable=False,default=0)
    category : Mapped[str] = mapped_column(String(100),nullable=False)

    __table_args__ = (
        CheckConstraint("price > 0"),
        CheckConstraint("stock_count >= 0"),
    )

class CartModel(Base):
    __tablename__ = "cart_items"

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    user_id : Mapped[int] = mapped_column(Integer,ForeignKey("users.id",ondelete="CASCADE"))
    product_id : Mapped[int] = mapped_column(Integer,ForeignKey("Products.id",ondelete="CASCADE"))
    quantity : Mapped[int] = mapped_column(Integer,default=1)

    user_info : Mapped["UserModel"] = relationship(back_populates="cart_items_info")
    product_info : Mapped["ProductModel"] = relationship()

    __table_args__ = (
        CheckConstraint("quantity >= 1"),
        UniqueConstraint(product_id,user_id)
    )



     
