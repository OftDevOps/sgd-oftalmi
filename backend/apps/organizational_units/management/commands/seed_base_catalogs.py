from collections import Counter

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.accounts.models import ROLE_GROUP_NAMES
from apps.document_types.models import DocumentType
from apps.organizational_units.models import OrganizationalUnit


BASE_ORGANIZATIONAL_UNITS = (
    {
        "code": "OYM",
        "name": "Organizacion y Metodos",
        "description": "Dueno funcional del MVP y administrador funcional de la gestion documental.",
        "is_active": True,
    },
    {
        "code": "GGC",
        "name": "Gerencia de Garantia de la Calidad",
        "description": "Unidad usuaria, consultora o destinataria cuando aplique bajo metodologia OyM.",
        "is_active": True,
    },
    {
        "code": "SIS",
        "name": "Sistemas",
        "description": "Responsable tecnico de plataforma, soporte y operacion; tambien puede actuar como unidad usuaria.",
        "is_active": True,
    },
    {
        "code": "PROD",
        "name": "Produccion",
        "description": "Unidad ejecutora definida como referencia base del MVP.",
        "is_active": True,
    },
    {
        "code": "RRHH",
        "name": "Recursos Humanos",
        "description": "Unidad ejecutora definida como referencia base del MVP.",
        "is_active": True,
    },
    {
        "code": "ADM",
        "name": "Administracion",
        "description": "Unidad ejecutora definida como referencia base del MVP.",
        "is_active": True,
    },
)

BASE_DOCUMENT_TYPES = (
    {
        "code": "FOR",
        "name": "Formato",
        "description": "Tipo documental referenciado por la codificacion validada FOR-GGHD-010.",
        "is_active": True,
    },
    {
        "code": "DOC",
        "name": "Documento",
        "description": "Tipo documental referenciado por codigos documentales base como DOC-GGHD-004.",
        "is_active": True,
    },
)


class Command(BaseCommand):
    help = "Seed base catalogs validated for the SGD-OFTALMI MVP."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show the catalog changes without writing to the database.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        stats = Counter()

        if dry_run:
            self.stdout.write("DRY-RUN: no database changes will be written.")

        self.stdout.write("Seeding role groups...")
        for group_name in ROLE_GROUP_NAMES.values():
            action = self._sync_group(group_name=group_name, dry_run=dry_run)
            stats[action] += 1
            self._write_result("role_group", group_name, action, dry_run=dry_run)

        self.stdout.write("Seeding organizational units...")
        for item in BASE_ORGANIZATIONAL_UNITS:
            action = self._sync_model_by_code(
                model=OrganizationalUnit,
                code=item["code"],
                defaults={
                    "name": item["name"],
                    "description": item["description"],
                    "is_active": item["is_active"],
                },
                dry_run=dry_run,
            )
            stats[action] += 1
            self._write_result(
                "organizational_unit",
                item["code"],
                action,
                dry_run=dry_run,
            )

        self.stdout.write("Seeding document types...")
        for item in BASE_DOCUMENT_TYPES:
            action = self._sync_model_by_code(
                model=DocumentType,
                code=item["code"],
                defaults={
                    "name": item["name"],
                    "description": item["description"],
                    "is_active": item["is_active"],
                },
                dry_run=dry_run,
            )
            stats[action] += 1
            self._write_result("document_type", item["code"], action, dry_run=dry_run)

        if dry_run:
            summary = (
                "Seed plan: "
                f"{stats['created']} to create, "
                f"{stats['updated']} to update, "
                f"{stats['unchanged']} unchanged."
            )
        else:
            summary = (
                "Seed completed: "
                f"{stats['created']} created, "
                f"{stats['updated']} updated, "
                f"{stats['unchanged']} unchanged."
            )

        self.stdout.write(self.style.SUCCESS(summary))

    def _sync_group(self, *, group_name, dry_run):
        if Group.objects.filter(name=group_name).exists():
            return "unchanged"

        if not dry_run:
            Group.objects.create(name=group_name)

        return "created"

    def _sync_model_by_code(self, *, model, code, defaults, dry_run):
        instance = model.objects.filter(code=code).first()

        if instance is None:
            if not dry_run:
                instance = model(code=code, **defaults)
                instance.full_clean()
                instance.save()

            return "created"

        changes = {
            field: value
            for field, value in defaults.items()
            if getattr(instance, field) != value
        }

        if not changes:
            return "unchanged"

        if not dry_run:
            for field, value in changes.items():
                setattr(instance, field, value)

            instance.full_clean()
            instance.save(update_fields=[*changes.keys(), "updated_at"])

        return "updated"

    def _write_result(self, catalog_name, key, action, *, dry_run):
        display_action = action
        if dry_run and action in {"created", "updated"}:
            display_action = {
                "created": "would create",
                "updated": "would update",
            }[action]

        self.stdout.write(f"{catalog_name}: {key} -> {display_action}")
