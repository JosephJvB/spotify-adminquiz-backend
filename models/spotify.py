from typing import TypedDict

class SpotifyTokenResponse(TypedDict):
  access_token: str
  token_type: str
  expires_in: int
  refresh_token: str
  scope: str

class SpotifyToken(SpotifyTokenResponse):
  ts: int

class SpotifyRefreshResponse(TypedDict):
  access_token: str
  token_type: str
  scope: str
  expires_in: int

class SpotifyImage(TypedDict):
  height: int
  url: str
  width: int

class SpotifyProfileResponse(TypedDict):
  country: str
  display_name: str
  email: str
  href: str
  id: str
  images: list[SpotifyImage]
  product: str
  type: str
  uri: str

class SpotifyArtistTrim(TypedDict):
  name: str
  type: str
  uri: str

class SpotifyImage(TypedDict):
  height: int
  url: str
  width: int

class SpotifyAlbum(TypedDict):
  album_type: str
  artists: list[SpotifyArtistTrim]
  images: list[SpotifyImage]
  name: str
  release_date: str
  available_markets: list[str]

class Followers(TypedDict):
  href: str
  total: int

class SpotifyArtist(TypedDict):
  external_urls: dict[str, str]
  followers: Followers
  genres: list[str]
  href: str
  id: str
  images: list[SpotifyImage]
  name: str
  popularity: int
  type: str
  uri: str

class SpotifyTrack(TypedDict):
  album: SpotifyAlbum
  artists: list[SpotifyArtistTrim]
  available_markets: list[str]
  disc_number: int
  duration_ms: int
  explicit: bool
  external_ids: dict[str, str]
  external_urls: dict[str, str]
  href: str
  id: str
  is_local: bool
  name: str
  popularity: int
  preview_url: str
  track_number: int
  type: str
  uri: str

class SpotifyTopItemsResponse(TypedDict):
  items: list[dict]
  total: int
  limit: int
  offset: int
  href: str
  previous: str
  next: str