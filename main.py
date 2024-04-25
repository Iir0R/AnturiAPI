from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

lohkot = [
  {'id': 1, 'anturiID': 1},
  {'id': 1, 'anturiID': 4},
  {'id': 2, 'anturiID': 2},
  {'id': 2, 'anturiID': 5},
  {'id': 3, 'anturiID': 3},
  {'id': 3, 'anturiID': 6}
]

anturit = [
  {'id': 1, 'tila': 'normaali'},
  {'id': 2, 'tila': 'normaali'},
  {'id': 3, 'tila': 'normaali'},
  {'id': 4, 'tila': 'normaali'},
  {'id': 5, 'tila': 'normaali'},
  {'id': 6, 'tila': 'normaali'}
]

tulokset = [
  {'id': 1, 'mittaus': 1, 'aika': '24.2.2024-20:15', 'anturiID': 1},
  {'id': 2, 'mittaus': -1, 'aika': '24.2.2024-20:15', 'anturiID': 2},
  {'id': 3, 'mittaus': 13, 'aika': '24.2.2024-20:15', 'anturiID': 3},
  {'id': 4, 'mittaus': 21, 'aika': '24.2.2024-20:15', 'anturiID': 4},
  {'id': 5, 'mittaus': 5, 'aika': '24.2.2024-20:15', 'anturiID': 5},
  {'id': 6, 'mittaus': -3, 'aika': '24.2.2024-20:15', 'anturiID': 6},
  {'id': 7, 'mittaus': 0, 'aika': '24.2.2024-20:15', 'anturiID': 1},
  {'id': 8, 'mittaus': 8, 'aika': '24.2.2024-20:15', 'anturiID': 2}
]

tilamuutokset = [
  
]

class AnturiBase(BaseModel):
  pass

class AnturiDB(AnturiBase):
  id: int
  tila: str

class LohkoBase(BaseModel):
  id: int

class LohkoDB(LohkoBase):
  anturiID: int

class TilaBase(BaseModel):
  pass

class tilaDB(TilaBase):
  id: int
  tila: str
  aika: str
  anturiID: int

@app.post('/sensors', status_code=status.HTTP_201_CREATED)
def create_sensor(section_in: LohkoBase, sensor_in: AnturiBase):
  new_id = len(anturit) + 1
  section = LohkoDB(**section_in.model_dump(), anturiID = new_id)
  lohkot.append(section)
  sensor = AnturiDB(**sensor_in.model_dump(), id= new_id, tila='normaali')
  anturit.append(sensor)
  return sensor

@app.put('/sensors/{id}')
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

@app.put('/sections/{id}')
def change_section(anturiID: int, id: int):
  for lohko in lohkot:
    if lohko['anturiID'] == anturiID:
      lohko['id'] = id
      return lohko
  
@app.delete('/measurements/{id}')
def delete_measurement(id: int):
  for tulos in tulokset:
    if tulos['id'] == id:
      tulokset.remove(tulos)
      return {'message': f'tulos id {id} poistettu'}
  raise HTTPException(status_code=404, detail='ID not found')

@app.get('/sensors')
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

@app.get('/sensors/{id}')
def get_sensor(id: int):
  tList = []
  for t in tulokset:
    if t['anturiID'] == id:
      tList.append({'°C': t['mittaus'], 'aika': t['aika']})
  for a in anturit:
    if a['id'] == id:
      a['mitta-arvot'] = tList
      return a
  raise HTTPException(status_code=404, detail='ID not found')

@app.get('/sensor/{id}/changes')
def get_changes(id: int):
  for t in tilamuutokset:
    if t['anturiID'] == id:
      return [t for t in tilamuutokset if t['anturiID'] == id]
  raise HTTPException(status_code=404, detail='ID not found')