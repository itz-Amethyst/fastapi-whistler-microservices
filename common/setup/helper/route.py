from importlib import import_module
from user_service import api as user_api
from order_service import api as order_api
from discount_service import api as discount_api
from product_service import api as product_api
from fastapi import FastAPI
from common.utils.logger import logger_system
from user_service.utils.scope_update import get_service_directories


def setup_routers(app: FastAPI) -> None:
    service_directories = get_service_directories()
    
    for service_dir in service_directories:
        try:
            module_path = f"{service_dir}.main"
            service_module = import_module(module_path)
            
            if hasattr(service_module, "app") and hasattr(service_module.app, "router"):
                app.include_router(service_module.app.router, prefix=f"/{service_dir}")
            else:
                logger_system.error(f"Module {module_path} does not have app attribute and route associated with it")
        except ModuleNotFoundError:
            logger_system.error(f"Module {module_path} not found, skipping...")
        except Exception as e:
            logger_system.error(f"Failed to include router {module_path}")
    