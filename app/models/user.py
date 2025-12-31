from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class User(models.Model):
    name = models.CharField(
        max_length=250,
        help_text="Full name of the user"
    )

    age = models.IntegerField(
        help_text="User age, must be adult (+18)"
    )

    music_preferences = models.JSONField(
        default=list,
        blank=True,
        help_text="List of preferred genres"
    )

    class Meta:
        db_table = "users"
        constraints = [
            models.CheckConstraint(
                check=Q(age__gt=18) & Q(age__lt=120),
                name="age_range_ck"
            )
        ]

    def clean(self):

        if self.name:
            if not self.name.strip():
                raise ValidationError({'name': "name cannot be empty or whitespace"})
            self.name = self.name.strip().title()

        if self.age is not None:
            if not (18 < self.age < 120):
                raise ValidationError({'age': "User age must be between 18 and 120"})

        if self.music_preferences:
            if not isinstance(self.music_preferences, list):
                self.music_preferences = []
            else:
                self.music_preferences = [
                    g.strip() for g in self.music_preferences
                    if isinstance(g, str) and g.strip()
                ]

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"<User id={self.id} name={self.name!r}>"
