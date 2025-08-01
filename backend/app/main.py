from fastapi import FastAPI 

app = FastAPI()

# Import and include routers here
# from app.routes import user, restaurant, menu, order, ...
# app.include_router(user.router)
# ...

@app.get("/")
def root():
    return {"message": "Cornucopia backend is running."}
