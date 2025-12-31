from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404
from app.models import User, SavedArtist, SavedTrack


class UserService:

    @staticmethod
    def get_user(user_id: int) -> User:
        return get_object_or_404(User, pk=user_id)

    @staticmethod
    @sync_to_async
    def get_user_async(user_id: int):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    @sync_to_async
    def add_favorite_artist(user: User, artist_dto) -> SavedArtist:
        obj, created = SavedArtist.objects.get_or_create(
            user=user,
            spotify_id=artist_dto.id,
            defaults={'name': artist_dto.name}
        )
        return obj

    @staticmethod
    @sync_to_async
    def add_favorite_track(user: User, track_dto) -> SavedTrack:
        obj, created = SavedTrack.objects.get_or_create(
            user=user,
            spotify_id=track_dto.id,
            defaults={'name': track_dto.name}
        )
        return obj