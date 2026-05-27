from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home_view(request):
    return render(request, 'grievances/home.html')


@login_required
def municipality_dashboard(request):
    return render(request, 'grievances/dashboard.html')