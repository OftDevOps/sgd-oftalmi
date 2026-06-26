from apps.accounts.models import UserRole
from apps.accounts.permissions import has_any_role, is_oym_user


def can_create_document_request(user):
    return has_any_role(
        user,
        {
            UserRole.OYM_ADMIN,
            UserRole.OYM_ANALYST,
            UserRole.EXECUTING_UNIT,
            UserRole.SYSTEMS_TECH_ADMIN,
        },
    )


def can_view_own_document_request(user, document_request):
    return bool(user and document_request and document_request.requested_by_id == user.id)


def can_view_all_document_requests(user):
    return is_oym_user(user)


def can_process_document_request(user):
    return is_oym_user(user)


def can_observe_document_request(user):
    return is_oym_user(user)


def can_close_document_request(user):
    return is_oym_user(user)
