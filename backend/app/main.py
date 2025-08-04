import uvicorn
from app.routes.user_login import router as user_login_router
from app.routes.user_refresh_token import router as user_refresh_router
from app.routes.user_registration import router as user_register_router
from app.routes.cart import router as cart_router
from app.routes.cart_item import router as cart_item_router
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware


my_app = FastAPI(title="Cornucopia API", version="1.0.0", root_path="/cornucopia")

my_app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://localhost(:\d+)?",
    allow_credentials=True,      
    allow_methods=["*"],         
    allow_headers=["*"],         
)

my_app.include_router(user_refresh_router, prefix="/user", tags=["user"])  
my_app.include_router(user_login_router, prefix="/user", tags=["user"])  
my_app.include_router(user_register_router, prefix="/user", tags=["user"])  
my_app.include_router(cart_router)  
my_app.include_router(cart_item_router) 

if __name__ == "__main__":
    uvicorn.run("app.main:my_app", host="0.0.0.0", port=8000, reload=True)
