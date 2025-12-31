from unittest.mock import patch, AsyncMock

from app.spotify import SpotifyArtistDTO

MOCK_ARTIST = SpotifyArtistDTO(
    id="123", name="Mock Band", href="http://api/1", uri="spotify:artist:1"
)


class TestSpotifyIntegration:

    @patch("app.services.spotify_service.SpotifyService.process_auth_callback", new_callable=AsyncMock)
    def test_spotify_callback_success(self, mock_process, client):
        mock_process.return_value = True

        response = client.get("/users/auth/callback?code=fake_code&state=1")

        assert response.status_code == 200
        assert response.data["message"] == "Spotify Connected!"
        mock_process.assert_called_once_with("fake_code", 1)

    def test_spotify_callback_missing_params(self, client):
        response = client.get("/users/auth/callback?code=only_code")
        assert response.status_code == 400
        assert "Missing code or state" in response.data["detail"]

    @patch("app.services.spotify_service.SpotifyService.find_artist_to_save", new_callable=AsyncMock)
    def test_add_favorite_artist_success(self, mock_find, client, created_user):
        user_id = created_user["id"]
        mock_find.return_value = MOCK_ARTIST

        response = client.post(f"/users/{user_id}/favorites/artists/?artist_name=Band")

        assert response.status_code == 200
        data = response.data
        assert data["name"] == "Mock Band"
        assert data["spotify_id"] == "123"

        user_resp = client.get(f"/users/{user_id}/")
        assert len(user_resp.data["favorite_artists"]) == 1

    @patch("app.services.spotify_service.SpotifyService.find_artist_to_save", new_callable=AsyncMock)
    def test_add_favorite_artist_no_token(self, mock_find, client, created_user):
        user_id = created_user["id"]
        mock_find.side_effect = ValueError("no_valid_token")

        response = client.post(f"/users/{user_id}/favorites/artists/?artist_name=Band")

        assert response.status_code == 401
        assert response.data["message"] == "User not logged in Spotify"

    @patch("app.services.spotify_service.SpotifyService.find_artist_to_save", new_callable=AsyncMock)
    def test_add_favorite_artist_not_found(self, mock_find, client, created_user):
        user_id = created_user["id"]
        mock_find.return_value = None

        response = client.post(f"/users/{user_id}/favorites/artists/?artist_name=UnknownBand")

        assert response.status_code == 404
        assert response.data["detail"] == "Artist not found on Spotify"

    @patch("app.services.spotify_service.SpotifyService.follow_targets", new_callable=AsyncMock)
    def test_follow_artist_endpoint(self, mock_follow, client, created_user):
        user_id = created_user["id"]
        mock_follow.return_value = True

        payload = {"ids": ["id1", "id2"]}

        response = client.put(
            f"/spotify/me/following?user_id={user_id}&type=artist",
            payload,
            format='json'
        )

        assert response.status_code == 200
        mock_follow.assert_called_once()
