from django.urls import path, include
from rest_framework import routers

from social_media_app.views import ProfileViewSet, PostViewSet

router = routers.DefaultRouter()
router.register("profiles", ProfileViewSet)
router.register("posts", PostViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "social"
