from typing import Any

from django.db.models import QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response

from social_media_app.models import Profile, Post
from social_media_app.permissions import IsPostOwnerOrReadOnly, IsProfileOwnerOrReadOnly
from social_media_app.serializers import (
    ProfileSerializer,
    PostSerializer,
    ProfileDetailSerializer,
    PostCreateUpdateSerializer,
    ProfileCreateUpdateSerializer,
)


class Pagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 30


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().prefetch_related(
        "user__followers",
        "posts",
    )
    serializer_class = ProfileSerializer
    permission_classes = [IsProfileOwnerOrReadOnly]
    pagination_class = Pagination

    def get_queryset(self) -> QuerySet[Profile]:
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")
        gender = self.request.query_params.get("gender")

        queryset = self.queryset

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)

        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        if gender:
            queryset = queryset.filter(gender=gender)

        return queryset.distinct()

    def perform_create(self, serializer: ProfileCreateUpdateSerializer) -> None:
        serializer.save(user=self.request.user)

    def get_serializer_class(
        self,
    ) -> serializers.Serializer:
        if self.action == "retrieve":
            return ProfileDetailSerializer

        if self.action in ["create", "update"]:
            return ProfileCreateUpdateSerializer

        return self.serializer_class

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "first_name",
                type=OpenApiTypes.STR,
                description="Filter by first_name (ex. ?first_name=John)",
            ),
            OpenApiParameter(
                "last_name",
                type=OpenApiTypes.STR,
                description="Filter by last_name (ex. ?last_name=Smith)",
            ),
            OpenApiParameter(
                "gender",
                type=OpenApiTypes.STR,
                description="Filter by gender (ex. ?gender=Male)",
            ),
        ]
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsPostOwnerOrReadOnly]
    pagination_class = Pagination

    def get_queryset(self) -> QuerySet[Post]:
        hashtag = self.request.query_params.get("hashtag")
        title = self.request.query_params.get("title")

        queryset = self.queryset

        if hashtag:
            queryset = queryset.filter(hashtag__icontains=hashtag)

        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset.distinct()

    def perform_create(self, serializer: PostCreateUpdateSerializer) -> None:
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(author=self.request.user, profile=profile)

    def get_serializer_class(
        self,
    ) -> serializers.Serializer:
        if self.action == "retrieve":
            return PostSerializer

        if self.action in ["create", "update"]:
            return PostCreateUpdateSerializer

        return self.serializer_class

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "hashtag",
                type=OpenApiTypes.STR,
                description="Filter by hashtag (ex. ?hashtag=#hashtag)",
            ),
            OpenApiParameter(
                "title",
                type=OpenApiTypes.STR,
                description="Filter by title (ex. ?title=title)",
            ),
        ]
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().list(request, *args, **kwargs)
