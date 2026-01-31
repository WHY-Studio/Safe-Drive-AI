from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404


def frontend_root(request):
    return frontend_file(request, 'Home.html')


def frontend_file(request, path):
    frontend_dir = Path(settings.FRONTEND_DIR)
    target = (frontend_dir / path).resolve()
    if not str(target).startswith(str(frontend_dir.resolve())):
        raise Http404
    if not target.exists() or not target.is_file():
        raise Http404
    return FileResponse(target.open('rb'))
