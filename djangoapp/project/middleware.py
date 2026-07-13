"""
Middleware para controle de cache no Cloudflare
"""


class StaticFilesCacheMiddleware:
    """
    Adiciona headers de cache apropriados para arquivos estáticos.
    Como usamos ManifestStaticFilesStorage (cache busting com hash),
    podemos permitir cache agressivo desses arquivos.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Verifica se é um arquivo estático
        if request.path.startswith('/static/'):
            # Cache por 1 ano (31536000 segundos) para arquivos com hash
            # O hash no nome garante que uma nova versão terá um URL diferente
            response['Cache-Control'] = 'public, max-age=31536000, immutable'
            response['Vary'] = 'Accept-Encoding'
        elif request.path.startswith('/media/'):
            # Cache por 1 dia para arquivos de mídia
            response['Cache-Control'] = 'public, max-age=86400'

        return response
