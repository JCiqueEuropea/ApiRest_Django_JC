import pytest
from django.core.exceptions import ValidationError

from app.models import User


class TestUserModels:

    def test_valid_user_creation(self):
        user = User(name="  juan perez  ", age=20, music_preferences=["Rock"])
        user.save()

        assert user.name == "Juan Perez"
        assert user.age == 20

    def test_invalid_age_under_18(self):
        user = User(name="Kid", age=15)
        with pytest.raises(ValidationError) as exc:
            user.full_clean()

        error_dict = exc.value.message_dict
        assert 'age' in error_dict
        assert "User age must be between 18 and 120" in error_dict['age'][0]

    def test_invalid_name_empty(self):
        user = User(name="   ", age=25)
        with pytest.raises(ValidationError) as exc:
            user.save()

        error_dict = exc.value.message_dict
        assert 'name' in error_dict
        assert "name cannot be empty" in str(error_dict['name'][0])

    def test_clean_music_preferences(self):
        user = User(name="Test", age=25, music_preferences=["Rock", "", "  ", "Jazz"])
        user.save()

        assert len(user.music_preferences) == 2
        assert "Rock" in user.music_preferences
        assert "Jazz" in user.music_preferences
