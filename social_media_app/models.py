from django.db import models

from py_social_media import settings


class Profile(models.Model):
    class GenderChoices(models.TextChoices):
        FEMALE = "Female"
        MALE = "Male"
        UNKNOWN = "unknown"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    biography = models.TextField(blank=True)
    gender = models.CharField(max_length=50, choices=GenderChoices.choices)
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="followers", blank=True
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Post(models.Model):
    title = models.CharField(max_length=70)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    hashtag = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title
