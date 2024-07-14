
from typing import Annotated
from common.db.session import get_db_session_async, get_db_session_sync
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session 
from fastapi import Depends

DBSessionDepAsync = Annotated[AsyncSession, Depends(get_db_session_async)]
DBSessionDep = Annotated[Session, Depends(get_db_session_sync)]


# usage
# @router.get(
#     "/{user_id}",
#     response_model=User,
#     dependencies=[Depends(validate_is_authenticated)],
# )
# async def user_details(
#     user_id: int,
#     db_session: DBSessionDep,
# ):
#     """
#     Get any user details
#     """
#     user = await get_user(db_session, user_id)
#     return user