from asgiref.sync import async_to_sync
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.services.spotify_service import SpotifyService
from app.services.user_service import UserService


class SpotifyAuthView(APIView):

    def get(self, request, user_id):
        async def _check_user():
            return await UserService.get_user_async(user_id)

        user = async_to_sync(_check_user)()

        if not user:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        url = SpotifyService.get_login_url(user_id)
        return redirect(url)


class SearchArtistView(APIView):

    def get(self, request):
        user_id = request.query_params.get('user_id')
        q = request.query_params.get('q')

        if not user_id or not q:
            return Response({"detail": "Missing user_id or q"}, status=status.HTTP_400_BAD_REQUEST)

        async def _search():
            return await SpotifyService.search_artists_raw(int(user_id), q)

        data = async_to_sync(_search)()

        if "error" in data:
            code = 401 if data["error"] == "no_valid_token" else 400
            return Response(data, status=code)

        return Response(data)


class SearchTrackView(APIView):

    def get(self, request):
        user_id = request.query_params.get('user_id')
        q = request.query_params.get('q')

        if not user_id or not q:
            return Response({"detail": "Missing user_id or q"}, status=status.HTTP_400_BAD_REQUEST)

        async def _search():
            return await SpotifyService.search_tracks_raw(int(user_id), q)

        data = async_to_sync(_search)()

        if "error" in data:
            code = 401 if data["error"] == "no_valid_token" else 400
            return Response(data, status=code)

        return Response(data)


class FollowTargetView(APIView):

    def put(self, request):
        user_id = request.query_params.get('user_id')
        target_type = request.query_params.get('type')
        ids = request.data.get('ids')

        if not user_id or not target_type or not ids:
            return Response({"detail": "Missing required params"}, status=status.HTTP_400_BAD_REQUEST)

        if target_type not in ['artist', 'user']:
            return Response({"detail": "Invalid type"}, status=status.HTTP_400_BAD_REQUEST)

        async def _follow():
            try:
                await SpotifyService.follow_targets(int(user_id), ids, target_type)
                return Response({"message": f"Successfully followed {len(ids)} {target_type}(s)"})
            except ValueError as e:
                if str(e) == "no_valid_token":
                    return Response(
                        {"detail": "User not authenticated with Spotify (Requires new login for scope update)"},
                        status=status.HTTP_401_UNAUTHORIZED)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            return async_to_sync(_follow)()
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetFollowedArtistsView(APIView):

    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"detail": "Missing user_id"}, status=status.HTTP_400_BAD_REQUEST)

        async def _get_artists():
            try:
                artists = await SpotifyService.get_my_followed_artists(int(user_id))
                return Response({"count": len(artists), "items": artists})
            except ValueError as e:
                if str(e) == "no_valid_token":
                    return Response({"detail": "User not authenticated with Spotify"},
                                    status=status.HTTP_401_UNAUTHORIZED)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return async_to_sync(_get_artists)()


class CheckFollowingView(APIView):

    def get(self, request):
        user_id = request.query_params.get('user_id')
        ids_param = request.query_params.get('ids')
        target_type = request.query_params.get('type')

        if not user_id or not ids_param or not target_type:
            return Response({"detail": "Missing params"}, status=status.HTTP_400_BAD_REQUEST)

        id_list = [item_id.strip() for item_id in ids_param.split(",")]

        async def _check():
            try:
                results = await SpotifyService.check_if_following(int(user_id), id_list, target_type)
                response_data = []
                for spotify_id, is_following in zip(id_list, results):
                    response_data.append({"id": spotify_id, "is_following": is_following})
                return Response(response_data)
            except ValueError as e:
                if str(e) == "no_valid_token":
                    return Response({"detail": "User not authenticated with Spotify"},
                                    status=status.HTTP_401_UNAUTHORIZED)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return async_to_sync(_check)()
