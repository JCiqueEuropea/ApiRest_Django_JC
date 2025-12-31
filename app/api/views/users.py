from asgiref.sync import async_to_sync
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from app.api.serializers import UserSerializer, UserCreateSerializer, SavedArtistSerializer, SavedTrackSerializer
from app.models import User
from app.services.spotify_service import SpotifyService
from app.services.user_service import UserService


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserCreateSerializer
        return UserSerializer

    @action(detail=True, methods=['post'], url_path='favorites/artists')
    def add_favorite_artist(self, request, pk=None):
        artist_name = request.query_params.get("artist_name")
        if not artist_name:
            return Response({"error": "Missing artist_name query param"}, status=status.HTTP_400_BAD_REQUEST)

        async def _process():
            user = await UserService.get_user_async(pk)
            if not user:
                raise NotFound(detail="User not found")

            try:
                artist_dto = await SpotifyService.find_artist_to_save(user.id, artist_name)
            except ValueError as e:
                if str(e) == "no_valid_token":
                    return Response({"message": "User not logged in Spotify"}, status=status.HTTP_401_UNAUTHORIZED)
                return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if not artist_dto:
                raise NotFound(detail="Artist not found on Spotify")

            saved_artist = await UserService.add_favorite_artist(user, artist_dto)
            return SavedArtistSerializer(saved_artist).data

        try:
            data = async_to_sync(_process)()
            if isinstance(data, Response): return data
            return Response(data)
        except NotFound as e:
            raise e
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    @action(detail=True, methods=['post'], url_path='favorites/tracks')
    def add_favorite_track(self, request, pk=None):
        track_name = request.query_params.get("track_name")
        if not track_name:
            return Response({"error": "Missing track_name query param"}, status=status.HTTP_400_BAD_REQUEST)

        async def _process():
            user = await UserService.get_user_async(pk)
            if not user:
                raise NotFound(detail="User not found")

            try:
                track_dto = await SpotifyService.find_track_to_save(user.id, track_name)
            except ValueError as e:
                if str(e) == "no_valid_token":
                    return Response({"message": "User not logged in Spotify"}, status=status.HTTP_401_UNAUTHORIZED)
                return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if not track_dto:
                raise NotFound(detail="Track not found on Spotify")

            saved_track = await UserService.add_favorite_track(user, track_dto)
            return SavedTrackSerializer(saved_track).data

        try:
            data = async_to_sync(_process)()
            if isinstance(data, Response): return data
            return Response(data)
        except NotFound as e:
            raise e
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class SpotifyCallbackView(APIView):

    def get(self, request):
        code = request.query_params.get("code")
        error = request.query_params.get("error")
        state = request.query_params.get("state")

        if error:
            return Response({"detail": f"Spotify Error: {error}"}, status=status.HTTP_400_BAD_REQUEST)
        if not code or not state:
            return Response({"detail": "Missing code or state"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = int(state)
        except ValueError:
            return Response({"detail": "Invalid state (user_id)"}, status=status.HTTP_400_BAD_REQUEST)

        async def _process():
            return await SpotifyService.process_auth_callback(code, user_id)

        success = async_to_sync(_process)()

        if not success:
            return Response({"detail": "Authentication failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Spotify Connected!", "user_id": user_id})
