import uvicorn
from app.core.database import engine, Base
from app.routes.user_refresh_token import router as user_refresh_router
from app.routes.user_login import router as user_login_router
from fastapi import FastAPI 

my_app = FastAPI(title="Cornucopia API", version="1.0.0", root_path="/cornucopia")

my_app.include_router(user_refresh_router, prefix="/user", tags=["user"])  
my_app.include_router(user_login_router, prefix="/user", tags=["user"])  

# skip if tables were already created (safe ops)
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run("app.main:my_app", host="0.0.0.0", port=8000, reload=True)
