from typing import Any

from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet


class IsPostOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request: Request, view: ViewSet, obj: Any) -> bool:
        if request.method in SAFE_METHODS:
            return True

        return obj.profile == request.user


class IsProfileOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request: Request, view: ViewSet, obj: Any) -> bool:
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user
