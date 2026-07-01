from django import forms

from apps.documents.selectors import document_list, document_version_list

from .models import ImplementationRecord
from .selectors import implementation_record_list
from .services import implementation_record_create


class ImplementationRecordCreateForm(forms.ModelForm):
    class Meta:
        model = ImplementationRecord
        fields = (
            "document",
            "document_version",
        )
        labels = {
            "document": "Documento",
            "document_version": "Version documental",
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["document"].queryset = document_list(is_active=True)
        self.fields["document_version"].queryset = document_version_list()

    def clean(self):
        cleaned_data = super().clean()
        document = cleaned_data.get("document")
        document_version = cleaned_data.get("document_version")

        if document and document_version and document_version.document_id != document.id:
            self.add_error(
                "document_version",
                "La version documental debe pertenecer al documento seleccionado.",
            )

        if (
            self.user
            and document_version
            and implementation_record_list(
                user=self.user,
                document_version=document_version,
            ).exists()
        ):
            self.add_error(
                "document_version",
                "Ya existe un registro de implementacion propio para esta version.",
            )

        return cleaned_data

    def save(self, commit=True):
        if not commit:
            return super().save(commit=False)

        return implementation_record_create(
            user=self.user,
            document=self.cleaned_data["document"],
            document_version=self.cleaned_data["document_version"],
        )
