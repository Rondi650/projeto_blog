from django.http import HttpRequest
from site_setup.models import SiteSetup


def site_setup(request: HttpRequest):
    setup = SiteSetup.objects.order_by('-id').first()

    # Inicio debug
    print("-"*50, "\n", "SITE_SETUP MENU LINKS", sep="")
    if setup:
        for link in setup.menu_links.all():  # type:ignore
            print(link)

    print("-"*50, "\n", "SITE_SETUP FIELDS", sep="")
    for chave, valor in setup.__dict__.items():
        print(chave, ": ", valor)
    print("-"*50)
    # Fim do debug
    
    if setup is None:
        return {}  # retorna contexto vazio, sem quebrar

    return {
        'site_setup': setup,
    }
