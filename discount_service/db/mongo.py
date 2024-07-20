import importlib
from typing import List, Type
from common.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import Document, init_beanie

from discount_service.models.discount import Discount

def load_models_from_given_path(module_name: str) -> List[Type[Document]]:
    module = importlib.import_module(module_name)
    models = []
    for attr_name in dir(module):
        attribute = getattr(module, attr_name)
        if isinstance(attribute, type) and issubclass(attribute, Document):
            models.append(attribute)
    return models


async def create_db_connection():
   global client
   client = AsyncIOMotorClient(settings.FULL_MONGODB_URL)
   document_models = load_models_from_given_path('discount_service.models')
   print("Connecting ...")
   print(document_models)
   await init_beanie(client["Whistler"], document_models=[Discount])
   
async def close_db_connection():
    client.close()