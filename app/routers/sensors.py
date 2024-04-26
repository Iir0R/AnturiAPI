from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from .changes import tilaDB, tilamuutokset
from .blocks import LohkoBase, LohkoDB, lohkot
from .results import tulokset

router = APIRouter(prefix='')

anturit = [
  {'id': 1, 'tila': 'normaali'},
  {'id': 2, 'tila': 'normaali'},
  {'id': 3, 'tila': 'normaali'},
  {'id': 4, 'tila': 'normaali'},
  {'id': 5, 'tila': 'normaali'},
  {'id': 6, 'tila': 'normaali'}
]

class AnturiBase(BaseModel):
  pass

class AnturiDB(AnturiBase):
  id: int
  tila: str

@router.put('/sensors/{id}')
def change_state(id: int, state: str):
  new_id = len(tilamuutokset) + 1
  current_time = datetime.now()
  for anturi in anturit:
    if anturi['id'] == id:
      anturi['tila'] = state
      change = tilaDB(id= new_id, tila= state, aika= current_time.strftime('%Y-%m-%d %H:%M:%S'), anturiID= anturi['id'])
      tilamuutokset.append(change.model_dump())
      return anturi
  raise HTTPException(status_code=404, detail='ID not found')

@router.get('/sensors')
def get_sensors(state: str = ''):
  aList = []
  if state == '':
    for a in anturit:
      for l in lohkot:
        if l['anturiID'] == a['id']:
          a['lohkoID'] = l['id']
          aList.append(a)
    return aList
  for a in anturit:
    for l in lohkot:
      if l['anturiID'] == a['id']:
        a['lohkoID'] = l['id']
        if a['tila'] == state:
          aList.append(a)
  return aList

@router.get('/sensors/{id}')
def get_sensor(id: int):
  tList = []
  for t in tulokset:
    if t['anturiID'] == id:
      tList.append({'id': t['id'], 'C': t['C'], 'aika': t['aika']})
  for a in anturit:
    a_copy = a.copy()
    if a['id'] == id:
      a_copy['mitta-arvot'] = tList
      return a_copy
  raise HTTPException(status_code=404, detail='ID not found')

@router.post('/sensors/blocks', status_code=status.HTTP_201_CREATED)
def create_sensor(section_in: LohkoBase, sensor_in: AnturiBase):
  new_id = len(anturit) + 1
  section = LohkoDB(**section_in.model_dump(), anturiID = new_id)
  lohkot.append(section.model_dump())
  sensor = AnturiDB(**sensor_in.model_dump(), id= new_id, tila='normaali')
  anturit.append(sensor.model_dump())
  return sensor