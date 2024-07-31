from user_service import api
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


app = FastAPI(docs_url='/docs/')
app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            expose_headers=["Content-Range", "Range"],
            allow_headers=["Authorization", "Range", "Content-Range"],
        )
app.include_router(api.router)