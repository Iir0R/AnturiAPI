from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix='')

tilamuutokset = [
  
]

class TilaBase(BaseModel):
  pass

class tilaDB(TilaBase):
  id: int
  tila: str
  aika: str
  anturiID: int

@router.get('/sensor/{id}/changes')
def get_changes(anturiID: int):
  for t in tilamuutokset:
    if t['anturiID'] == anturiID:
      return [t for t in tilamuutokset if t['anturiID'] == anturiID]
  raise HTTPException(status_code=404, detail='ID not found')