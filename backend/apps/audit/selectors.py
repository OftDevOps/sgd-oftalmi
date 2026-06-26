from .models import AuditEvent


def audit_event_list(
    *,
    user=None,
    action=None,
    module=None,
    result=None,
    entity_type=None,
    entity_id=None,
):
    queryset = AuditEvent.objects.select_related("user")

    if user is not None:
        queryset = queryset.filter(user=user)
    if action is not None:
        queryset = queryset.filter(action=action)
    if module is not None:
        queryset = queryset.filter(module=module)
    if result is not None:
        queryset = queryset.filter(result=result)
    if entity_type is not None:
        queryset = queryset.filter(entity_type=entity_type)
    if entity_id is not None:
        queryset = queryset.filter(entity_id=entity_id)

    return queryset
