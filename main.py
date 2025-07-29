from typing import Union
from containers import Container
from user.interface.controllers.user_controller import router as user_routers
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

# ✅ Container 인스턴스 생성
container = Container()

# ✅ 반드시 wire 해줘야 DI가 작동함!
container.wire(modules=["user.interface.controllers.user_controller"])

app.container = container
app.include_router(user_routers)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content=exc.errors(),
    )

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
