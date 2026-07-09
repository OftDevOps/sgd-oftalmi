from calendar import monthrange
from collections import Counter
from datetime import date

from django.utils import timezone
from django.views.generic import ListView

from config.access import ModuleAccessMixin, ModuleIndexView

from .forms import MasterBookFilterForm, MonthlyDocumentReportFilterForm
from .permissions import can_view_reports
from .selectors import get_master_book_queryset, get_monthly_document_report_queryset


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
