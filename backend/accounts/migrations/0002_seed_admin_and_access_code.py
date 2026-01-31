from django.conf import settings
from django.db import migrations


def seed_admin(apps, schema_editor):
    user_model = apps.get_model('auth', 'User')
    admin_email = 'mail@whystudio.info'
    admin_password = 'thecreatorV11'

    admin_user, created = user_model.objects.get_or_create(
        username=admin_email,
        defaults={
            'email': admin_email,
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        },
    )
    if created:
        admin_user.set_password(admin_password)
        admin_user.save(update_fields=['password'])

    access_code_model = apps.get_model('accounts', 'AccessCode')
    access_code_model.objects.get_or_create(code='API-ACCESS-DEV')


def unseed_admin(apps, schema_editor):
    user_model = apps.get_model('auth', 'User')
    user_model.objects.filter(username='mail@whystudio.info').delete()
    access_code_model = apps.get_model('accounts', 'AccessCode')
    access_code_model.objects.filter(code='API-ACCESS-DEV').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(seed_admin, unseed_admin),
    ]
