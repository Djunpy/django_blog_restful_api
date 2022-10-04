from rest_framework import permissions


class IsCurrentAuthorOwnerOrReadOnly(permissions.BasePermission):
    """
    Определяет права доступа к посту
    если пользователь владелец, ему доступно редактирование
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # если post запрос делает проверку пользователя
            return obj.author == request.user
