from typing import Optional, Dict, Any, List

import httpx
from asgiref.sync import sync_to_async
from django.utils import timezone

from app.models import SpotifyCredentials
from .auth import refresh_token_with_refresh_token

API_BASE = "https://api.spotify.com/v1"


@sync_to_async
def get_credentials(user_id: int):
    try:
        return SpotifyCredentials.objects.get(user_id=user_id)
    except SpotifyCredentials.DoesNotExist:
        return None


@sync_to_async
def update_credentials(cred: SpotifyCredentials, new_token_dto):
    cred.access_token = new_token_dto.access_token
    cred.expires_in = new_token_dto.expires_in
    cred.expires_at = timezone.now() + timezone.timedelta(seconds=new_token_dto.expires_in)
    if new_token_dto.refresh_token:
        cred.refresh_token = new_token_dto.refresh_token
    cred.save()


async def _ensure_valid_token_for_user(user_id: int) -> Optional[str]:
    creds = await get_credentials(user_id)
    if not creds:
        return None

    if creds.is_expired():
        if not creds.refresh_token:
            return None

        print(f"Refreshing token for user {user_id}")
        refreshed_dto = await refresh_token_with_refresh_token(creds.refresh_token)

        if refreshed_dto is None:
            return None

        await update_credentials(creds, refreshed_dto)
        return refreshed_dto.access_token

    return creds.access_token


async def _spotify_get(access_token: str, path: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    url = f"{API_BASE}{path}"
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url, headers=headers, params=params)
        if resp.status_code == 401:
            return {"error": "token_expired_or_invalid"}
        resp.raise_for_status()
        return resp.json()


async def _spotify_put(access_token: str, path: str, params: Optional[Dict[str, str]] = None,
                       json_body: Any = None) -> bool:
    url = f"{API_BASE}{path}"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.put(url, headers=headers, params=params, json=json_body)
        if resp.status_code == 401:
            return False
        if resp.status_code not in [200, 204]:
            resp.raise_for_status()
        return True


async def search_artist(user_id: int, q: str, limit: int = 5) -> Any:
    token = await _ensure_valid_token_for_user(user_id)
    if not token: return {"error": "no_valid_token"}

    data = await _spotify_get(token, "/search", params={"q": q, "type": "artist", "limit": str(limit)})
    return data


async def search_track(user_id: int, q: str, limit: int = 5) -> Any:
    token = await _ensure_valid_token_for_user(user_id)
    if not token: return {"error": "no_valid_token"}
    return await _spotify_get(token, "/search", params={"q": q, "type": "track", "limit": str(limit)})


async def follow_ids(user_id: int, ids: List[str], type_: str) -> Dict[str, Any]:
    token = await _ensure_valid_token_for_user(user_id)
    if not token: return {"error": "no_valid_token"}

    try:
        await _spotify_put(token, "/me/following", params={"type": type_}, json_body={"ids": ids})
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}


async def get_followed_artists(user_id: int, limit: int = 20) -> Dict[str, Any]:
    token = await _ensure_valid_token_for_user(user_id)
    if not token: return {"error": "no_valid_token"}
    return await _spotify_get(token, "/me/following", params={"type": "artist", "limit": str(limit)})


async def check_following_status(user_id: int, ids: List[str], type_: str) -> Dict[str, Any]:
    token = await _ensure_valid_token_for_user(user_id)
    if not token: return {"error": "no_valid_token"}
    ids_str = ",".join(ids)
    return await _spotify_get(token, "/me/following/contains", params={"type": type_, "ids": ids_str})
