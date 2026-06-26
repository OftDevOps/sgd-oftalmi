from .models import OrganizationalUnit


def organizational_unit_list(*, is_active=None):
    queryset = OrganizationalUnit.objects.all()

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset


def organizational_unit_get_by_code(code):
    if not code:
        return None

    return OrganizationalUnit.objects.filter(code=code).first()
