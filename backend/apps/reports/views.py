from calendar import monthrange
from collections import Counter
from datetime import date

from django.utils import timezone
from django.views.generic import ListView

from apps.implementation_records.models import ImplementationRecordStatus
from config.access import ModuleAccessMixin, ModuleIndexView

from .forms import (
    ControlledCopiesReportFilterForm,
    ImplementationRecordsReportFilterForm,
    MasterBookFilterForm,
    MonthlyDocumentReportFilterForm,
)
from .permissions import can_view_reports
from .selectors import (
    get_controlled_copies_report_queryset,
    get_implementation_records_report_queryset,
    get_master_book_queryset,
    get_monthly_document_report_queryset,
)


class ReportAccessMixin(ModuleAccessMixin):
    permission_check = staticmethod(can_view_reports)


class ReportIndexView(ModuleIndexView):
    module_key = "reports"
    module_title = "Reportes"
    module_section = "Control"
    permission_check = staticmethod(can_view_reports)


class MasterBookView(ReportAccessMixin, ListView):
    template_name = "reports/master_book.html"
    context_object_name = "documents"

    def get_filter_form(self):
        return MasterBookFilterForm(self.request.GET or None)

    def get_queryset(self):
        self.filter_form = self.get_filter_form()
        if not self.filter_form.is_valid():
            return get_master_book_queryset()

        filters = {
            key: value
            for key, value in self.filter_form.cleaned_data.items()
            if value not in (None, "")
        }
        if "date_from" in filters or "date_to" in filters:
            filters["date_field"] = "created_at__date"
        return get_master_book_queryset(**filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = getattr(self, "filter_form", self.get_filter_form())
        return context


class MonthlyDocumentReportView(ReportAccessMixin, ListView):
    template_name = "reports/monthly_documents.html"
    context_object_name = "document_versions"

    def get_filter_data(self):
        today = timezone.localdate()
        data = self.request.GET.copy()
        data.setdefault("month", str(today.month))
        data.setdefault("year", str(today.year))
        return data

    def get_filter_form(self):
        return MonthlyDocumentReportFilterForm(self.get_filter_data())

    def get_queryset(self):
        self.filter_form = self.get_filter_form()
        today = timezone.localdate()
        month = today.month
        year = today.year
        filters = {}

        if self.filter_form.is_valid():
            cleaned_data = self.filter_form.cleaned_data
            month = cleaned_data["month"]
            year = cleaned_data["year"]
            filters = {
                key: value
                for key, value in cleaned_data.items()
                if key not in {"month", "year"} and value not in (None, "")
            }

        date_from, date_to = self.get_month_date_range(year=year, month=month)
        self.report_period = {
            "month": month,
            "year": year,
            "date_from": date_from,
            "date_to": date_to,
        }
        filters.update(
            {
                "date_field": "published_at__date",
                "date_from": date_from,
                "date_to": date_to,
            }
        )
        return get_monthly_document_report_queryset(**filters)

    def get_month_date_range(self, *, year, month):
        last_day = monthrange(year, month)[1]
        return date(year, month, 1), date(year, month, last_day)

    def get_summary(self, document_versions):
        return {
            "total": len(document_versions),
            "status_totals": sorted(
                Counter(
                    document_version.get_status_display()
                    for document_version in document_versions
                ).items()
            ),
            "document_type_totals": sorted(
                Counter(
                    str(document_version.document.document_type)
                    for document_version in document_versions
                ).items()
            ),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        document_versions = list(context["document_versions"])
        context["document_versions"] = document_versions
        context["filter_form"] = getattr(self, "filter_form", self.get_filter_form())
        context["report_period"] = self.report_period
        context["report_period_label"] = (
            f"{self.report_period['year']}-{self.report_period['month']:02d}"
        )
        context["report_summary"] = self.get_summary(document_versions)
        return context


class ControlledCopiesReportView(ReportAccessMixin, ListView):
    template_name = "reports/controlled_copies.html"
    context_object_name = "controlled_copies"

    def get_filter_form(self):
        return ControlledCopiesReportFilterForm(self.request.GET or None)

    def get_queryset(self):
        self.filter_form = self.get_filter_form()
        if not self.filter_form.is_valid():
            return get_controlled_copies_report_queryset()

        filters = {
            key: value
            for key, value in self.filter_form.cleaned_data.items()
            if value not in (None, "")
        }
        if "date_from" in filters or "date_to" in filters:
            filters["date_field"] = "delivered_at__date"
        return get_controlled_copies_report_queryset(**filters)

    def get_summary(self, controlled_copies):
        return {
            "total": len(controlled_copies),
            "status_totals": sorted(
                Counter(
                    controlled_copy.get_status_display()
                    for controlled_copy in controlled_copies
                ).items()
            ),
            "receiver_unit_totals": sorted(
                Counter(
                    controlled_copy.receiver_unit.name
                    for controlled_copy in controlled_copies
                ).items()
            ),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        controlled_copies = list(context["controlled_copies"])
        context["controlled_copies"] = controlled_copies
        context["filter_form"] = getattr(self, "filter_form", self.get_filter_form())
        context["report_summary"] = self.get_summary(controlled_copies)
        return context


class ImplementationRecordsReportView(ReportAccessMixin, ListView):
    template_name = "reports/implementation_records.html"
    context_object_name = "implementation_records"

    def get_filter_form(self):
        return ImplementationRecordsReportFilterForm(self.request.GET or None)

    def get_queryset(self):
        self.filter_form = self.get_filter_form()
        if not self.filter_form.is_valid():
            return get_implementation_records_report_queryset()

        filters = {
            key: value
            for key, value in self.filter_form.cleaned_data.items()
            if value not in (None, "")
        }
        if "date_from" in filters or "date_to" in filters:
            filters["date_field"] = "assigned_at__date"
        return get_implementation_records_report_queryset(**filters)

    def get_summary(self, implementation_records):
        implemented_count = sum(
            1
            for implementation_record in implementation_records
            if implementation_record.status == ImplementationRecordStatus.IMPLEMENTED
        )
        return {
            "total": len(implementation_records),
            "implemented": implemented_count,
            "not_implemented": len(implementation_records) - implemented_count,
            "status_totals": sorted(
                Counter(
                    implementation_record.get_status_display()
                    for implementation_record in implementation_records
                ).items()
            ),
            "user_unit_totals": sorted(
                Counter(
                    implementation_record.user.organizational_unit.name
                    if implementation_record.user.organizational_unit
                    else "Sin unidad"
                    for implementation_record in implementation_records
                ).items()
            ),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        implementation_records = list(context["implementation_records"])
        context["implementation_records"] = implementation_records
        context["filter_form"] = getattr(self, "filter_form", self.get_filter_form())
        context["report_summary"] = self.get_summary(implementation_records)
        return context
