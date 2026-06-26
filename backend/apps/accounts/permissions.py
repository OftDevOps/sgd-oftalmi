from .models import UserRole


OYM_ROLES = {UserRole.OYM_ADMIN, UserRole.OYM_ANALYST}
FUNCTIONAL_USER_ROLES = {
    UserRole.OYM_ADMIN,
    UserRole.OYM_ANALYST,
    UserRole.EXECUTING_UNIT,
    UserRole.READER,
}


def is_active_user(user):
    return bool(user and user.is_authenticated and user.is_active)


def has_any_role(user, roles):
    return is_active_user(user) and user.role in roles


def is_oym_user(user):
    return has_any_role(user, OYM_ROLES)


def is_oym_admin(user):
    return has_any_role(user, {UserRole.OYM_ADMIN})


def is_systems_tech_admin(user):
    return has_any_role(user, {UserRole.SYSTEMS_TECH_ADMIN})


def can_view_users(user):
    return has_any_role(user, {UserRole.OYM_ADMIN, UserRole.SYSTEMS_TECH_ADMIN})


def can_manage_users(user):
    return has_any_role(user, {UserRole.OYM_ADMIN, UserRole.SYSTEMS_TECH_ADMIN})


def can_change_user_roles(user):
    return has_any_role(user, {UserRole.OYM_ADMIN})
