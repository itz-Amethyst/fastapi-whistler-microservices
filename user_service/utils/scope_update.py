import os
from typing import List
from common.db.session import get_db_session_sync
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from common.utils.logger import logger_system

from user_service.models.scope import Scope

def get_service_directories() -> List[str]:
    current_dir = os.getcwd()
    return [
        dir_name for dir_name in os.listdir(current_dir)
        if os.path.isdir(os.path.join(current_dir, dir_name)) and dir_name.endswith('_service')
    ]

def update_scopes(db: Session, service_dirs: List[str]):
    existing_scopes = db.query(Scope).all()
    existing_scopes_names = {scope.name for scope in existing_scopes}

    for service_dir in service_dirs:
        if service_dir not in existing_scopes_names:
            try:
                new_scope = Scope(name=service_dir, description= f"Scope for {service_dir}")
                db.add(new_scope)
                db.commit()
                
                logger_system.info(f"Added new scope for {service_dir}")
            except IntegrityError:
                print(f"Scope already exists: {service_dir}")
    if "full_control" not in existing_scopes_names:
        try:
            new_scope = Scope(name="full_control", description="Full permission scope")
            db.add(new_scope)
            db.commit()
            logger_system.info("Added full_control scope")
        except IntegrityError:
            logger_system.warning("full_control scope already exists") 

def check_and_update_scopes():
    db = get_db_session_sync()
    try:
        service_dirs = get_service_directories()
        update_scopes(next(db), service_dirs)
    except Exception as e:
        logger_system.error(f"something went wrong during updating scopes {e}")