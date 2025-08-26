from pydantic import BaseModel

# TODO: fill title and url typing
class Event(BaseModel):
    title: str
    date: str
    time: str
    url: str
    location: str
