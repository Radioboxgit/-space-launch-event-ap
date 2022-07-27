from fastapi import FastAPI
from typing import List

from fastapi import FastAPI, HTTPException
from models import launch_Pydantic, launch_pydantic_in, Launch


from tortoise.contrib.fastapi import register_tortoise


description = """
"Here is an API for upcoming space launch events modeled after spacenewsflight API to reduce service burden on spaceflightnews API"🚀

## Events API

You can Creat **events**.

You will be able to:

* **Create events** 
* **Read events** 
* **Delete events** 
"""


app= FastAPI(
    title="Space Launch Event",
    description=description,
    version="0.0.1",
    contact={
        "name": "Anigbogu Chinedu",
        "url": "https://anigbogu-resume.vercel.app",
        "email": "chinedulaw62@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)


@app.get("/events", response_model=List[launch_Pydantic], tags=["Events"])
async def get_events():
    '''get all upcoming launch events'''
    return await launch_Pydantic.from_queryset(Launch.all().order_by('id'))


@app.get("/confirm/event/{id}",tags=["Events"])
async def check_event(id:str):
    '''check if an event with a given reference id exists'''

    return {"message":f"event with reference_id:{id} found"} if await Launch.filter(reference_id=id) else None


@app.post("/event", response_model=launch_Pydantic,status_code=201,tags=["Events"])
async def post_event( event: launch_pydantic_in):
    '''create a single event'''
    event_object = await Launch.create(**event.dict(exclude_unset=True))
    return await launch_Pydantic.from_tortoise_orm(event_object)


@app.post("/events", response_model=List[launch_Pydantic],status_code=201,tags=["Events"])
async def post_events( events: List[launch_pydantic_in]):
    '''create multiple events at a go.'''
    events_object=[await Launch.create(**event.dict(exclude_unset=True)) for event in events]
    return events_object


@app.delete("/event",tags=["Events"])
async def delete_event(id: str):
    deleted_count = await Launch.filter(reference_id=id).delete()
    return deleted_count


# register tortoise orm models 
register_tortoise(
    app,
    db_url="sqlite://event.db",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

