from django.db import models
from django.utils import timezone
from .user import User


class SpotifyCredentials(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='spotify_credentials',
        db_constraint=True
    )

    access_token = models.TextField()
    refresh_token = models.TextField(null=True, blank=True)
    token_type = models.CharField(max_length=50)
    expires_in = models.IntegerField()
    expires_at = models.DateTimeField()
    scope = models.TextField()

    class Meta:
        db_table = "spotify_credentials"

    def is_expired(self, margin_seconds: int = 60) -> bool:
        return timezone.now().timestamp() > (self.expires_at.timestamp() - margin_seconds)

    def __str__(self):
        return f"<SpotifyCredentials id={self.id} user_id={self.user_id}>"


class SavedArtist(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorite_artists',
        on_delete=models.CASCADE
    )
    spotify_id = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "saved_artists"
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'spotify_id'],
                name='uq_artist_user_sid'
            )
        ]
        indexes = [
            models.Index(fields=['user', 'spotify_id'], name='ix_artist_user_sid')
        ]

    def __str__(self):
        return f"<SavedArtist id={self.id} spotify_id={self.spotify_id} name={self.name!r}>"


class SavedTrack(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorite_tracks',
        on_delete=models.CASCADE
    )
    spotify_id = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "saved_tracks"
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'spotify_id'],
                name='uq_track_user_sid'
            )
        ]
        indexes = [
            models.Index(fields=['user', 'spotify_id'], name='ix_track_user_sid')
        ]

    def __str__(self):
        return f"<SavedTrack id={self.id} spotify_id={self.spotify_id} name={self.name!r}>"