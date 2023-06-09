"""
extinguisher_router.py

Handles extinguisher requests.
"""
# Import modules and libraries
from datetime import timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas, utils, crud, models, enums

router = APIRouter()
"""
Creates an instance of the router that will handle extinguisher functions.
"""

@router.get("/", response_model=List[schemas.Extinguisher])
def read_extinguishers(database: Session = Depends(utils.get_database), offset: int = 0, limit: int = 16, current_user: models.User = Depends(utils.get_current_user)):
    """
    This function pulls a list of extinguishers from the database.
    """
    if current_user:
        extinguishers = crud.get_extinguishers(database=database, offset=offset, limit=limit)
        return extinguishers

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate your user! Sorry.")
    
@router.get("/types", response_model=List[schemas.Extinguisher])
def read_extinguishers_by_type(database: Session = Depends(utils.get_database), ext_type: enums.FireClass = enums.FireClass.ABC, offset: int = 0, limit: int = 16, current_user: models.User = Depends(utils.get_current_user)):
    """
    This function pulls a list of a specific type of extinguisher from the database.
    """
    if current_user:
        extinguishers = crud.get_extinguishers_by_type(database=database, extinguisher_type=ext_type, offset=offset, limit=limit)
        return extinguishers
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate your user! Sorry.")