import datetime

from NEMO.models import AccountType, ConsumableWithdraw, User
from NEMO.typing import QuerySetType
from NEMO.utilities import beginning_of_the_day, end_of_the_day
from django.db.models.functions import Coalesce, Least

try:
    from NEMO.models import Discipline as ProjectDiscipline
except:
    from NEMO.models import ProjectDiscipline

from NEMO.models import (
    AreaAccessRecord,
    Reservation,
    StaffCharge,
    TrainingSession,
    UsageEvent,
)
from django.db.models import Case, CharField, DateTimeField, F, OuterRef, Subquery, Value, When
from django.shortcuts import render
from django.views.decorators.http import require_GET

from NEMO.decorators import accounting_or_manager_required
from NEMO_reports.views.reporting import (
    ACTIVITIES_PARAMETER_LIST,
    DEFAULT_PARAMETER_LIST,
    DataDisplayTable,
    ReportingParameters,
    SummaryDisplayTable,
    billing_installed,
    get_core_facility,
    get_institution,
    get_institution_type,
    get_month_range,
    get_monthly_rule,
    get_rate_category,
    report_export,
    reporting_dictionary,
)


@accounting_or_manager_required
@require_GET
def new_users(request):
    param_names = DEFAULT_PARAMETER_LIST + ACTIVITIES_PARAMETER_LIST + ["during_date_range"]
    params = ReportingParameters(request, param_names)
    start, end = params.start, params.end
    split_by_month = params.get_bool("split_by_month")
    cumulative_count = params.get_bool("cumulative_count")
    monthly_start = None
    if cumulative_count:
        split_by_month = True
        monthly_start, monthly_end = get_month_range(start)

    RateCategory = get_rate_category()
    CoreFacility = get_core_facility()
    InstitutionType = get_institution_type()
    Institution = get_institution()

    data = DataDisplayTable()
    if params.get_bool("detailed_data"):
        data.headers = [
            ("first", "First name"),
            ("last", "Last name"),
            ("username", "Username"),
            ("first_activity", "First activity"),
            ("project", "Project"),
        ]

        if billing_installed():
            if CoreFacility and CoreFacility.objects.exists():
                data.add_header(("core_facility", "Core Facility"))
            if RateCategory and RateCategory.objects.exists():
                data.add_header(("rate_category", "Rate category"))
            if Institution and Institution.objects.exists():
                data.add_header(("institution_name", "Institution Name"))
                data.add_header(("institution_type", "Institution Type"))
        if ProjectDiscipline.objects.exists():
            data.add_header(("discipline", "Discipline"))
        if AccountType.objects.exists():
            data.add_header(("account_type", "Account type"))

        new_users = get_first_activities_and_data(params, start, end)
        for user in new_users:
            data_row = {
                "first": user.first_name,
                "last": user.last_name,
                "username": user.username,
                "first_activity": getattr(user, "first_activity", None),
                "project": getattr(user, "first_activity_project", None),
                "discipline": getattr(user, "first_activity_discipline", None),
                "account_type": getattr(user, "first_activity_account_type", None),
            }
            if billing_installed():
                data_row["institution_name"] = getattr(user, "first_activity_institution_name", None)
                data_row["institution_type"] = getattr(user, "first_activity_institution_type", None)
                data_row["rate_category"] = getattr(user, "first_activity_rate_category", None)
                data_row["core_facility"] = getattr(user, "first_activity_core_facility", None)

            data.add_row(data_row)
        data.rows.sort(key=lambda x: x["first_activity"])

    summary = SummaryDisplayTable()
    summary.add_header(("item", "Item"))
    summary.add_row({"item": "New users"})
    if CoreFacility and CoreFacility.objects.exists():
        summary.add_row({"item": "By core facility"})
        for facility in CoreFacility.objects.all():
            summary.add_row({"item": f"{facility.name}"})
        summary.add_row({"item": "N/A"})
    if ProjectDiscipline.objects.exists():
        summary.add_row({"item": "By project discipline"})
        for discipline in ProjectDiscipline.objects.all():
            summary.add_row({"item": f"{discipline.name}"})
        summary.add_row({"item": "N/A"})
    if AccountType.objects.exists():
        summary.add_row({"item": "By account type"})
        for account_type in AccountType.objects.all():
            summary.add_row({"item": f"{account_type.name}"})
        summary.add_row({"item": "N/A"})
    if RateCategory and RateCategory.objects.exists():
        summary.add_row({"item": "By project rate category"})
        for category in RateCategory.objects.all():
            summary.add_row({"item": f"{category.name}"})
        summary.add_row({"item": "N/A"})
    if Institution and Institution.objects.exists():
        summary.add_row({"item": "By institution"})
        for institution in Institution.objects.all():
            summary.add_row({"item": f"{institution.name}"})
        summary.add_row({"item": "N/A"})
    if InstitutionType and InstitutionType.objects.exists():
        summary.add_row({"item": "By institution type"})
        for institution_type in InstitutionType.objects.all():
            summary.add_row({"item": f"{institution_type.name}"})
        summary.add_row({"item": "N/A"})

    if split_by_month:
        for month in get_monthly_rule(start, end):
            month_key = f"month_{month.strftime('%Y')}_{month.strftime('%m')}"
            summary.add_header((month_key, month.strftime("%b %Y")))
            month_start, month_end = get_month_range(month)
            add_summary_info(params, summary, monthly_start or month_start, month_end, month_key)
    else:
        summary.add_header(("value", "Value"))
        add_summary_info(params, summary, start, end)

    if params.get_bool("export"):
        return report_export([summary, data], "active_users", start, end)
    dictionary = {
        "data": data,
        "summary": summary,
    }
    return render(
        request,
        "NEMO_reports/report_new_users.html",
        reporting_dictionary("new_users", params, dictionary),
    )


def add_summary_info(
    parameters: ReportingParameters,
    summary: SummaryDisplayTable,
    start,
    end,
    summary_key=None,
):

    RateCategory = get_rate_category()
    CoreFacility = get_core_facility()
    InstitutionType = get_institution_type()
    Institution = get_institution()

    summary_key = summary_key or "value"
    users = get_first_activities_and_data(parameters, start, end)
    summary.rows[0][summary_key] = users.count()
    current_row = 1

    if CoreFacility and CoreFacility.objects.exists():
        for facility in CoreFacility.objects.all():
            current_row += 1
            summary.rows[current_row][summary_key] = len(users.filter(first_activity_core_facility=facility.name))
        current_row += 1
        summary.rows[current_row][summary_key] = len(users.filter(first_activity_core_facility__isnull=True))
        current_row += 1  # For mid table header
    if ProjectDiscipline.objects.exists():
        for discipline in ProjectDiscipline.objects.all():
            current_row += 1
            summary.rows[current_row][summary_key] = len(users.filter(first_activity_discipline=discipline.name))
        current_row += 1
        summary.rows[current_row][summary_key] = len(users.filter(first_activity_discipline__isnull=True))
        current_row += 1  # For mid table header
    if AccountType.objects.exists():
        for account_type in AccountType.objects.all():
            current_row += 1
            summary.rows[current_row][summary_key] = len(users.filter(first_activity_account_type=account_type.name))
        current_row += 1
        summary.rows[current_row][summary_key] = len(users.filter(first_activity_account_type__isnull=True))
        current_row += 1  # For mid table header
    if RateCategory and RateCategory.objects.exists():
        for category in RateCategory.objects.all():
            current_row += 1
            summary.rows[current_row][summary_key] = len(users.filter(first_activity_rate_category=category.name))
        current_row += 1
        summary.rows[current_row][summary_key] = len(users.filter(first_activity_rate_category__isnull=True))
        current_row += 1  # For mid table header
    if Institution and Institution.objects.exists():
        for institution in Institution.objects.all():
            current_row += 1
            summary.rows[current_row][summary_key] = len(users.filter(first_activity_institution_name=institution.name))
        current_row += 1
        summary.rows[current_row][summary_key] = len(users.filter(first_activity_institution_name__isnull=True))
        current_row += 1  # For mid table header
    if InstitutionType and InstitutionType.objects.exists():
        for institution_type in InstitutionType.objects.all():
            current_row += 1
            summary.rows[current_row][summary_key] = len(
                users.filter(first_activity_institution_type=institution_type.name)
            )
        current_row += 1
        summary.rows[current_row][summary_key] = len(users.filter(first_activity_institution_type__isnull=True))
        current_row += 1  # For mid table header
    current_row += 1


def get_first_activities_and_data(
    params: ReportingParameters,
    start: datetime.datetime,
    end: datetime.datetime,
) -> QuerySetType[User]:
    origin_start = params.start
    users = User.objects.all()
    during_date_range = params.get_bool("during_date_range")
    origin_start_datetime = beginning_of_the_day(datetime.datetime.combine(origin_start, datetime.time()))
    start_datetime = beginning_of_the_day(datetime.datetime.combine(start, datetime.time()))
    end_datetime = end_of_the_day(datetime.datetime.combine(end, datetime.time()))
    max_date = datetime.datetime.max - datetime.timedelta(days=1)
    max_date = max_date.astimezone()
    base_empty_annotations = {}
    for first_type in [
        "first_tool_usage",
        "first_area_access",
        "first_staff_charge",
        "first_training",
        "first_missed_reservation",
        "first_consumable_withdrawal",
        "first_custom_charge",
    ]:
        base_empty_annotations[first_type] = Value(max_date, output_field=DateTimeField())
        for first_type_property in [
            "_project",
            "_discipline",
            "_account_type",
            "_core_facility",
            "_rate_category",
            "_institution_name",
            "_institution_type",
        ]:
            base_empty_annotations[first_type + first_type_property] = Value(None, output_field=CharField())
    users = users.annotate(**base_empty_annotations)
    if params.get_bool("tool_usage", "on"):
        first_usage_sub = UsageEvent.objects.filter(user=OuterRef("pk"))
        if during_date_range:
            first_usage_sub = first_usage_sub.filter(start__gte=origin_start_datetime)
        first_usage_sub = first_usage_sub.order_by("start")
        users = users.annotate(
            first_tool_usage=Coalesce(Subquery(first_usage_sub.values("start")[:1]), Value(max_date)),
            first_tool_usage_project=Subquery(first_usage_sub.values("project__name")[:1]),
            first_tool_usage_discipline=Subquery(first_usage_sub.values("project__discipline__name")[:1]),
            first_tool_usage_account_type=Subquery(first_usage_sub.values("project__account__type__name")[:1]),
        )
        if billing_installed():
            users = users.annotate(
                first_tool_usage_core_facility=Subquery(
                    first_usage_sub.values("tool__core_rel__core_facility__name")[:1]
                ),
                first_tool_usage_rate_category=Subquery(
                    first_usage_sub.values("project__projectbillingdetails__category__name")[:1]
                ),
                first_tool_usage_institution_name=Subquery(
                    first_usage_sub.values("project__projectbillingdetails__institution__name")[:1]
                ),
                first_tool_usage_institution_type=Subquery(
                    first_usage_sub.values("project__projectbillingdetails__institution__institution_type__name")[:1]
                ),
            )
    if params.get_bool("area_access", "on"):
        first_access_sub = AreaAccessRecord.objects.filter(customer=OuterRef("pk"))
        if during_date_range:
            first_access_sub = first_access_sub.filter(start__gte=origin_start_datetime)
        first_access_sub = first_access_sub.order_by("start")
        users = users.annotate(
            first_area_access=Coalesce(Subquery(first_access_sub.values("start")[:1]), Value(max_date)),
            first_area_access_project=Subquery(first_access_sub.values("project__name")[:1]),
            first_area_access_discipline=Subquery(first_access_sub.values("project__discipline__name")[:1]),
            first_area_access_account_type=Subquery(first_access_sub.values("project__account__type__name")[:1]),
        )
        if billing_installed():
            users = users.annotate(
                first_area_access_core_facility=Subquery(
                    first_access_sub.values("area__core_rel__core_facility__name")[:1]
                ),
                first_area_access_rate_category=Subquery(
                    first_access_sub.values("project__projectbillingdetails__category__name")[:1]
                ),
                first_area_access_institution_name=Subquery(
                    first_access_sub.values("project__projectbillingdetails__institution__name")[:1]
                ),
                first_area_access_institution_type=Subquery(
                    first_access_sub.values("project__projectbillingdetails__institution__institution_type__name")[:1]
                ),
            )
    if params.get_bool("staff_charges", "on"):
        first_staff_charge_sub = StaffCharge.objects.filter(customer=OuterRef("pk"))
        if during_date_range:
            first_staff_charge_sub = first_staff_charge_sub.filter(start__gte=origin_start_datetime)
        first_staff_charge_sub = first_staff_charge_sub.order_by("start")
        users = users.annotate(
            first_staff_charge=Coalesce(Subquery(first_staff_charge_sub.values("start")[:1]), Value(max_date)),
            first_staff_charge_project=Subquery(first_staff_charge_sub.values("project__name")[:1]),
            first_staff_charge_discipline=Subquery(first_staff_charge_sub.values("project__discipline__name")[:1]),
            first_staff_charge_account_type=Subquery(first_staff_charge_sub.values("project__account__type__name")[:1]),
        )
        if billing_installed():
            users = users.annotate(
                first_staff_charge_core_facility=Subquery(
                    first_staff_charge_sub.values("core_rel__core_facility__name")[:1]
                ),
                first_staff_charge_rate_category=Subquery(
                    first_staff_charge_sub.values("project__projectbillingdetails__category__name")[:1]
                ),
                first_staff_charge_institution_name=Subquery(
                    first_staff_charge_sub.values("project__projectbillingdetails__institution__name")[:1]
                ),
                first_staff_charge_institution_type=Subquery(
                    first_staff_charge_sub.values(
                        "project__projectbillingdetails__institution__institution_type__name"
                    )[:1]
                ),
            )
    if params.get_bool("training", "on"):
        first_training_sub = TrainingSession.objects.filter(trainee=OuterRef("pk"))
        if during_date_range:
            first_training_sub = first_training_sub.filter(date__gte=origin_start_datetime)
        first_training_sub = first_training_sub.order_by("date")
        users = users.annotate(
            first_training=Coalesce(Subquery(first_training_sub.values("date")[:1]), Value(max_date)),
            first_training_project=Subquery(first_training_sub.values("project__name")[:1]),
            first_training_discipline=Subquery(first_training_sub.values("project__discipline__name")[:1]),
            first_training_account_type=Subquery(first_training_sub.values("project__account__type__name")[:1]),
        )
        if billing_installed():
            users = users.annotate(
                first_training_core_facility=Subquery(
                    first_training_sub.values("tool__core_rel__core_facility__name")[:1]
                ),
                first_training_rate_category=Subquery(
                    first_training_sub.values("project__projectbillingdetails__category__name")[:1]
                ),
                first_training_institution_name=Subquery(
                    first_training_sub.values("project__projectbillingdetails__institution__name")[:1]
                ),
                first_training_institution_type=Subquery(
                    first_training_sub.values("project__projectbillingdetails__institution__institution_type__name")[:1]
                ),
            )
    if params.get_bool("missed_reservations", "on"):
        first_missed_sub = Reservation.objects.filter(missed=True, user=OuterRef("pk"))
        if during_date_range:
            first_missed_sub = first_missed_sub.filter(start__gte=origin_start_datetime)
        first_missed_sub = first_missed_sub.order_by("start")
        users = users.annotate(
            first_missed_reservation=Coalesce(
                Subquery(first_missed_sub.order_by("start").values("start")[:1]), Value(max_date)
            ),
            first_missed_reservation_project=Subquery(first_missed_sub.values("project__name")[:1]),
            first_missed_reservation_discipline=Subquery(first_missed_sub.values("project__discipline__name")[:1]),
            first_missed_reservation_account_type=Subquery(first_missed_sub.values("project__account__type__name")[:1]),
        )
        if billing_installed():
            users = users.annotate(
                first_missed_reservation_rate_category=Subquery(
                    first_missed_sub.values("project__projectbillingdetails__category__name")[:1]
                ),
                first_missed_reservation_institution_name=Subquery(
                    first_missed_sub.values("project__projectbillingdetails__institution__name")[:1]
                ),
                first_missed_reservation_institution_type=Subquery(
                    first_missed_sub.values("project__projectbillingdetails__institution__institution_type__name")[:1]
                ),
            )
    if params.get_bool("consumables", "on"):
        first_consumable_sub = ConsumableWithdraw.objects.filter(customer=OuterRef("pk"))
        if during_date_range:
            first_consumable_sub = first_consumable_sub.filter(date__gte=origin_start_datetime)
        first_consumable_sub = first_consumable_sub.order_by("date")
        users = users.annotate(
            first_consumable_withdrawal=Coalesce(Subquery(first_consumable_sub.values("date")[:1]), Value(max_date)),
            first_consumable_withdrawal_project=Subquery(first_consumable_sub.values("project__name")[:1]),
            first_consumable_withdrawal_discipline=Subquery(
                first_consumable_sub.values("project__discipline__name")[:1]
            ),
            first_consumable_withdrawal_account_type=Subquery(
                first_consumable_sub.values("project__account__type__name")[:1]
            ),
        )
        if billing_installed():
            users = users.annotate(
                first_consumable_withdrawal_core_facility=Subquery(
                    first_consumable_sub.values("consumable__core_rel__core_facility__name")[:1]
                ),
                first_consumable_withdrawal_rate_category=Subquery(
                    first_consumable_sub.values("project__projectbillingdetails__category__name")[:1]
                ),
                first_consumable_withdrawal_institution_name=Subquery(
                    first_consumable_sub.values("project__projectbillingdetails__institution__name")[:1]
                ),
                first_consumable_withdrawal_institution_type=Subquery(
                    first_consumable_sub.values("project__projectbillingdetails__institution__institution_type__name")[
                        :1
                    ]
                ),
            )
    if billing_installed():
        from NEMO_billing.models import CustomCharge

        if params.get_bool("custom_charges", "on"):
            first_custom_sub = CustomCharge.objects.filter(customer=OuterRef("pk"))
            if during_date_range:
                first_custom_sub = first_custom_sub.filter(date__gte=origin_start_datetime)
            first_custom_sub = first_custom_sub.order_by("date")
            users = users.annotate(
                first_custom_charge=Coalesce(Subquery(first_custom_sub.values("date")[:1]), Value(max_date)),
                first_custom_charge_project=Subquery(first_custom_sub.values("project__name")[:1]),
                first_custom_charge_discipline=Subquery(first_custom_sub.values("project__discipline__name")[:1]),
                first_custom_charge_account_type=Subquery(first_custom_sub.values("project__account__type__name")[:1]),
            )
            if billing_installed():
                users = users.annotate(
                    first_custom_charge_core_facility=Subquery(first_custom_sub.values("core_facility__name")[:1]),
                    first_custom_charge_rate_category=Subquery(
                        first_custom_sub.values("project__projectbillingdetails__category__name")[:1]
                    ),
                    first_custom_charge_institution_name=Subquery(
                        first_custom_sub.values("project__projectbillingdetails__institution__name")[:1]
                    ),
                    first_custom_charge_institution_type=Subquery(
                        first_custom_sub.values("project__projectbillingdetails__institution__institution_type__name")[
                            :1
                        ]
                    ),
                )
    users = users.annotate(
        first_activity=Least(
            "first_tool_usage",
            "first_area_access",
            "first_staff_charge",
            "first_training",
            "first_missed_reservation",
            "first_consumable_withdrawal",
            "first_custom_charge",
        ),
        first_activity_project=Case(
            When(first_activity=F("first_tool_usage"), then=F("first_tool_usage_project")),
            When(first_activity=F("first_area_access"), then=F("first_area_access_project")),
            When(first_activity=F("first_staff_charge"), then=F("first_staff_charge_project")),
            When(first_activity=F("first_training"), then=F("first_training_project")),
            When(first_activity=F("first_missed_reservation"), then=F("first_missed_reservation_project")),
            When(first_activity=F("first_consumable_withdrawal"), then=F("first_consumable_withdrawal_project")),
            When(first_activity=F("first_custom_charge"), then=F("first_custom_charge_project")),
        ),
        first_activity_discipline=Case(
            When(first_activity=F("first_tool_usage"), then=F("first_tool_usage_discipline")),
            When(first_activity=F("first_area_access"), then=F("first_area_access_discipline")),
            When(first_activity=F("first_staff_charge"), then=F("first_staff_charge_discipline")),
            When(first_activity=F("first_training"), then=F("first_training_discipline")),
            When(first_activity=F("first_missed_reservation"), then=F("first_missed_reservation_discipline")),
            When(first_activity=F("first_consumable_withdrawal"), then=F("first_consumable_withdrawal_discipline")),
            When(first_activity=F("first_custom_charge"), then=F("first_custom_charge_discipline")),
        ),
        first_activity_account_type=Case(
            When(first_activity=F("first_tool_usage"), then=F("first_tool_usage_account_type")),
            When(first_activity=F("first_area_access"), then=F("first_area_access_account_type")),
            When(first_activity=F("first_staff_charge"), then=F("first_staff_charge_account_type")),
            When(first_activity=F("first_training"), then=F("first_training_account_type")),
            When(first_activity=F("first_missed_reservation"), then=F("first_missed_reservation_account_type")),
            When(first_activity=F("first_consumable_withdrawal"), then=F("first_consumable_withdrawal_account_type")),
            When(first_activity=F("first_custom_charge"), then=F("first_custom_charge_account_type")),
        ),
        first_activity_core_facility=Case(
            When(first_activity=F("first_tool_usage"), then=F("first_tool_usage_core_facility")),
            When(first_activity=F("first_area_access"), then=F("first_area_access_core_facility")),
            When(first_activity=F("first_staff_charge"), then=F("first_staff_charge_core_facility")),
            When(first_activity=F("first_training"), then=F("first_training_core_facility")),
            When(first_activity=F("first_missed_reservation"), then=F("first_missed_reservation_core_facility")),
            When(first_activity=F("first_consumable_withdrawal"), then=F("first_consumable_withdrawal_core_facility")),
            When(first_activity=F("first_custom_charge"), then=F("first_custom_charge_core_facility")),
        ),
        first_activity_rate_category=Case(
            When(first_activity=F("first_tool_usage"), then=F("first_tool_usage_rate_category")),
            When(first_activity=F("first_area_access"), then=F("first_area_access_rate_category")),
            When(first_activity=F("first_staff_charge"), then=F("first_staff_charge_rate_category")),
            When(first_activity=F("first_training"), then=F("first_training_rate_category")),
            When(first_activity=F("first_missed_reservation"), then=F("first_missed_reservation_rate_category")),
            When(first_activity=F("first_consumable_withdrawal"), then=F("first_consumable_withdrawal_rate_category")),
            When(first_activity=F("first_custom_charge"), then=F("first_custom_charge_rate_category")),
        ),
        first_activity_institution_name=Case(
            When(first_activity=F("first_tool_usage"), then=F("first_tool_usage_institution_name")),
            When(first_activity=F("first_area_access"), then=F("first_area_access_institution_name")),
            When(first_activity=F("first_staff_charge"), then=F("first_staff_charge_institution_name")),
            When(first_activity=F("first_training"), then=F("first_training_institution_name")),
            When(first_activity=F("first_missed_reservation"), then=F("first_missed_reservation_institution_name")),
            When(
                first_activity=F("first_consumable_withdrawal"), then=F("first_consumable_withdrawal_institution_name")
            ),
            When(first_activity=F("first_custom_charge"), then=F("first_custom_charge_institution_name")),
        ),
        first_activity_institution_type=Case(
            When(first_activity=F("first_tool_usage"), then=F("first_tool_usage_institution_type")),
            When(first_activity=F("first_area_access"), then=F("first_area_access_institution_type")),
            When(first_activity=F("first_staff_charge"), then=F("first_staff_charge_institution_type")),
            When(first_activity=F("first_training"), then=F("first_training_institution_type")),
            When(first_activity=F("first_missed_reservation"), then=F("first_missed_reservation_institution_type")),
            When(
                first_activity=F("first_consumable_withdrawal"), then=F("first_consumable_withdrawal_institution_type")
            ),
            When(first_activity=F("first_custom_charge"), then=F("first_custom_charge_institution_type")),
        ),
    )
    users = users.filter(first_activity__gte=start_datetime, first_activity__lte=end_datetime)
    return users
