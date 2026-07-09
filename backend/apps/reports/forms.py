from django import forms
from django.contrib.auth import get_user_model

from apps.controlled_copies.models import ControlledCopyStatus
from apps.document_types.models import DocumentType
from apps.documents.models import DocumentStatus
from apps.implementation_records.models import ImplementationRecordStatus
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


class MonthlyDocumentReportFilterForm(forms.Form):
    MONTH_CHOICES = tuple((month, f"{month:02d}") for month in range(1, 13))

    month = forms.TypedChoiceField(
        label="Mes",
        choices=MONTH_CHOICES,
        coerce=int,
    )
    year = forms.IntegerField(
        label="Ano",
        min_value=2000,
        max_value=2100,
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


class ControlledCopiesReportFilterForm(forms.Form):
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
    receiver_unit = forms.ModelChoiceField(
        label="Unidad destinataria",
        queryset=OrganizationalUnit.objects.all(),
        required=False,
        empty_label="Todas",
    )
    receiver_user = forms.ModelChoiceField(
        label="Usuario destinatario",
        queryset=get_user_model().objects.all(),
        required=False,
        empty_label="Todos",
    )
    status = forms.ChoiceField(
        label="Estado de copia",
        choices=(("", "Todos"), *ControlledCopyStatus.choices),
        required=False,
    )
    code = forms.CharField(
        label="Codigo documental",
        required=False,
        max_length=100,
    )
    date_from = forms.DateField(
        label="Entregada desde",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    date_to = forms.DateField(
        label="Entregada hasta",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )


class ImplementationRecordsReportFilterForm(forms.Form):
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
    user_organizational_unit = forms.ModelChoiceField(
        label="Unidad destinataria",
        queryset=OrganizationalUnit.objects.all(),
        required=False,
        empty_label="Todas",
    )
    user = forms.ModelChoiceField(
        label="Usuario destinatario",
        queryset=get_user_model().objects.all(),
        required=False,
        empty_label="Todos",
    )
    status = forms.ChoiceField(
        label="Estado de implementacion",
        choices=(("", "Todos"), *ImplementationRecordStatus.choices),
        required=False,
    )
    code = forms.CharField(
        label="Codigo documental",
        required=False,
        max_length=100,
    )
    date_from = forms.DateField(
        label="Asignado desde",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    date_to = forms.DateField(
        label="Asignado hasta",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    confirmation_date_from = forms.DateField(
        label="Confirmado desde",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    confirmation_date_to = forms.DateField(
        label="Confirmado hasta",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
