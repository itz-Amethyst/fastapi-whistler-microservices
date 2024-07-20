from discount_service.api import discount

from fastapi import APIRouter

from discount_service.db.mongo import close_db_connection, create_db_connection


router = APIRouter() 

router.add_event_handler("startup", create_db_connection)
router.add_event_handler("shutdown", close_db_connection)

router.include_router(discount.router)