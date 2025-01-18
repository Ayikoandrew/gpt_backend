import logging
from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel

from db.database import engine
from routes.auth import router

app = FastAPI()


# @app.middleware("http")
# async def add_no_cache_header(request, call_next):
#     try:
#         response = await call_next(request)
#         if response is None:
#             return JSONResponse(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 content={"detail": "Internal server error"},
#             )
#         if isinstance(response, Response):
#             response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#             response.headers["Pragma"] = "no-cache"
#             response.headers["Expires"] = "0"
#         return response
#     except Exception as e:
#         logging.error(f"Middleware error: {str(e)}")
#         return JSONResponse(
#             status_code=500, content={"detail": f"Internal server error: {str(e)}"}
#         )


app.include_router(router=router, prefix="/auth")

SQLModel.metadata.create_all(engine)
