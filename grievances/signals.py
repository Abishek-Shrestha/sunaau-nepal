from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from .models import Issue, Notification
from accounts.models import CustomUser


@receiver(post_save, sender=Issue)
def notify_on_new_issue(sender, instance, created, **kwargs):
    if not created:
        return

    # Find all officers for this municipality + all admins
    recipients = CustomUser.objects.filter(
        role__in=['officer', 'admin']
    )

    if instance.municipality:
        recipients = recipients.filter(
            models.Q(municipality=instance.municipality) |
            models.Q(role='admin')
        )

    message = (
        f"New {instance.get_severity_display()} issue reported: "
        f"'{instance.title}' in "
        f"{instance.municipality.name if instance.municipality else 'Unknown Municipality'}"
        f", Ward {instance.ward_number or 'N/A'}."
    )

    # Create in-app notification for each officer/admin
    for user in recipients:
        Notification.objects.create(
            recipient=user,
            issue=instance,
            notification_type='new_issue',
            message=message,
        )

    # Send email notification
    officer_emails = list(recipients.values_list('email', flat=True))
    officer_emails = [e for e in officer_emails if e]  # remove empty emails

    if officer_emails:
        try:
            send_mail(
                subject=f'[SunaauNepal] New Issue — {instance.title}',
                message=f"""
A new infrastructure issue has been reported.

Title: {instance.title}
Category: {instance.get_category_display()}
Severity: {instance.get_severity_display()}
Municipality: {instance.municipality.name if instance.municipality else 'Not specified'}
Ward: {instance.ward_number or 'Not specified'}
Location: {instance.location_name or 'Not specified'}
Description: {instance.description}

Reported at: {instance.created_at.strftime('%Y-%m-%d %H:%M')}

Login to your dashboard to review and assign this issue.
http://127.0.0.1:8000/dashboard/
                """.strip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=officer_emails,
                fail_silently=True,
            )
        except Exception:
            pass  # Never let email failure crash the report submission