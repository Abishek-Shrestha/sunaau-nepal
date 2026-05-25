from django.db import models
from accounts.models import CustomUser, Municipality


class Issue(models.Model):

    CATEGORY_CHOICES = (
        ('pothole', '🕳️ Pothole / Road Damage'),
        ('streetlight', '💡 Broken Streetlight'),
        ('drainage', '🚰 Drainage / Sewage Problem'),
        ('bridge', '🌉 Bridge / Footpath Damage'),
        ('garbage', '🚮 Garbage / Waste Disposal'),
        ('water', '💧 Water Supply Issue'),
        ('tree', '🌳 Fallen Tree / Hazard'),
        ('other', '⚠️ Other'),
    )

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    )

    SEVERITY_CHOICES = (
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('critical', 'Critical'),
    )

    # Core fields
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='minor')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    # Location fields
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_name = models.CharField(max_length=255, blank=True)
    ward_number = models.PositiveIntegerField(null=True, blank=True)
    municipality = models.ForeignKey(
        Municipality,
        on_delete=models.SET_NULL,
        null=True,
        related_name='issues'
    )

    # Photo
    photo = models.ImageField(upload_to='issues/%Y/%m/', blank=True, null=True)

    # Relations
    reported_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reported_issues'
    )
    assigned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_issues'
    )

    # Engagement
    upvotes = models.PositiveIntegerField(default=0)
    is_anonymous = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title}"

    class Meta:
        ordering = ['-created_at']


class IssueUpdate(models.Model):
    """Tracks status changes and municipality updates on an issue"""
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='updates')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20, blank=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.issue.title} → {self.new_status}"
