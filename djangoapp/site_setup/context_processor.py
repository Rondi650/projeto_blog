from django.http import HttpRequest
from site_setup.models import SiteSetup

def site_setup(request: HttpRequest):
    setup = SiteSetup.objects.order_by('-id').first()
    
    # Para debug
    print("-"*50,"\n","SITE_SETUP VALIDATION", sep="")
    print(f'Validating setup: {setup}')
    for chave, valor in setup.__dict__.items():
        print(chave, ": " ,valor)
    print("-"*50)
    
    return {
        'site_setup': setup,
    }
    