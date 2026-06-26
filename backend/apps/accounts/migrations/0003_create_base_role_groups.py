from django.db import migrations


ROLE_GROUP_NAMES = [
    "OYM_ADMIN",
    "OYM_ANALYST",
    "EXECUTING_UNIT",
    "READER",
    "SYSTEMS_TECH_ADMIN",
    "AUDITOR",
]


def create_base_role_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")

    for group_name in ROLE_GROUP_NAMES:
        Group.objects.get_or_create(name=group_name)


def remove_base_role_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=ROLE_GROUP_NAMES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_user_is_technical_user_user_organizational_unit_and_more"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_base_role_groups, remove_base_role_groups),
    ]
