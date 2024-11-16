from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.functions.create_tables import create_tables
from web_app.routes.auth import login_router
from web_app.routes.debts import depts_router
from web_app.routes.expenses import expence_router
from web_app.routes.groups import group_router
from web_app.routes.payments import payments_router
from web_app.routes.user import user_router

create_tables()


def get_application() -> FastAPI:
    application = FastAPI(root_path="/api")
    application.include_router(login_router)
    application.include_router(depts_router)
    application.include_router(expence_router)
    application.include_router(group_router)
    application.include_router(payments_router)
    application.include_router(user_router)
    return application


app = get_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
