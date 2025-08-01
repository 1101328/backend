from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from common.logger import logger
from common.auth import CurrentUser, decode_access_token
from context_vars import user_context

def create_middlewares(app: FastAPI):
    @app.middleware("http")
    async def get_current_user_middleware(request: Request, call_next):
        authorization = request.headers.get("Authorization")
        if authorization:
            splits = authorization.split(" ")
            if splits[0] == "Bearer":
                token = splits[1]
                try:
                    payload = decode_access_token(token)
                    user_id = payload.get("user_id")
                    user_role = payload.get("role")
                    logger.info(str(request.url))
                    user_context.set(CurrentUser(user_id, user_role))
                except HTTPException as e:
                    return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
                except Exception:
                    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Invalid token"})
        response = await call_next(request)
        return response
