from pydantic import BaseModel


class FiltersRequest(BaseModel):
    year: int
    event_codes: list[str] | None = None
    team_numbers: list[str] | None = None