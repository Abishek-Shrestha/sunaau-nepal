from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import IssueReportForm
from django.utils import timezone
from django.db.models import Count, Q
from .models import Issue
from .models import Issue, Notification
from accounts.models import Municipality
import json
from django.core.serializers.base import SerializationError

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
def report_issue(request):
    if request.method == 'POST':
        form = IssueReportForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)

            if request.user.is_authenticated and not form.cleaned_data.get('is_anonymous'):
                issue.reported_by = request.user
            
            issue.save()
            messages.success(request, '✅ Your report has been submitted successfully! We will notify you of updates.')
            return redirect('issue_detail', pk=issue.pk)
    else:
        form = IssueReportForm(initial={
            'municipality': request.user.municipality,
            'ward_number': request.user.ward_number,
        })

    return render(request, 'grievances/report_issue.html', {'form': form})


@login_required
def my_reports(request):
    issues = Issue.objects.filter(
        reported_by=request.user
    ).order_by('-created_at')
    return render(request, 'grievances/my_reports.html', {'issues': issues})


def issue_detail(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    updates = issue.updates.all().order_by('created_at')
    return render(request, 'grievances/issue_detail.html', {
        'issue': issue,
        'updates': updates,
    })


@login_required
def municipality_dashboard(request):
    return render(request, 'grievances/dashboard.html')

@login_required
def notifications_view(request):
    notifs = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    notifs.filter(is_read=False).update(is_read=True)  # Mark all as read when viewing  
    return render(request, 'grievances/notifications.html', {'notifications': notifs})

@login_required
def mark_notification_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notif.is_read = True
    notif.save()
    if notif.issue:
        return redirect('issue_detail', pk=notif.issue.pk)
    return redirect('notifications')

def issue_map(request):
    # Only get issues that have GPS coordinates
    issues = Issue.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    ).select_related('municipality')

    # Build a JSON list for Leaflet
    issues_data = []
    for issue in issues:
        issues_data.append({
            'id': issue.id,
            'title': issue.title,
            'category': issue.category,
            'category_display': issue.get_category_display(),
            'severity': issue.severity,
            'status': issue.status,
            'status_display': issue.get_status_display(),
            'lat': float(issue.latitude),
            'lng': float(issue.longitude),
            'location': issue.location_name or '',
            'municipality': issue.municipality.name if issue.municipality else '',
            'ward': issue.ward_number or '',
            'photo': issue.photo.url if issue.photo else '',
            'created_at': issue.created_at.strftime('%b %d, %Y'),
            'url': f'/issue/{issue.id}/',
        })

    municipalities = Municipality.objects.all().order_by('name')

    return render(request, 'grievances/map.html', {
        'issues_json': json.dumps(issues_data),
        'municipalities': municipalities,
        'total_count': issues.count(),
    })