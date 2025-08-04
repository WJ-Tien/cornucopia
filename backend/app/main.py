import uvicorn
from app.routes.user_login import router as user_login_router
from app.routes.user_refresh_token import router as user_refresh_router
from app.routes.user_registration import router as user_register_router
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware


my_app = FastAPI(title="Cornucopia API", version="1.0.0", root_path="/cornucopia")

origins = [
    "http://localhost",
    "http://localhost:5173", # Vite 預設的開發伺服器位址
    # 如果您有其他前端位址，也一併加入
]

my_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # 允許指定的來源
    allow_credentials=True,      # 允許 cookies
    allow_methods=["*"],         # 允許所有 HTTP 方法 (GET, POST, OPTIONS 等)
    allow_headers=["*"],         # 允許所有 HTTP 標頭
)


my_app.include_router(user_refresh_router, prefix="/user", tags=["user"])  
my_app.include_router(user_login_router, prefix="/user", tags=["user"])  
my_app.include_router(user_register_router, prefix="/user", tags=["user"])  

if __name__ == "__main__":
    uvicorn.run("app.main:my_app", host="0.0.0.0", port=8000, reload=True)
