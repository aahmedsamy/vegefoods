from rest_framework.permissions import BasePermission


class IsMyProfile(BasePermission):
    def has_permission(self, request, view):
        pk = int(request.resolver_match.kwargs.get('pk'))
        return request.user.is_authenticated and pk == request.user.id


class EmailIsNotVerified(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.email_is_verified()


class PhoneNumberIsNotVerified(BasePermission):
    def has_permission(self, request, view):
        return not request.user.phone_number_is_verified()


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser



