from django.contrib.auth import get_user_model


def user_list(*, role=None, is_active=None, organizational_unit=None):
    queryset = get_user_model().objects.select_related("organizational_unit").all()

    if role is not None:
        queryset = queryset.filter(role=role)
    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)
    if organizational_unit is not None:
        queryset = queryset.filter(organizational_unit=organizational_unit)

    return queryset


def user_get_by_email(email):
    if not email:
        return None

    normalized_email = get_user_model().objects.normalize_email(email)
    return (
        get_user_model()
        .objects.select_related("organizational_unit")
        .filter(email=normalized_email)
        .first()
    )
