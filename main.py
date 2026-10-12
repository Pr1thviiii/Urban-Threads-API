from fastapi import FastAPI
import models
from database import engine , Base
from routers.auth import router as AuthRouter
from  routers.catalog import router as CatalogRouter
from  routers.cart import router as CartRouter


Base.metadata.create_all(bind=engine)

app = FastAPI(title="URBAN THREADS")

app.include_router(AuthRouter)
app.include_router(CatalogRouter)
app.include_router(CartRouter)