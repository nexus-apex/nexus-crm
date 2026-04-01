import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import Contact, Deal, Activity


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['contact_count'] = Contact.objects.count()
    ctx['contact_lead'] = Contact.objects.filter(status='lead').count()
    ctx['contact_customer'] = Contact.objects.filter(status='customer').count()
    ctx['contact_prospect'] = Contact.objects.filter(status='prospect').count()
    ctx['contact_total_value'] = Contact.objects.aggregate(t=Sum('value'))['t'] or 0
    ctx['deal_count'] = Deal.objects.count()
    ctx['deal_qualification'] = Deal.objects.filter(stage='qualification').count()
    ctx['deal_proposal'] = Deal.objects.filter(stage='proposal').count()
    ctx['deal_negotiation'] = Deal.objects.filter(stage='negotiation').count()
    ctx['deal_total_value'] = Deal.objects.aggregate(t=Sum('value'))['t'] or 0
    ctx['activity_count'] = Activity.objects.count()
    ctx['activity_call'] = Activity.objects.filter(activity_type='call').count()
    ctx['activity_email'] = Activity.objects.filter(activity_type='email').count()
    ctx['activity_meeting'] = Activity.objects.filter(activity_type='meeting').count()
    ctx['recent'] = Contact.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def contact_list(request):
    qs = Contact.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'contact_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def contact_create(request):
    if request.method == 'POST':
        obj = Contact()
        obj.name = request.POST.get('name', '')
        obj.company = request.POST.get('company', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.status = request.POST.get('status', '')
        obj.source = request.POST.get('source', '')
        obj.value = request.POST.get('value') or 0
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/contacts/')
    return render(request, 'contact_form.html', {'editing': False})


@login_required
def contact_edit(request, pk):
    obj = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.company = request.POST.get('company', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.status = request.POST.get('status', '')
        obj.source = request.POST.get('source', '')
        obj.value = request.POST.get('value') or 0
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/contacts/')
    return render(request, 'contact_form.html', {'record': obj, 'editing': True})


@login_required
def contact_delete(request, pk):
    obj = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/contacts/')


@login_required
def deal_list(request):
    qs = Deal.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(stage=status_filter)
    return render(request, 'deal_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def deal_create(request):
    if request.method == 'POST':
        obj = Deal()
        obj.title = request.POST.get('title', '')
        obj.company = request.POST.get('company', '')
        obj.value = request.POST.get('value') or 0
        obj.stage = request.POST.get('stage', '')
        obj.probability = request.POST.get('probability') or 0
        obj.expected_close = request.POST.get('expected_close') or None
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/deals/')
    return render(request, 'deal_form.html', {'editing': False})


@login_required
def deal_edit(request, pk):
    obj = get_object_or_404(Deal, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '')
        obj.company = request.POST.get('company', '')
        obj.value = request.POST.get('value') or 0
        obj.stage = request.POST.get('stage', '')
        obj.probability = request.POST.get('probability') or 0
        obj.expected_close = request.POST.get('expected_close') or None
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/deals/')
    return render(request, 'deal_form.html', {'record': obj, 'editing': True})


@login_required
def deal_delete(request, pk):
    obj = get_object_or_404(Deal, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/deals/')


@login_required
def activity_list(request):
    qs = Activity.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(subject__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(activity_type=status_filter)
    return render(request, 'activity_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def activity_create(request):
    if request.method == 'POST':
        obj = Activity()
        obj.subject = request.POST.get('subject', '')
        obj.related_to = request.POST.get('related_to', '')
        obj.activity_type = request.POST.get('activity_type', '')
        obj.scheduled = request.POST.get('scheduled') or None
        obj.done = request.POST.get('done') == 'on'
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/activities/')
    return render(request, 'activity_form.html', {'editing': False})


@login_required
def activity_edit(request, pk):
    obj = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        obj.subject = request.POST.get('subject', '')
        obj.related_to = request.POST.get('related_to', '')
        obj.activity_type = request.POST.get('activity_type', '')
        obj.scheduled = request.POST.get('scheduled') or None
        obj.done = request.POST.get('done') == 'on'
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/activities/')
    return render(request, 'activity_form.html', {'record': obj, 'editing': True})


@login_required
def activity_delete(request, pk):
    obj = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/activities/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['contact_count'] = Contact.objects.count()
    data['deal_count'] = Deal.objects.count()
    data['activity_count'] = Activity.objects.count()
    return JsonResponse(data)
