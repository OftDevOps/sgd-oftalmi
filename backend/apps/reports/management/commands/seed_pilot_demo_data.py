from calendar import monthrange
from collections import Counter
from datetime import datetime, time, timedelta
from hashlib import sha256

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import ROLE_GROUP_NAMES, UserRole
from apps.controlled_copies.models import ControlledCopy, ControlledCopyStatus
from apps.document_types.models import DocumentType
from apps.documents.models import Document, DocumentFile, DocumentStatus, DocumentVersion
from apps.implementation_records.models import (
    ImplementationRecord,
    ImplementationRecordStatus,
)
from apps.organizational_units.models import OrganizationalUnit


DEMO_PASSWORD = "DemoPilot2026!"

DEMO_UNITS = (
    {
        "code": "OYM",
        "name": "Organizacion y Metodos Demo",
        "description": "Unidad demo duena funcional del piloto controlado.",
        "is_active": True,
    },
    {
        "code": "PROD",
        "name": "Produccion Demo",
        "description": "Unidad ejecutora demo principal para copias e implementacion.",
        "is_active": True,
    },
    {
        "code": "RRHH",
        "name": "Recursos Humanos Demo",
        "description": "Unidad demo secundaria para filtros y escenarios por unidad.",
        "is_active": True,
    },
    {
        "code": "SIS",
        "name": "Sistemas Demo",
        "description": "Unidad tecnica demo sin propiedad funcional sobre reglas OyM.",
        "is_active": True,
    },
    {
        "code": "ADMIN",
        "name": "Administracion Demo",
        "description": "Unidad demo para usuario autenticado sin relacion documental.",
        "is_active": True,
    },
)

DEMO_DOCUMENT_TYPES = (
    {
        "code": "PROC",
        "name": "Procedimiento Demo",
        "description": "Tipo documental demo para procedimientos del piloto.",
        "is_active": True,
    },
    {
        "code": "INST",
        "name": "Instructivo Demo",
        "description": "Tipo documental demo para instructivos del piloto.",
        "is_active": True,
    },
    {
        "code": "FORM",
        "name": "Formato Demo",
        "description": "Tipo documental demo para formatos controlados del piloto.",
        "is_active": True,
    },
    {
        "code": "MAN",
        "name": "Manual Demo",
        "description": "Tipo documental demo para manuales internos del piloto.",
        "is_active": True,
    },
)

DEMO_USERS = (
    {
        "key": "USR-OYM-ADM",
        "email": "oym.admin.demo@oftalmi.test",
        "first_name": "OyM",
        "last_name": "Administrador Demo",
        "role": UserRole.OYM_ADMIN,
        "unit_code": "OYM",
        "is_technical_user": False,
    },
    {
        "key": "USR-OYM-ANA",
        "email": "oym.analista.demo@oftalmi.test",
        "first_name": "OyM",
        "last_name": "Analista Demo",
        "role": UserRole.OYM_ANALYST,
        "unit_code": "OYM",
        "is_technical_user": False,
    },
    {
        "key": "USR-UE-PROD",
        "email": "unidad.produccion.demo@oftalmi.test",
        "first_name": "Unidad",
        "last_name": "Produccion Demo",
        "role": UserRole.EXECUTING_UNIT,
        "unit_code": "PROD",
        "is_technical_user": False,
    },
    {
        "key": "USR-LECT-PROD",
        "email": "lector.produccion.demo@oftalmi.test",
        "first_name": "Lector",
        "last_name": "Produccion Demo",
        "role": UserRole.READER,
        "unit_code": "PROD",
        "is_technical_user": False,
    },
    {
        "key": "USR-AUD",
        "email": "auditor.demo@oftalmi.test",
        "first_name": "Auditor",
        "last_name": "Demo",
        "role": UserRole.AUDITOR,
        "unit_code": "OYM",
        "is_technical_user": False,
    },
    {
        "key": "USR-SIS",
        "email": "sistemas.demo@oftalmi.test",
        "first_name": "Sistemas",
        "last_name": "Tecnico Demo",
        "role": UserRole.SYSTEMS_TECH_ADMIN,
        "unit_code": "SIS",
        "is_technical_user": True,
    },
    {
        "key": "USR-SIN-PERM",
        "email": "sin.permiso.demo@oftalmi.test",
        "first_name": "Sin Permiso",
        "last_name": "Demo",
        "role": UserRole.READER,
        "unit_code": "ADMIN",
        "is_technical_user": False,
    },
)

DEMO_DOCUMENTS = (
    {
        "code": "PROC-OYM-DEMO-001",
        "title": "Procedimiento demo de gestion documental",
        "document_type_code": "PROC",
        "owner_unit_code": "OYM",
        "status": DocumentStatus.ACTIVE,
        "version_number": "1.0",
        "version_status": DocumentStatus.ACTIVE,
        "file_name": "proc-oym-demo-001-v1.pdf",
        "file_active": True,
    },
    {
        "code": "INST-PROD-DEMO-001",
        "title": "Instructivo demo de produccion",
        "document_type_code": "INST",
        "owner_unit_code": "PROD",
        "status": DocumentStatus.PUBLISHED,
        "version_number": "1.0",
        "version_status": DocumentStatus.PUBLISHED,
        "file_name": "inst-prod-demo-001-v1.pdf",
        "file_active": True,
    },
    {
        "code": "FORM-RRHH-DEMO-001",
        "title": "Formato demo de induccion",
        "document_type_code": "FORM",
        "owner_unit_code": "RRHH",
        "status": DocumentStatus.UNDER_REVIEW,
        "version_number": "0.1",
        "version_status": DocumentStatus.UNDER_REVIEW,
        "file_name": "form-rrhh-demo-001-v01.pdf",
        "file_active": False,
    },
    {
        "code": "MAN-OYM-DEMO-001",
        "title": "Manual demo obsoleto",
        "document_type_code": "MAN",
        "owner_unit_code": "OYM",
        "status": DocumentStatus.OBSOLETE,
        "version_number": "1.0",
        "version_status": DocumentStatus.OBSOLETE,
        "file_name": "man-oym-demo-001-v1.pdf",
        "file_active": True,
    },
    {
        "code": "PROC-PROD-DEMO-002",
        "title": "Procedimiento demo sin relacion lector",
        "document_type_code": "PROC",
        "owner_unit_code": "PROD",
        "status": DocumentStatus.ACTIVE,
        "version_number": "1.0",
        "version_status": DocumentStatus.ACTIVE,
        "file_name": "proc-prod-demo-002-v1.pdf",
        "file_active": True,
    },
)

DEMO_CONTROLLED_COPIES = (
    {
        "copy_number": "C-001",
        "document_code": "PROC-OYM-DEMO-001",
        "receiver_unit_code": "PROD",
        "receiver_user_key": "USR-LECT-PROD",
        "status": ControlledCopyStatus.ACTIVE,
        "delivered": True,
        "retired": False,
    },
    {
        "copy_number": "C-002",
        "document_code": "INST-PROD-DEMO-001",
        "receiver_unit_code": "PROD",
        "receiver_user_key": "USR-UE-PROD",
        "status": ControlledCopyStatus.DELIVERED,
        "delivered": True,
        "retired": False,
    },
    {
        "copy_number": "C-003",
        "document_code": "MAN-OYM-DEMO-001",
        "receiver_unit_code": "RRHH",
        "receiver_user_key": None,
        "status": ControlledCopyStatus.RETIRED,
        "delivered": True,
        "retired": True,
    },
    {
        "copy_number": "C-004",
        "document_code": "PROC-PROD-DEMO-002",
        "receiver_unit_code": "RRHH",
        "receiver_user_key": None,
        "status": ControlledCopyStatus.REGISTERED,
        "delivered": False,
        "retired": False,
    },
)

DEMO_IMPLEMENTATION_RECORDS = (
    {
        "user_key": "USR-LECT-PROD",
        "document_code": "PROC-OYM-DEMO-001",
        "status": ImplementationRecordStatus.PENDING,
        "read": False,
        "interpreted": False,
        "accepted": False,
        "implemented": False,
    },
    {
        "user_key": "USR-UE-PROD",
        "document_code": "INST-PROD-DEMO-001",
        "status": ImplementationRecordStatus.IMPLEMENTED,
        "read": True,
        "interpreted": True,
        "accepted": True,
        "implemented": True,
    },
    {
        "user_key": "USR-LECT-PROD",
        "document_code": "INST-PROD-DEMO-001",
        "status": ImplementationRecordStatus.ACCEPTED,
        "read": True,
        "interpreted": True,
        "accepted": True,
        "implemented": False,
    },
)


class Command(BaseCommand):
    help = "Seed fictitious controlled-pilot demo data for SGD-OFTALMI."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show the pilot demo changes without writing to the database.",
        )
        parser.add_argument(
            "--password",
            default=DEMO_PASSWORD,
            help="Password assigned only to newly created demo users.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        password = options["password"]

        self._validate_base_catalogs()
        dates = self._build_dates()
        stats = Counter()

        if dry_run:
            self.stdout.write("DRY-RUN: no pilot demo data will be written.")

        units = self._seed_units(dry_run=dry_run, stats=stats)
        document_types = self._seed_document_types(dry_run=dry_run, stats=stats)
        users = self._seed_users(
            units=units,
            password=password,
            dry_run=dry_run,
            stats=stats,
        )
        documents = self._seed_documents(
            users=users,
            units=units,
            document_types=document_types,
            dates=dates,
            dry_run=dry_run,
            stats=stats,
        )
        self._seed_controlled_copies(
            documents=documents,
            users=users,
            units=units,
            dates=dates,
            dry_run=dry_run,
            stats=stats,
        )
        self._seed_implementation_records(
            documents=documents,
            users=users,
            dates=dates,
            dry_run=dry_run,
            stats=stats,
        )

        summary = (
            "Pilot demo seed plan: "
            if dry_run
            else "Pilot demo seed completed: "
        )
        summary += (
            f"{stats['created']} created, "
            f"{stats['updated']} updated, "
            f"{stats['unchanged']} existing."
        )
        self.stdout.write(self.style.SUCCESS(summary))

    def _validate_base_catalogs(self):
        expected_groups = set(ROLE_GROUP_NAMES.values())
        existing_groups = set(
            Group.objects.filter(name__in=expected_groups).values_list("name", flat=True)
        )
        missing_groups = sorted(expected_groups - existing_groups)
        if missing_groups:
            raise CommandError(
                "Missing base role groups: "
                f"{', '.join(missing_groups)}. "
                "Run `python manage.py seed_base_catalogs` before "
                "`python manage.py seed_pilot_demo_data`."
            )

    def _build_dates(self):
        today = timezone.localdate()
        anchor_day = min(15, monthrange(today.year, today.month)[1])
        anchor_date = today.replace(day=anchor_day)
        current_month_datetime = timezone.make_aware(
            datetime.combine(anchor_date, time(hour=10)),
            timezone.get_current_timezone(),
        )
        previous_datetime = current_month_datetime - timedelta(days=45)
        later_datetime = current_month_datetime + timedelta(days=2)

        return {
            "issue_date": anchor_date,
            "effective_date": anchor_date,
            "expiration_date": anchor_date + timedelta(days=365),
            "published_at": current_month_datetime,
            "obsolete_at": previous_datetime,
            "delivered_at": current_month_datetime,
            "retired_at": later_datetime,
            "assigned_at": current_month_datetime,
            "confirmed_at": later_datetime,
        }

    def _seed_units(self, *, dry_run, stats):
        units = {}
        self.stdout.write("Seeding pilot demo organizational units...")
        for item in DEMO_UNITS:
            action, instance = self._sync_model_by_code(
                model=OrganizationalUnit,
                code=item["code"],
                defaults={
                    "name": item["name"],
                    "description": item["description"],
                    "is_active": item["is_active"],
                },
                dry_run=dry_run,
            )
            units[item["code"]] = instance
            self._record_result(stats, "organizational_unit", item["code"], action)

        return units

    def _seed_document_types(self, *, dry_run, stats):
        document_types = {}
        self.stdout.write("Seeding pilot demo document types...")
        for item in DEMO_DOCUMENT_TYPES:
            action, instance = self._sync_model_by_code(
                model=DocumentType,
                code=item["code"],
                defaults={
                    "name": item["name"],
                    "description": item["description"],
                    "is_active": item["is_active"],
                },
                dry_run=dry_run,
            )
            document_types[item["code"]] = instance
            self._record_result(stats, "document_type", item["code"], action)

        return document_types

    def _seed_users(self, *, units, password, dry_run, stats):
        users = {}
        self.stdout.write("Seeding pilot demo users...")
        for item in DEMO_USERS:
            action, instance = self._sync_user(
                item=item,
                unit=units[item["unit_code"]],
                password=password,
                dry_run=dry_run,
            )
            users[item["key"]] = instance
            self._record_result(stats, "user", item["email"], action)

        return users

    def _seed_documents(self, *, users, units, document_types, dates, dry_run, stats):
        documents = {}
        self.stdout.write("Seeding pilot demo documents, versions and files...")
        created_by = users["USR-OYM-ADM"]
        for item in DEMO_DOCUMENTS:
            action, document = self._sync_document(
                item=item,
                document_type=document_types[item["document_type_code"]],
                owner_unit=units[item["owner_unit_code"]],
                created_by=created_by,
                dry_run=dry_run,
            )
            documents[item["code"]] = {"document": document}
            self._record_result(stats, "document", item["code"], action)

            version_action, version = self._sync_document_version(
                item=item,
                document=document,
                created_by=created_by,
                dates=dates,
                dry_run=dry_run,
            )
            documents[item["code"]]["version"] = version
            self._record_result(
                stats,
                "document_version",
                f"{item['code']} v{item['version_number']}",
                version_action,
            )

            current_action = self._sync_current_version(
                document=document,
                version=version,
                dry_run=dry_run,
            )
            if current_action != "unchanged":
                self._record_result(
                    stats,
                    "document_current_version",
                    item["code"],
                    current_action,
                )

            file_action, document_file = self._sync_document_file(
                item=item,
                version=version,
                uploaded_by=created_by,
                dry_run=dry_run,
            )
            documents[item["code"]]["file"] = document_file
            self._record_result(stats, "document_file", item["file_name"], file_action)

        return documents

    def _seed_controlled_copies(self, *, documents, users, units, dates, dry_run, stats):
        self.stdout.write("Seeding pilot demo controlled copies...")
        created_by = users["USR-OYM-ADM"]
        for item in DEMO_CONTROLLED_COPIES:
            receiver_user = (
                users[item["receiver_user_key"]]
                if item["receiver_user_key"] is not None
                else None
            )
            action, _instance = self._sync_controlled_copy(
                item=item,
                document=documents[item["document_code"]]["document"],
                version=documents[item["document_code"]]["version"],
                receiver_unit=units[item["receiver_unit_code"]],
                receiver_user=receiver_user,
                created_by=created_by,
                dates=dates,
                dry_run=dry_run,
            )
            self._record_result(stats, "controlled_copy", item["copy_number"], action)

    def _seed_implementation_records(self, *, documents, users, dates, dry_run, stats):
        self.stdout.write("Seeding pilot demo implementation records...")
        for item in DEMO_IMPLEMENTATION_RECORDS:
            action, _instance = self._sync_implementation_record(
                item=item,
                user=users[item["user_key"]],
                document=documents[item["document_code"]]["document"],
                version=documents[item["document_code"]]["version"],
                dates=dates,
                dry_run=dry_run,
            )
            self._record_result(
                stats,
                "implementation_record",
                f"{item['user_key']}:{item['document_code']}",
                action,
            )

    def _sync_model_by_code(self, *, model, code, defaults, dry_run):
        instance = model.objects.filter(code=code).first()
        if instance is None:
            if dry_run:
                return "created", None

            instance = model(code=code, **defaults)
            instance.full_clean()
            instance.save()
            return "created", instance

        changes = self._get_changes(instance, defaults)
        if not changes:
            return "unchanged", instance

        if not dry_run:
            for field, value in changes.items():
                setattr(instance, field, value)
            instance.full_clean()
            instance.save(update_fields=[*changes.keys(), "updated_at"])

        return "updated", instance

    def _sync_user(self, *, item, unit, password, dry_run):
        User = get_user_model()
        instance = User.objects.filter(email=item["email"]).first()
        defaults = {
            "first_name": item["first_name"],
            "last_name": item["last_name"],
            "role": item["role"],
            "organizational_unit": unit,
            "is_active": True,
            "is_staff": item["role"] in {UserRole.OYM_ADMIN, UserRole.SYSTEMS_TECH_ADMIN},
            "is_technical_user": item["is_technical_user"],
        }

        if instance is None:
            if dry_run:
                return "created", None

            instance = User.objects.create_user(
                email=item["email"],
                password=password,
                **defaults,
            )
            self._sync_user_group(instance, item["role"])
            return "created", instance

        changes = self._get_changes(instance, defaults)
        expected_group_name = ROLE_GROUP_NAMES[item["role"]]
        role_group_names = set(ROLE_GROUP_NAMES.values())
        current_role_groups = set(
            instance.groups.filter(name__in=role_group_names).values_list(
                "name",
                flat=True,
            )
        )
        group_changes = current_role_groups != {expected_group_name}

        if not changes and not group_changes:
            return "unchanged", instance

        if not dry_run:
            for field, value in changes.items():
                setattr(instance, field, value)
            instance.full_clean()
            instance.save(update_fields=[*changes.keys(), "updated_at"])
            self._sync_user_group(instance, item["role"])

        return "updated", instance

    def _sync_user_group(self, user, role):
        expected_group = Group.objects.get(name=ROLE_GROUP_NAMES[role])
        role_groups = Group.objects.filter(name__in=ROLE_GROUP_NAMES.values())
        user.groups.remove(*role_groups)
        user.groups.add(expected_group)

    def _sync_document(self, *, item, document_type, owner_unit, created_by, dry_run):
        instance = Document.objects.filter(code=item["code"]).first()
        defaults = {
            "title": item["title"],
            "document_type": document_type,
            "owner_unit": owner_unit,
            "status": item["status"],
            "is_active": True,
            "created_by": created_by,
        }
        if instance is None:
            if dry_run:
                return "created", None

            instance = Document(code=item["code"], **defaults)
            instance.full_clean()
            instance.save()
            return "created", instance

        changes = self._get_changes(instance, defaults)
        if not changes:
            return "unchanged", instance

        if not dry_run:
            for field, value in changes.items():
                setattr(instance, field, value)
            instance.full_clean()
            instance.save(update_fields=[*changes.keys(), "updated_at"])

        return "updated", instance

    def _sync_document_version(self, *, item, document, created_by, dates, dry_run):
        instance = DocumentVersion.objects.filter(
            document=document,
            version_number=item["version_number"],
        ).first()
        published_at = (
            dates["published_at"]
            if item["version_status"] in {DocumentStatus.ACTIVE, DocumentStatus.PUBLISHED}
            else None
        )
        obsolete_at = (
            dates["obsolete_at"] if item["version_status"] == DocumentStatus.OBSOLETE else None
        )
        defaults = {
            "status": item["version_status"],
            "issue_date": dates["issue_date"],
            "effective_date": dates["effective_date"],
            "expiration_date": dates["expiration_date"],
            "approved_at": published_at,
            "published_at": published_at,
            "obsolete_at": obsolete_at,
            "created_by": created_by,
        }

        if instance is None:
            if dry_run:
                return "created", None

            instance = DocumentVersion(
                document=document,
                version_number=item["version_number"],
                **defaults,
            )
            instance.full_clean()
            instance.save()
            return "created", instance

        changes = self._get_changes(instance, defaults)
        if not changes:
            return "unchanged", instance

        if not dry_run:
            for field, value in changes.items():
                setattr(instance, field, value)
            instance.full_clean()
            instance.save(update_fields=list(changes.keys()))

        return "updated", instance

    def _sync_current_version(self, *, document, version, dry_run):
        if document is None or version is None:
            return "updated"

        if document.current_version_id == version.id:
            return "unchanged"

        if not dry_run:
            document.current_version = version
            document.full_clean()
            document.save(update_fields=["current_version", "updated_at"])

        return "updated"

    def _sync_document_file(self, *, item, version, uploaded_by, dry_run):
        instance = DocumentFile.objects.filter(
            document_version=version,
            original_filename=item["file_name"],
        ).first()
        content = self._build_pdf_content(item)
        file_hash = sha256(content).hexdigest()
        defaults = {
            "content_type": "application/pdf",
            "size_bytes": len(content),
            "file_hash": file_hash,
            "uploaded_by": uploaded_by,
            "is_active": item["file_active"],
        }

        if instance is None:
            if dry_run:
                return "created", None

            instance = DocumentFile(
                document_version=version,
                original_filename=item["file_name"],
                **defaults,
            )
            instance.file.save(
                item["file_name"],
                ContentFile(content),
                save=False,
            )
            instance.full_clean()
            instance.save()
            return "created", instance

        changes = self._get_changes(instance, defaults)
        file_missing = not instance.file or not instance.file.storage.exists(instance.file.name)
        should_replace_file = file_missing or instance.file_hash != file_hash
        if not changes and not file_missing:
            return "unchanged", instance

        if not dry_run:
            for field, value in changes.items():
                setattr(instance, field, value)
            if should_replace_file:
                instance.file.save(
                    item["file_name"],
                    ContentFile(content),
                    save=False,
                )
            instance.full_clean()
            instance.save()

        return "updated", instance

    def _sync_controlled_copy(
        self,
        *,
        item,
        document,
        version,
        receiver_unit,
        receiver_user,
        created_by,
        dates,
        dry_run,
    ):
        instance = ControlledCopy.objects.filter(
            document_version=version,
            copy_number=item["copy_number"],
        ).first()
        defaults = {
            "document": document,
            "receiver_unit": receiver_unit,
            "receiver_user": receiver_user,
            "delivered_at": dates["delivered_at"] if item["delivered"] else None,
            "retired_at": dates["retired_at"] if item["retired"] else None,
            "status": item["status"],
            "observations": "Registro demo para piloto controlado.",
            "evidence_reference": f"PILOTO-DEMO-{item['copy_number']}",
            "created_by": created_by,
        }
        if instance is None:
            if dry_run:
                return "created", None

            instance = ControlledCopy(
                document_version=version,
                copy_number=item["copy_number"],
                **defaults,
            )
            instance.full_clean()
            instance.save()
            return "created", instance

        changes = self._get_changes(instance, defaults)
        if not changes:
            return "unchanged", instance

        if not dry_run:
            for field, value in changes.items():
                setattr(instance, field, value)
            instance.full_clean()
            instance.save(update_fields=[*changes.keys(), "updated_at"])

        return "updated", instance

    def _sync_implementation_record(self, *, item, user, document, version, dates, dry_run):
        instance = ImplementationRecord.objects.filter(
            user=user,
            document_version=version,
        ).first()
        defaults = {
            "document": document,
            "assigned_at": dates["assigned_at"],
            "read_at": dates["confirmed_at"] if item["read"] else None,
            "interpreted_at": dates["confirmed_at"] if item["interpreted"] else None,
            "accepted_at": dates["confirmed_at"] if item["accepted"] else None,
            "implemented_at": dates["confirmed_at"] if item["implemented"] else None,
            "status": item["status"],
        }
        if instance is None:
            if dry_run:
                return "created", None

            instance = ImplementationRecord(
                user=user,
                document_version=version,
                **defaults,
            )
            instance.full_clean()
            instance.save()
            return "created", instance

        changes = self._get_changes(instance, defaults)
        if not changes:
            return "unchanged", instance

        if not dry_run:
            for field, value in changes.items():
                setattr(instance, field, value)
            instance.full_clean()
            instance.save(update_fields=[*changes.keys(), "updated_at"])

        return "updated", instance

    def _build_pdf_content(self, item):
        text = (
            f"SGD-OFTALMI PILOTO DEMO\n"
            f"Documento ficticio: {item['code']}\n"
            "No contiene informacion productiva.\n"
        )
        return (
            b"%PDF-1.4\n"
            b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
            b"2 0 obj << /Type /Pages /Count 1 /Kids [3 0 R] >> endobj\n"
            b"3 0 obj << /Type /Page /Parent 2 0 R /Resources << >> "
            b"/MediaBox [0 0 612 792] /Contents 4 0 R >> endobj\n"
            + f"4 0 obj << /Length {len(text)} >> stream\n".encode("utf-8")
            + text.encode("utf-8")
            + b"\nendstream endobj\n%%EOF\n"
        )

    def _get_changes(self, instance, defaults):
        changes = {}
        for field, expected in defaults.items():
            current = getattr(instance, field)
            if self._values_differ(current, expected):
                changes[field] = expected

        return changes

    def _values_differ(self, current, expected):
        if hasattr(expected, "pk"):
            return getattr(current, "pk", None) != expected.pk

        return current != expected

    def _record_result(self, stats, catalog_name, key, action):
        stats[action] += 1
        self.stdout.write(f"{catalog_name}: {key} -> {action}")
