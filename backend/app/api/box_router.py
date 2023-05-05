"""
box_router.py

Handles box requests.
"""

# Import modules and libraries
from datetime import timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas, utils, crud, models

router = APIRouter()
"""
Creates an instance of the router that will handle box functions.
"""

@router.get("/", response_model=List[schemas.Box])
def read_boxes(database: Session = Depends(utils.get_database), offset: int = 0, limit: int = 16, current_user: models.User = Depends(utils.get_current_user)):
    """
    This function pulls a list of boxes from the database.
    """
    if current_user:
        try:
            boxes = crud.get_boxes(database=database, offset=offset, limit=limit)
            return boxes
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error!")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate your user! Sorry.")
    
@router.post("/", response_model=schemas.Box)
def create_new_box(database: Session = Depends(utils.get_database), new_box: schemas.BoxCreate = None, current_user: models.User = Depends(utils.get_current_user)):
    """
    Create a new box in the database.
    """
    box = crud.create_box(database=database, box_in=new_box)
    return box

@router.put("/{id}", response_model=schemas.Box)
def update_box(database: Session = Depends(utils.get_database), box_id: int = 1, new_box: schemas.BoxUpdate = None, current_user: models.User = Depends(utils.get_current_user)):
    """
    Update a box.
    """
    # Get the box from the database
    box_in_database = crud.get_box_by_id(database=database, box_id=box_id)

    if box_in_database:
        updated_box = crud.update_box(database=database, box_id=box_id, box=new_box)
        return updated_box
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown error!")