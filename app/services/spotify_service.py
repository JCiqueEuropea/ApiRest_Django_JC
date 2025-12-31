from django.shortcuts import get_object_or_404
from django.utils import timezone
from asgiref.sync import sync_to_async

from app.models import User, SpotifyCredentials
from app.spotify import auth, client


class SpotifyService:

    @staticmethod
    def get_login_url(user_id: int) -> str:
        return auth.build_authorize_url(user_id)

    @staticmethod
    async def process_auth_callback(code: str, user_id: int) -> bool:
        token_dto = await auth.exchange_code_for_token(code)
        if not token_dto:
            return False

        @sync_to_async
        def save_token():
            user = get_object_or_404(User, pk=user_id)
            expires_at = timezone.now() + timezone.timedelta(seconds=token_dto.expires_in)

            SpotifyCredentials.objects.update_or_create(
                user=user,
                defaults={
                    'access_token': token_dto.access_token,
                    'refresh_token': token_dto.refresh_token,
                    'token_type': token_dto.token_type,
                    'expires_in': token_dto.expires_in,
                    'expires_at': expires_at,
                    'scope': token_dto.scope
                }
            )

        await save_token()
        return True

    @staticmethod
    async def search_artists_raw(user_id: int, q: str):
        return await client.search_artist(user_id, q)

    @staticmethod
    async def search_tracks_raw(user_id: int, q: str):
        return await client.search_track(user_id, q)

    @staticmethod
    async def follow_targets(user_id: int, ids: list, target_type: str):
        result = await client.follow_ids(user_id, ids, target_type)
        if "error" in result:
            raise ValueError(result["error"])
        return result

    @staticmethod
    async def get_my_followed_artists(user_id: int):
        data = await client.get_followed_artists(user_id)
        if "error" in data:
            raise ValueError(data["error"])
        return data.get("artists", {}).get("items", [])

    @staticmethod
    async def check_if_following(user_id: int, ids: list, target_type: str):
        return await client.check_following_status(user_id, ids, target_type)

    @staticmethod
    async def find_artist_to_save(user_id: int, artist_name: str):
        data = await client.search_artist(user_id, artist_name, limit=1)
        if "error" in data:
            raise ValueError(data["error"])

        items = data.get("artists", {}).get("items", [])
        if not items:
            return None

        item = items[0]

        from app.spotify.dtos import SpotifyArtistDTO
        return SpotifyArtistDTO(**item)
