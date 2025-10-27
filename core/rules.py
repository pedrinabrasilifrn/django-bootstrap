import rules
from django.contrib.auth.models import AnonymousUser

from accounts.models import UserRole


@rules.predicate
def is_superadmin(request):
    if isinstance(request.user, AnonymousUser):
        return False
    return request.user.is_superuser


@rules.predicate
def is_admin(request):
    if isinstance(request.user, AnonymousUser):
        return False
    return request.user.is_superuser or request.user.role == UserRole.ADMIN


@rules.predicate
def is_user(request):
    if isinstance(request.user, AnonymousUser):
        return False
    return request.user.role == UserRole.COMMON or request.user.role == UserRole.ADMIN or request.user.is_superuser


rules.add_rule("is_user_rule", is_user)
rules.add_rule("is_superadmin_rule", is_superadmin)
rules.add_rule("is_admin_rule", is_admin)
