from django import forms

from apps.document_types.selectors import document_type_list
from apps.documents.selectors import document_list
from apps.organizational_units.selectors import organizational_unit_list

from .models import DocumentRequest, DocumentRequestType
from .services import document_request_create


class DocumentRequestCreateForm(forms.ModelForm):
    class Meta:
        model = DocumentRequest
        fields = (
            "request_type",
            "title",
            "description",
            "organizational_unit",
            "document_type",
            "related_document",
        )
        labels = {
            "request_type": "Tipo de solicitud",
            "title": "Titulo",
            "description": "Descripcion",
            "organizational_unit": "Unidad ejecutora",
            "document_type": "Tipo documental",
            "related_document": "Documento relacionado",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["request_type"].choices = DocumentRequestType.choices
        self.fields["organizational_unit"].queryset = organizational_unit_list(is_active=True)
        self.fields["document_type"].queryset = document_type_list(is_active=True)
        self.fields["related_document"].queryset = document_list(is_active=True)
        self.fields["document_type"].required = False
        self.fields["related_document"].required = False

        if user and user.organizational_unit_id:
            self.fields["organizational_unit"].initial = user.organizational_unit

    def save(self, commit=True):
        if not commit:
            return super().save(commit=False)

        return document_request_create(
            request_type=self.cleaned_data["request_type"],
            title=self.cleaned_data["title"],
            description=self.cleaned_data.get("description", ""),
            requested_by=self.user,
            organizational_unit=self.cleaned_data["organizational_unit"],
            document_type=self.cleaned_data.get("document_type"),
            related_document=self.cleaned_data.get("related_document"),
        )
