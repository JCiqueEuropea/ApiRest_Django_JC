from rest_framework import serializers

from app.models import User, SavedArtist, SavedTrack


class SavedArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedArtist
        fields = ['spotify_id', 'name']


class SavedTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedTrack
        fields = ['spotify_id', 'name']


class UserSerializer(serializers.ModelSerializer):
    favorite_artists = SavedArtistSerializer(many=True, read_only=True)
    favorite_tracks = SavedTrackSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'age', 'music_preferences', 'favorite_artists', 'favorite_tracks']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'age', 'music_preferences']
        read_only_fields = ['id']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty")
        return value.strip().title()
