from dataclasses import dataclass

from .models import AuditEvent, AuditResult


@dataclass(frozen=True)
class AuditContext:
    user: object = None
    ip_address: str | None = None
    user_agent: str = ""


def audit_event_create(
    *,
    action,
    module,
    result,
    user=None,
    entity_type="",
    entity_id="",
    ip_address=None,
    user_agent="",
    description="",
    before_data=None,
    after_data=None,
):
    audit_event = AuditEvent(
        user=user,
        action=action,
        module=module,
        entity_type=entity_type,
        entity_id=entity_id,
        result=result,
        ip_address=ip_address,
        user_agent=user_agent,
        description=description,
        before_data=before_data,
        after_data=after_data,
    )
    audit_event.full_clean()
    audit_event.save()
    return audit_event


def audit_event_create_for_instance(
    *,
    action,
    module,
    instance,
    result=AuditResult.SUCCESS,
    audit_context=None,
    user=None,
    ip_address=None,
    user_agent="",
    description="",
    before_data=None,
    after_data=None,
):
    if audit_context is not None:
        user = audit_context.user
        ip_address = audit_context.ip_address
        user_agent = audit_context.user_agent

    return audit_event_create(
        user=user,
        action=action,
        module=module,
        entity_type=instance.__class__.__name__,
        entity_id=str(instance.pk),
        result=result,
        ip_address=ip_address,
        user_agent=user_agent,
        description=description,
        before_data=before_data,
        after_data=after_data,
    )


def audit_event_create_if_requested(*, audit_context=None, **kwargs):
    if audit_context is None:
        return None

    return audit_event_create_for_instance(audit_context=audit_context, **kwargs)
