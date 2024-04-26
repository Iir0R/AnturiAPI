from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix='')

tulokset = [
  
]

class MittausBase(BaseModel):
  C: float
  anturiID: int

class MittausDB(MittausBase):
  id: int
  aika: str

@router.post('/results')
def create_result(result_in: MittausBase):
  new_id = len(tulokset) + 1
  current_time = datetime.now()
  result = MittausDB(**result_in.model_dump(),aika= current_time.strftime('%Y-%m-%d %H:%M:%S'), id= new_id)
  tulokset.append(result.model_dump())
  return result

@router.delete('/results/{id}')
def delete_measurement(id: int):
  for tulos in tulokset:
    if tulos['id'] == id:
      tulokset.remove(tulos)
      return {'message': f'tulos id {id} poistettu'}
  raise HTTPException(status_code=404, detail='ID not found')