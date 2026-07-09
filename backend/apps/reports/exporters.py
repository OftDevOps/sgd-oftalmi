import csv
from datetime import date, datetime
from io import StringIO

from django.http import HttpResponse
from django.utils import timezone


MASTER_BOOK_CSV_HEADERS = [
    "Codigo documental",
    "Titulo",
    "Tipo documental",
    "Unidad responsable",
    "Estado",
    "Version",
    "Fecha creacion/emision",
    "Fecha vigencia",
    "Ultima actualizacion",
]

MONTHLY_DOCUMENTS_CSV_HEADERS = [
    "Codigo documental",
    "Titulo",
    "Tipo documental",
    "Unidad responsable",
    "Estado",
    "Version",
    "Fecha creacion/emision",
    "Ultima actualizacion",
    "Periodo reportado",
]

CONTROLLED_COPIES_CSV_HEADERS = [
    "Codigo documental",
    "Titulo",
    "Tipo documental",
    "Unidad responsable",
    "Version",
    "Destinatario",
    "Unidad destinataria",
    "Estado copia",
    "Fecha entrega/asignacion",
    "Fecha cierre/devolucion",
    "Ultima actualizacion",
]

IMPLEMENTATION_RECORDS_CSV_HEADERS = [
    "Codigo documental",
    "Titulo",
    "Tipo documental",
    "Unidad responsable",
    "Version",
    "Unidad destinataria/ejecutora",
    "Usuario",
    "Estado implementacion/lectura",
    "Fecha asignacion",
    "Fecha implementacion/confirmacion",
    "Ultima actualizacion",
]


def build_csv_response(*, filename, headers, rows):
    buffer = StringIO()
    buffer.write("\ufeff")
    writer = csv.writer(buffer)
    writer.writerow(headers)
    writer.writerows(serialize_csv_rows(rows))

    response = HttpResponse(buffer.getvalue(), content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    response["X-Content-Type-Options"] = "nosniff"
    return response


def format_csv_value(value):
    if value is None:
        return ""
    if isinstance(value, datetime):
        if timezone.is_aware(value):
            value = timezone.localtime(value)
        return value.strftime("%Y-%m-%d %H:%M")
    if isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    return str(value)


def master_book_csv_rows(documents):
    for document in documents:
        current_version = document.current_version
        yield [
            document.code,
            document.title,
            document.document_type,
            document.owner_unit.name,
            document.get_status_display(),
            current_version.version_number if current_version else "",
            (
                current_version.issue_date
                if current_version and current_version.issue_date
                else document.created_at
            ),
            current_version.effective_date if current_version else None,
            document.updated_at,
        ]


def monthly_documents_csv_rows(document_versions, *, period_label):
    for document_version in document_versions:
        document = document_version.document
        yield [
            document.code,
            document.title,
            document.document_type,
            document.owner_unit.name,
            document_version.get_status_display(),
            document_version.version_number,
            document_version.issue_date or document_version.created_at,
            document.updated_at,
            period_label,
        ]


def controlled_copies_csv_rows(controlled_copies):
    for controlled_copy in controlled_copies:
        document = controlled_copy.document
        receiver_user = controlled_copy.receiver_user
        yield [
            document.code,
            document.title,
            document.document_type,
            document.owner_unit.name,
            controlled_copy.document_version.version_number,
            receiver_user.email if receiver_user else "",
            controlled_copy.receiver_unit.name,
            controlled_copy.get_status_display(),
            controlled_copy.delivered_at or controlled_copy.created_at,
            controlled_copy.retired_at,
            controlled_copy.updated_at,
        ]


def implementation_records_csv_rows(implementation_records):
    for implementation_record in implementation_records:
        document = implementation_record.document
        user = implementation_record.user
        yield [
            document.code,
            document.title,
            document.document_type,
            document.owner_unit.name,
            implementation_record.document_version.version_number,
            user.organizational_unit.name if user.organizational_unit else "",
            user.email,
            implementation_record.get_status_display(),
            implementation_record.assigned_at,
            _implementation_confirmation_date(implementation_record),
            implementation_record.updated_at,
        ]


def serialize_csv_rows(rows):
    return [[format_csv_value(value) for value in row] for row in rows]


def _implementation_confirmation_date(implementation_record):
    return (
        implementation_record.implemented_at
        or implementation_record.accepted_at
        or implementation_record.interpreted_at
        or implementation_record.read_at
    )
