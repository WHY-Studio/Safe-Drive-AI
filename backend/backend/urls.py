from django.contrib import admin
from django.urls import include, path

from backend import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('', views.frontend_root, name='frontend-root'),
    path('<path:path>', views.frontend_file, name='frontend-file'),
]
