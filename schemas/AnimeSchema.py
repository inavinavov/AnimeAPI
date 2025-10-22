from pydantic import BaseModel


class AnimeCreateClass(BaseModel):
    name : str
    create_data: str
    final_data: str
    count_of_series: int
    genre: str

