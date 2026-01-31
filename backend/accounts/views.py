import json

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from accounts.models import AccessCode


def _parse_payload(request):
    if request.content_type == 'application/json':
        try:
            return json.loads(request.body or '{}')
        except json.JSONDecodeError:
            return {}
    return request.POST


@csrf_exempt
def register_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Nur POST erlaubt.'}, status=405)

    payload = _parse_payload(request)
    email = (payload.get('email') or '').strip().lower()
    password = payload.get('password') or ''
    access_code = (payload.get('access_code') or '').strip()

    if not email or not password or not access_code:
        return JsonResponse({'error': 'Email, Passwort und Zugangscode sind erforderlich.'}, status=400)

    user_model = get_user_model()
    if user_model.objects.filter(email__iexact=email).exists():
        return JsonResponse({'error': 'Diese Email ist bereits registriert.'}, status=400)

    with transaction.atomic():
        try:
            code = AccessCode.objects.select_for_update().get(code=access_code)
        except AccessCode.DoesNotExist:
            return JsonResponse({'error': 'Zugangscode ist ungültig.'}, status=400)

        if code.is_used:
            return JsonResponse({'error': 'Zugangscode wurde bereits verwendet.'}, status=400)

        user = user_model.objects.create_user(
            username=email,
            email=email,
            password=password,
        )
        code.is_used = True
        code.used_by = user
        code.used_at = timezone.now()
        code.save(update_fields=['is_used', 'used_by', 'used_at'])

    return JsonResponse({'success': True, 'message': 'Registrierung erfolgreich.'})


@csrf_exempt
def login_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Nur POST erlaubt.'}, status=405)

    payload = _parse_payload(request)
    email = (payload.get('email') or '').strip().lower()
    password = payload.get('password') or ''

    if not email or not password:
        return JsonResponse({'error': 'Email und Passwort sind erforderlich.'}, status=400)

    user = authenticate(request, email=email, password=password)
    if user is None:
        return JsonResponse({'error': 'Login fehlgeschlagen.'}, status=401)

    login(request, user)
    role = 'admin' if user.is_staff or user.is_superuser else 'customer'

    return JsonResponse({
        'success': True,
        'role': role,
        'user': {
            'email': user.email,
            'username': user.username,
        },
    })


@csrf_exempt
def logout_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Nur POST erlaubt.'}, status=405)

    logout(request)
    return JsonResponse({'success': True})


def me_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'authenticated': False}, status=401)

    role = 'admin' if request.user.is_staff or request.user.is_superuser else 'customer'
    return JsonResponse({
        'authenticated': True,
        'role': role,
        'user': {
            'email': request.user.email,
            'username': request.user.username,
        },
    })
