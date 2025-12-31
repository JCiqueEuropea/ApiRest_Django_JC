import time
from typing import List, Optional

from pydantic import BaseModel, Field


class SpotifyImageDTO(BaseModel):
    url: str
    height: Optional[int] = None
    width: Optional[int] = None


class SpotifyArtistDTO(BaseModel):
    id: str
    name: str
    popularity: Optional[int] = None
    genres: List[str] = Field(default_factory=list)
    href: str
    uri: str


class SpotifyTrackDTO(BaseModel):
    id: str
    name: str
    popularity: Optional[int] = None
    duration_ms: int
    explicit: bool
    artists: List[SpotifyArtistDTO] = Field(default_factory=list)
    album_name: str = ""
    href: str
    uri: str


class SpotifyTokenDTO(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    scope: str
    created_at: float = Field(default_factory=time.time)
