from django import forms

from apps.document_types.models import DocumentType
from apps.documents.models import DocumentStatus
from apps.organizational_units.models import OrganizationalUnit


class MasterBookFilterForm(forms.Form):
    VIGENCY_CHOICES = (
        ("", "Todas"),
        ("current", "Vigentes actuales"),
        ("expired", "Vencidos"),
        ("obsolete", "Obsoletos"),
        ("archived", "Archivados"),
    )

    document_type = forms.ModelChoiceField(
        label="Tipo documental",
        queryset=DocumentType.objects.all(),
        required=False,
        empty_label="Todos",
    )
    organizational_unit = forms.ModelChoiceField(
        label="Unidad responsable",
        queryset=OrganizationalUnit.objects.all(),
        required=False,
        empty_label="Todas",
    )
    status = forms.ChoiceField(
        label="Estado documental",
        choices=(("", "Todos"), *DocumentStatus.choices),
        required=False,
    )
    vigency = forms.ChoiceField(
        label="Vigencia",
        choices=VIGENCY_CHOICES,
        required=False,
    )
    code = forms.CharField(
        label="Codigo documental",
        required=False,
        max_length=100,
    )
    title = forms.CharField(
        label="Titulo",
        required=False,
        max_length=255,
    )
    date_from = forms.DateField(
        label="Creado desde",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    date_to = forms.DateField(
        label="Creado hasta",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
