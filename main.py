from common.setup.factory import create_app
# if project gets bigger should decide to create a setup folder for this even 
# app = FastAPI(lifespan=lifespan) 
app = create_app()


# @asynccontextmanager
# async def lifespan_setup(app):
#     logger_system.info("Starting server ...")

#     async with sessionManager._async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield

#     logger_system.info("Shutting down the system.")

#     await sessionManager.close_async()