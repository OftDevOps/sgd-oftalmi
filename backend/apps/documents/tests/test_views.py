import shutil
import tempfile
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse

from apps.accounts.models import UserRole
from apps.audit.models import AuditAction, AuditEvent, AuditResult
from apps.controlled_copies.models import ControlledCopy, ControlledCopyStatus
from apps.document_types.models import DocumentType
from apps.documents.models import Document, DocumentFile, DocumentStatus, DocumentVersion
from apps.implementation_records.models import ImplementationRecord
from apps.organizational_units.models import OrganizationalUnit


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class DocumentViewsTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        media_root = cls._overridden_settings["MEDIA_ROOT"]
        super().tearDownClass()
        shutil.rmtree(media_root, ignore_errors=True)

    def create_user(self, role, prefix, organizational_unit=None):
        return get_user_model().objects.create_user(
            email=f"{prefix}@oftalmi.test",
            role=role,
            organizational_unit=organizational_unit,
        )

    def assert_document_access_event(self, event, *, user, result, description):
        self.assertEqual(event.user, user)
        self.assertEqual(event.action, AuditAction.DOCUMENT_VIEWED)
        self.assertEqual(event.result, result)
        self.assertEqual(event.module, "documents")
        self.assertEqual(event.entity_type, "DocumentFile")
        self.assertEqual(event.entity_id, str(self.active_file.pk))
        self.assertEqual(event.description, description)
        self.assertIsNotNone(event.created_at)
        self.assertEqual(event.after_data["document_id"], self.active_document.pk)
        self.assertEqual(event.after_data["document_code"], self.active_document.code)
        self.assertEqual(event.after_data["document_title"], self.active_document.title)
        self.assertEqual(event.after_data["document_status"], self.active_document.status)
        self.assertEqual(event.after_data["document_version_id"], self.active_version.pk)
        self.assertEqual(event.after_data["version_number"], self.active_version.version_number)
        self.assertEqual(event.after_data["version_status"], self.active_version.status)
        self.assertEqual(event.after_data["document_file_id"], self.active_file.pk)
        self.assertEqual(event.after_data["original_filename"], self.active_file.original_filename)
        self.assertEqual(event.after_data["content_type"], self.active_file.content_type)
        self.assertEqual(event.after_data["size_bytes"], self.active_file.size_bytes)
        self.assertEqual(event.after_data["file_hash"], self.active_file.file_hash)

    def setUp(self):
        self.document_type = DocumentType.objects.create(code="FOR", name="Formato")
        self.owner_unit = OrganizationalUnit.objects.create(
            name="Organizacion y Metodos",
            code="OYM",
        )
        self.production_unit = OrganizationalUnit.objects.create(
            name="Produccion",
            code="PROD",
        )
        self.hr_unit = OrganizationalUnit.objects.create(
            name="Recursos Humanos",
            code="RRHH",
        )
        self.oym_admin = self.create_user(UserRole.OYM_ADMIN, "oym_admin")
        self.oym_analyst = self.create_user(UserRole.OYM_ANALYST, "oym_analyst")
        self.executing_unit = self.create_user(
            UserRole.EXECUTING_UNIT,
            "executing_unit",
            organizational_unit=self.owner_unit,
        )
        self.other_executing_unit = self.create_user(
            UserRole.EXECUTING_UNIT,
            "other_executing_unit",
            organizational_unit=self.production_unit,
        )
        self.reader = self.create_user(
            UserRole.READER,
            "reader",
            organizational_unit=self.production_unit,
        )
        self.other_reader = self.create_user(
            UserRole.READER,
            "other_reader",
            organizational_unit=self.hr_unit,
        )
        self.systems_admin = self.create_user(UserRole.SYSTEMS_TECH_ADMIN, "systems_admin")
        self.auditor = self.create_user(UserRole.AUDITOR, "auditor")

        self.active_document = Document.objects.create(
            code="FOR-OYM-001",
            title="Registro de Recepcion de Informacion",
            document_type=self.document_type,
            owner_unit=self.owner_unit,
            created_by=self.oym_admin,
            status=DocumentStatus.ACTIVE,
        )
        self.active_version = DocumentVersion.objects.create(
            document=self.active_document,
            version_number="01",
            status=DocumentStatus.PUBLISHED,
            created_by=self.oym_admin,
        )
        self.active_document.current_version = self.active_version
        self.active_document.save(update_fields=["current_version", "updated_at"])

        self.active_file = DocumentFile.objects.create(
            document_version=self.active_version,
            file=SimpleUploadedFile(
                "for-oym-001-v01.pdf",
                b"%PDF-1.4 controlled file",
                content_type="application/pdf",
            ),
            original_filename="for-oym-001-v01.pdf",
            content_type="application/pdf",
            size_bytes=2048,
            file_hash="hash-v01",
            uploaded_by=self.oym_admin,
        )

        self.draft_version = DocumentVersion.objects.create(
            document=self.active_document,
            version_number="02",
            status=DocumentStatus.DRAFT,
            created_by=self.oym_admin,
        )
        self.draft_file = DocumentFile.objects.create(
            document_version=self.draft_version,
            file=SimpleUploadedFile(
                "for-oym-001-v02.pdf",
                b"%PDF-1.4 draft file",
                content_type="application/pdf",
            ),
            original_filename="for-oym-001-v02.pdf",
            content_type="application/pdf",
            size_bytes=3072,
            file_hash="hash-v02",
            uploaded_by=self.oym_admin,
        )

        self.obsolete_document = Document.objects.create(
            code="FOR-OYM-009",
            title="Documento obsoleto",
            document_type=self.document_type,
            owner_unit=self.owner_unit,
            created_by=self.oym_admin,
            status=DocumentStatus.OBSOLETE,
        )
        self.obsolete_version = DocumentVersion.objects.create(
            document=self.obsolete_document,
            version_number="01",
            status=DocumentStatus.OBSOLETE,
            created_by=self.oym_admin,
        )
        self.obsolete_document.current_version = self.obsolete_version
        self.obsolete_document.save(update_fields=["current_version", "updated_at"])

    def test_list_requires_login(self):
        response = self.client.get(reverse("app:documents:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_allowed_roles_can_view_visible_documents(self):
        allowed_roles = (
            UserRole.OYM_ADMIN,
            UserRole.OYM_ANALYST,
            UserRole.EXECUTING_UNIT,
            UserRole.READER,
        )

        for role in allowed_roles:
            with self.subTest(role=role):
                self.client.logout()
                self.client.force_login(self.create_user(role, f"allowed-{role}"))

                response = self.client.get(reverse("app:documents:index"))

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "Documentos")
                self.assertContains(response, "FOR-OYM-001")
                if role in (UserRole.OYM_ADMIN, UserRole.OYM_ANALYST):
                    self.assertContains(response, "FOR-OYM-009")
                else:
                    self.assertNotContains(response, "FOR-OYM-009")

    def test_disallowed_role_cannot_view_list(self):
        self.client.force_login(self.systems_admin)

        response = self.client.get(reverse("app:documents:index"))

        self.assertEqual(response.status_code, 403)

    def test_oym_can_view_detail_with_versions_and_file_metadata(self):
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse("app:documents:detail", args=[self.active_document.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FOR-OYM-001 - Registro de Recepcion de Informacion")
        self.assertContains(response, "01")
        self.assertContains(response, "02")
        self.assertContains(response, "for-oym-001-v01.pdf")
        self.assertContains(response, "for-oym-001-v02.pdf")
        self.assertContains(response, "hash-v01")
        self.assertContains(response, "hash-v02")

    def test_reader_sees_only_visible_versions_in_detail(self):
        self.client.force_login(self.reader)

        response = self.client.get(
            reverse("app:documents:detail", args=[self.active_document.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FOR-OYM-001 - Registro de Recepcion de Informacion")
        self.assertContains(response, "01")
        self.assertContains(response, "for-oym-001-v01.pdf")
        self.assertNotContains(response, "for-oym-001-v02.pdf")
        self.assertNotContains(response, "hash-v02")

    def test_reader_cannot_view_obsolete_document_detail(self):
        self.client.force_login(self.reader)

        response = self.client.get(
            reverse("app:documents:detail", args=[self.obsolete_document.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_controlled_file_view_requires_login(self):
        response = self.client.get(
            reverse(
                "app:documents:file_view",
                args=[
                    self.active_document.pk,
                    self.active_version.pk,
                    self.active_file.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])
        self.assertEqual(AuditEvent.objects.count(), 0)

    def test_controlled_viewer_requires_login(self):
        response = self.client.get(
            reverse(
                "app:documents:file_viewer",
                args=[
                    self.active_document.pk,
                    self.active_version.pk,
                    self.active_file.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_reader_can_open_controlled_viewer_when_related_by_unit_copy(self):
        ControlledCopy.objects.create(
            document=self.active_document,
            document_version=self.active_version,
            copy_number="CC-003",
            receiver_unit=self.production_unit,
            status=ControlledCopyStatus.ACTIVE,
            created_by=self.oym_admin,
        )
        self.client.force_login(self.reader)

        response = self.client.get(
            reverse(
                "app:documents:file_viewer",
                args=[
                    self.active_document.pk,
                    self.active_version.pk,
                    self.active_file.pk,
                ],
            )
        )

        file_view_url = reverse(
            "app:documents:file_view",
            args=[
                self.active_document.pk,
                self.active_version.pk,
                self.active_file.pk,
            ],
        )
        viewer_file_url = f"{file_view_url}#toolbar=0&amp;navpanes=0&amp;scrollbar=1"
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "documents/document_viewer.html")
        self.assertContains(response, "Consulta controlada de archivo PDF documental")
        self.assertContains(response, self.active_file.original_filename)
        self.assertContains(response, viewer_file_url)
        self.assertContains(response, "<iframe", html=False)
        self.assertContains(response, 'sandbox="allow-same-origin allow-scripts"', html=False)
        self.assertContains(response, 'referrerpolicy="same-origin"', html=False)
        self.assertContains(response, "contextmenu")
        self.assertContains(response, "event.preventDefault()")
        self.assertContains(response, '["s", "p", "c"]')
        self.assertContains(response, "viewer-watermark")
        self.assertContains(response, "Usuario:")
        self.assertContains(response, self.reader.email)
        self.assertContains(response, "Unidad:")
        self.assertContains(response, self.production_unit.name)
        self.assertContains(response, "Documento:")
        self.assertContains(response, self.active_document.code)
        self.assertContains(response, "Version:")
        self.assertContains(response, self.active_version.version_number)
        self.assertContains(response, "Fecha/hora:")
        self.assertContains(
            response,
            "La impresion de documentos controlados no esta permitida desde el visor.",
        )
        self.assertContains(response, "print-restriction-message")
        self.assertNotContains(response, f'href="{file_view_url}', html=False)
        self.assertNotContains(response, " download", html=False)
        self.assertNotContains(response, "Imprimir")
        self.assertNotContains(response, "window.print")
        self.assertNotContains(response, self.active_file.file.url)

    def test_viewer_watermark_styles_overlay_document_frame(self):
        css_path = Path(settings.BASE_DIR) / "static" / "css" / "app.css"
        css = css_path.read_text(encoding="utf-8")

        self.assertIn(".viewer-watermark", css)
        self.assertIn("position: absolute", css)
        self.assertIn("pointer-events: none", css)
        self.assertIn("z-index: 2", css)
        self.assertIn(".viewer-watermark-content", css)
        self.assertIn("transform: rotate(-24deg)", css)

    def test_viewer_print_styles_hide_document_frame(self):
        css_path = Path(settings.BASE_DIR) / "static" / "css" / "app.css"
        css = css_path.read_text(encoding="utf-8")

        self.assertIn("@media print", css)
        self.assertIn(".viewer-panel", css)
        self.assertIn(".document-viewer-frame", css)
        self.assertIn("display: none !important", css)
        self.assertIn(".print-restriction-message", css)
        self.assertIn("display: block", css)

    def test_controlled_viewer_returns_403_message_for_disallowed_user(self):
        self.client.force_login(self.systems_admin)

        response = self.client.get(
            reverse(
                "app:documents:file_viewer",
                args=[
                    self.active_document.pk,
                    self.active_version.pk,
                    self.active_file.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "documents/document_viewer.html")
        self.assertContains(
            response,
            "No tiene permiso para visualizar este archivo",
            status_code=403,
        )
        self.assertNotContains(response, "<iframe", html=False, status_code=403)
        event = AuditEvent.objects.get()
        self.assert_document_access_event(
            event,
            user=self.systems_admin,
            result=AuditResult.DENIED,
            description="Document viewer access denied.",
        )

    def test_controlled_viewer_returns_404_message_for_missing_file_record(self):
        self.client.force_login(self.reader)

        response = self.client.get(
            reverse(
                "app:documents:file_viewer",
                args=[
                    self.active_document.pk,
                    self.active_version.pk,
                    999999,
                ],
            )
        )

        self.assertEqual(response.status_code, 404)
        self.assertContains(
            response,
            "El documento, version o archivo solicitado no existe",
            status_code=404,
        )
        self.assertNotContains(response, "<iframe", html=False, status_code=404)
        self.assertEqual(AuditEvent.objects.count(), 0)

    def test_controlled_viewer_returns_404_message_for_missing_physical_file(self):
        self.active_file.file.storage.delete(self.active_file.file.name)
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse(
                "app:documents:file_viewer",
                args=[
                    self.active_document.pk,
                    self.active_version.pk,
                    self.active_file.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 404)
        self.assertContains(
            response,
            "El archivo documental no esta disponible",
            status_code=404,
        )
        self.assertNotContains(response, "<iframe", html=False, status_code=404)
        event = AuditEvent.objects.get()
        self.assert_document_access_event(
            event,
            user=self.oym_admin,
            result=AuditResult.FAILURE,
            description="Document viewer access failed because the file is unavailable.",
        )

    def test_controlled_file_view_records_failure_when_physical_file_is_missing(self):
        self.active_file.file.storage.delete(self.active_file.file.name)
        self.client.force_login(self.oym_admin)

        response = self.client.get(
            reverse(
                "app:documents:file_view",
                args=[
                    self.active_document.pk,
                    self.active_version.pk,
                    self.active_file.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 404)
        event = AuditEvent.objects.get()
        self.assert_document_access_event(
            event,
            user=self.oym_admin,
            result=AuditResult.FAILURE,
            description="Document viewer access failed because the file is unavailable.",
        )

    def test_document_detail_links_to_viewer_when_user_can_view_file(self):
        ControlledCopy.objects.create(
            document=self.active_document,
            document_version=self.active_version,
            copy_number="CC-004",
            receiver_unit=self.production_unit,
            status=ControlledCopyStatus.ACTIVE,
            created_by=self.oym_admin,
        )
        self.client.force_login(self.reader)

        response = self.client.get(
            reverse("app:documents:detail", args=[self.active_document.pk])
        )

        viewer_url = reverse(
            "app:documents:file_viewer",
            args=[
                self.active_document.pk,
                self.active_version.pk,
                self.active_file.pk,
            ],
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Abrir visor")
        self.assertContains(response, viewer_url)
        self.assertNotContains(response, self.active_file.file.url)

    def test_reader_can_view_active_pdf_through_controlled_route(self):
        ControlledCopy.objects.create(
            document=self.active_document,
            document_version=self.active_version,
            copy_number="CC-001",
            receiver_unit=self.production_unit,
            status=ControlledCopyStatus.ACTIVE,
            created_by=self.oym_admin,
        )
        self.client.force_login(self.reader)

        response = self.client.get(
            reverse(
                "app:documents:file_view",
                args=[
                    self.active_document.pk,
                    self.active_version.pk,
                    self.active_file.pk,
                ],
            ),
            HTTP_USER_AGENT="viewer-test",
            REMOTE_ADDR="127.0.0.1",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertIn("inline", response["Content-Disposition"])
        self.assertNotIn("attachment", response["Content-Disposition"].lower())
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertEqual(response["Pragma"], "no-cache")
        self.assertEqual(response["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response["X-Frame-Options"], "SAMEORIGIN")
        self.assertEqual(response["Content-Security-Policy"], "frame-ancestors 'self'")
        self.assertEqual(b"".join(response.streaming_content), b"%PDF-1.4 controlled file")

        event = AuditEvent.objects.get()
        self.assert_document_access_event(
            event,
            user=self.reader,
            result=AuditResult.SUCCESS,
            description="Document viewer access granted.",
        )
        self.assertEqual(event.ip_address, "127.0.0.1")
        self.assertEqual(event.user_agent, "viewer-test")

    def test_oym_roles_can_view_any_document_file(self):
        for user in (self.oym_admin, self.oym_analyst):
            with self.subTest(user=user.email):
                AuditEvent.objects.all().delete()
                self.client.logout()
                self.client.force_login(user)

                response = self.client.get(
                    reverse(
                        "app:documents:file_view",
                        args=[
                            self.active_document.pk,
                            self.draft_version.pk,
                            self.draft_file.pk,
                        ],
                    )
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(AuditEvent.objects.get().result, AuditResult.SUCCESS)

    def test_systems_and_auditor_roles_get_403_and_denied_audit_event(self):
        for user in (self.systems_admin, self.auditor):
            with self.subTest(user=user.email):
                AuditEvent.objects.all().delete()
                self.client.logout()
                self.client.force_login(user)

                response = self.client.get(
                    reverse(
                        "app:documents:file_view",
                        args=[
                            self.active_document.pk,
                            self.active_version.pk,
                            self.active_file.pk,
                        ],
                    )
                )

                self.assertEqual(response.status_code, 403)

                event = AuditEvent.objects.get()
                self.assert_document_access_event(
                    event,
                    user=user,
                    result=AuditResult.DENIED,
                    description="Document viewer access denied.",
                )

    def test_executing_unit_can_view_document_owned_by_own_unit(self):
        self.client.force_login(self.executing_unit)

        response = self.client.get(
            reverse(
                "app:documents:file_view",
                args=[
                    self.active_document.pk,
                    self.active_version.pk,
                    self.active_file.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(AuditEvent.objects.get().result, AuditResult.SUCCESS)

    def test_executing_unit_without_unit_relation_gets_403(self):
        self.client.force_login(self.other_executing_unit)

        response = self.client.get(
            reverse(
                "app:documents:file_view",
                args=[
                    self.active_document.pk,
                    self.active_version.pk,
                    self.active_file.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(AuditEvent.objects.get().result, AuditResult.DENIED)

    def test_reader_with_direct_implementation_record_can_view_document_file(self):
        ImplementationRecord.objects.create(
            user=self.other_reader,
            document=self.active_document,
            document_version=self.active_version,
        )
        self.client.force_login(self.other_reader)

        response = self.client.get(
            reverse(
                "app:documents:file_view",
                args=[
                    self.active_document.pk,
                    self.active_version.pk,
                    self.active_file.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(AuditEvent.objects.get().result, AuditResult.SUCCESS)

    def test_reader_with_direct_controlled_copy_can_view_document_file(self):
        ControlledCopy.objects.create(
            document=self.active_document,
            document_version=self.active_version,
            copy_number="CC-002",
            receiver_unit=self.hr_unit,
            receiver_user=self.other_reader,
            status=ControlledCopyStatus.DELIVERED,
            created_by=self.oym_admin,
        )
        self.client.force_login(self.other_reader)

        response = self.client.get(
            reverse(
                "app:documents:file_view",
                args=[
                    self.active_document.pk,
                    self.active_version.pk,
                    self.active_file.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(AuditEvent.objects.get().result, AuditResult.SUCCESS)

    def test_reader_without_unit_or_direct_relation_gets_403(self):
        self.client.force_login(self.other_reader)

        response = self.client.get(
            reverse(
                "app:documents:file_view",
                args=[
                    self.active_document.pk,
                    self.active_version.pk,
                    self.active_file.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(AuditEvent.objects.get().result, AuditResult.DENIED)

    def test_reader_gets_403_for_non_visible_version_and_denied_audit_event(self):
        self.client.force_login(self.reader)

        response = self.client.get(
            reverse(
                "app:documents:file_view",
                args=[
                    self.active_document.pk,
                    self.draft_version.pk,
                    self.draft_file.pk,
                ],
            )
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(AuditEvent.objects.get().result, AuditResult.DENIED)

    def test_missing_controlled_file_returns_404_without_audit_event(self):
        self.client.force_login(self.reader)

        response = self.client.get(
            reverse(
                "app:documents:file_view",
                args=[
                    self.active_document.pk,
                    self.active_version.pk,
                    999999,
                ],
            )
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(AuditEvent.objects.count(), 0)

    def test_document_detail_does_not_expose_direct_media_url(self):
        self.client.force_login(self.reader)

        response = self.client.get(
            reverse("app:documents:detail", args=[self.active_document.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.active_file.original_filename)
        self.assertNotContains(response, self.active_file.file.url)
