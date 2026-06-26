from django.contrib.auth.models import Group

from .models import ROLE_GROUP_NAMES


def user_assign_role(*, user, role, sync_group=True):
    user.role = role
    user.full_clean()
    user.save(update_fields=["role", "updated_at"])

    if sync_group:
        group_name = ROLE_GROUP_NAMES[role]
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.remove(*user.groups.filter(name__in=ROLE_GROUP_NAMES.values()))
        user.groups.add(group)

    return user


def user_set_organizational_unit(*, user, organizational_unit):
    user.organizational_unit = organizational_unit
    user.full_clean()
    user.save(update_fields=["organizational_unit", "updated_at"])
    return user
