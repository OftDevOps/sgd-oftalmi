from .models import OrganizationalUnit


def organizational_unit_create(*, name, code=None, description="", is_active=True):
    organizational_unit = OrganizationalUnit(
        name=name,
        code=code,
        description=description,
        is_active=is_active,
    )
    organizational_unit.full_clean()
    organizational_unit.save()
    return organizational_unit
