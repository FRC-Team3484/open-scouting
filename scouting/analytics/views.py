import json

from django.utils.timezone import now, timedelta
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from .models import PageView


def get_view_count_since(hours=0, days=0, months=0, years=0):
    from dateutil.relativedelta import relativedelta

    since = now() - relativedelta(hours=hours, days=days, months=months, years=years)
    return PageView.objects.filter(timestamp__gte=since).count()


def get_analytics(request):
    if request.method != "POST":
        return HttpResponse("Request is not a POST request!", status=501)

    data = {
        "1_hour": get_view_count_since(hours=1),
        "12_hours": get_view_count_since(hours=12),
        "24_hours": get_view_count_since(hours=24),
        "3_days": get_view_count_since(days=3),
        "7_days": get_view_count_since(days=7),
        "1_month": get_view_count_since(months=1),
        "3_months": get_view_count_since(months=3),
        "6_months": get_view_count_since(months=6),
        "1_year": get_view_count_since(years=1),
        "all_time": PageView.objects.count(),
    }
    return JsonResponse(json.dumps(data), safe=False)
