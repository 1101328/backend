from typing import Union
from containers import Container
from user.interface.controllers.user_controller import router as user_router
from note.interface.controllers.note_controller import router as note_router
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn
from example.ch06_02.sync_ex import sync_ex_routers
from example.ch11_01.middleware import create_sample_middleware
from example.ch11_01.context_sample import router as context_ex_router
from middlewares import create_middlewares

app = FastAPI()

container = Container()
container.wire(modules=["user.interface.controllers.user_controller"])
container.wire(modules=["note.interface.controllers.note_controller"])

create_sample_middleware(app)
create_middlewares(app)

app.container = container
app.include_router(user_router)   
app.include_router(sync_ex_routers)
app.include_router(note_router)
app.include_router(context_ex_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content=exc.errors())

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)