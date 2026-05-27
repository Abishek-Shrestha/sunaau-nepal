from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import Issue
from accounts.models import Municipality


def home_view(request):
    total_issues = Issue.objects.count()
    resolved_issues = Issue.objects.filter(status='resolved').count()
    total_municipalities = Municipality.objects.count()

    resolved_rate = 0
    if total_issues > 0:
        resolved_rate = round((resolved_issues / total_issues) * 100)

    recent_issues = Issue.objects.select_related(
        'municipality', 'reported_by'
    ).order_by('-created_at')[:5]

    context = {
        'total_issues': total_issues,
        'resolved_rate': resolved_rate,
        'total_municipalities': total_municipalities,
        'recent_issues': recent_issues,
    }
    return render(request, 'grievances/home.html', context)


@login_required
def municipality_dashboard(request):
    return render(request, 'grievances/dashboard.html')


@login_required
def my_reports(request):
    issues = Issue.objects.filter(
        reported_by=request.user
    ).order_by('-created_at')
    return render(request, 'grievances/my_reports.html', {'issues': issues})