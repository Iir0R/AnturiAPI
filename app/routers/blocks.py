from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix='')

lohkot = [
  {'id': 1, 'anturiID': 1},
  {'id': 1, 'anturiID': 4},
  {'id': 2, 'anturiID': 2},
  {'id': 2, 'anturiID': 5},
  {'id': 3, 'anturiID': 3},
  {'id': 3, 'anturiID': 6}
]

class LohkoBase(BaseModel):
  id: int

class LohkoDB(LohkoBase):
  anturiID: int

@router.put('/blocks/{id}/sensor')
def change_section(anturiID: int, id: int):
  for lohko in lohkot:
    if lohko['anturiID'] == anturiID:
      lohko['id'] = id
      return lohko