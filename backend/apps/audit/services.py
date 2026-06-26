from .models import AuditEvent


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
