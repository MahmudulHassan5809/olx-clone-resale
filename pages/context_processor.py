from .models import Setting


def setting(request):
    setting = Setting.objects.all().first()
    return {'setting': setting}
