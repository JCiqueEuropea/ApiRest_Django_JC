from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import users, spotify

router = DefaultRouter()
router.register(r'users', users.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),

    path('users/auth/callback', users.SpotifyCallbackView.as_view(), name='spotify-callback'),

    path('spotify/auth/<int:user_id>/login', spotify.SpotifyAuthView.as_view(), name='spotify-login'),
    path('spotify/search/artist', spotify.SearchArtistView.as_view(), name='search-artist'),
    path('spotify/search/track', spotify.SearchTrackView.as_view(), name='search-track'),
    path('spotify/me/following', spotify.FollowTargetView.as_view(), name='follow-targets'),
    path('spotify/me/following/artists', spotify.GetFollowedArtistsView.as_view(), name='get-followed'),
    path('spotify/me/following/contains', spotify.CheckFollowingView.as_view(), name='check-following'),
]
