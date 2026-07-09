from apps.audit.models import AuditAction, AuditResult
from apps.audit.services import AuditContext, audit_event_create


REPORT_VIEWED = "REPORT_VIEWED"
REPORT_EXPORTED = "REPORT_EXPORTED"
REPORT_MODULE = "reports"
REPORT_ENTITY_TYPE = "Report"

MASTER_BOOK_REPORT = "master_book"
MONTHLY_DOCUMENTS_REPORT = "monthly_documents"
CONTROLLED_COPIES_REPORT = "controlled_copies"
IMPLEMENTATION_RECORDS_REPORT = "implementation_records"

REPORT_NAMES = {
    MASTER_BOOK_REPORT: "Libro Maestro documental",
    MONTHLY_DOCUMENTS_REPORT: "Reporte mensual documental",
    CONTROLLED_COPIES_REPORT: "Reporte de copias controladas",
    IMPLEMENTATION_RECORDS_REPORT: "Reporte de implementacion y lectura",
}


def report_audit_event_create(
    *,
    audit_context,
    report_code,
    report_event,
    result=AuditResult.SUCCESS,
    filters=None,
    output_format="html",
):
    if audit_context is None:
        return None

    report_name = REPORT_NAMES.get(report_code, report_code)
    return audit_event_create(
        user=audit_context.user,
        action=AuditAction.REPORT_GENERATED,
        module=REPORT_MODULE,
        entity_type=REPORT_ENTITY_TYPE,
        entity_id=report_code,
        result=result,
        ip_address=audit_context.ip_address,
        user_agent=audit_context.user_agent,
        description=_report_audit_description(
            report_name=report_name,
            report_event=report_event,
            result=result,
        ),
        after_data={
            "report_code": report_code,
            "report_name": report_name,
            "report_event": report_event,
            "filters": filters or {},
            "format": output_format,
        },
    )


def request_audit_context(request):
    return AuditContext(
        user=request.user,
        ip_address=_request_ip_address(request),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
    )


def request_filter_metadata(request):
    return {
        key: values if len(values) > 1 else values[0]
        for key, values in request.GET.lists()
    }


def _request_ip_address(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",", 1)[0].strip() or None
    return request.META.get("REMOTE_ADDR") or None


def _report_audit_description(*, report_name, report_event, result):
    if report_event == REPORT_EXPORTED:
        action_label = "exported"
    elif report_event == REPORT_VIEWED:
        action_label = "viewed"
    else:
        action_label = "processed"

    return f"Report {action_label}: {report_name}. Result: {result}."
