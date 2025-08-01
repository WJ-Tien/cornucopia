import uvicorn
from app.routes.user import router as user_router
from fastapi import FastAPI 

my_app = FastAPI(title="Cornucopia API", version="1.0.0", root_path="/cornucopia")
my_app.include_router(user_router, prefix="/user", tags=["user"])  

if __name__ == "__main__":
    # 1. uvicorn app.main:my_app --> uvicorn finds my_app and run 
    # 2. python -m app.main --> enter the __name__ block and uvicorn.run
    uvicorn.run("app.main:my_app", host="0.0.0.0", port=8000, reload=True)
