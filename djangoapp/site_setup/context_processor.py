from django.http import HttpRequest
from site_setup.models import SiteSetup

def site_setup(request: HttpRequest):
    setup = SiteSetup.objects.order_by('-id').first()
    
    return {
        'site_setup': setup,
    }