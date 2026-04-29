# Blog - Deploy com Nginx + Gunicorn + PostgreSQL

## Visão Geral da Arquitetura

```
Internet
   │
   ▼
Cloudflare (SSL termination + CDN)
   │
   ▼
Nginx (porta 80/443) — reverse proxy
   │
   ├── /static/ → serve direto do disco
   ├── /media/  → serve direto do disco
   └── /        → proxy_pass → Gunicorn (127.0.0.1:8000)
                        │
                        ▼
                   Django App (3 workers)
                        │
                        ▼
                   PostgreSQL (container)
```

### Como funciona o fluxo

1. **O usuário acessa** `https://blog.samaramutielli.site`
2. **Cloudflare** recebe a requisição, aplica bot challenge e encaminha para o servidor
3. **Nginx** recebe na porta 443 (SSL já configurado pelo Certbot)
4. **Arquivos estáticos** (`/static/`, `/media/`) são servidos **diretamente pelo nginx** do disco — sem passar pelo Django
5. **Demais requisições** (`/`, `/admin/`, `/post/...`) são encaminhadas via `proxy_pass` para `127.0.0.1:8000`
6. **Gunicorn** recebe a requisição, repassa ao Django que processa e retorna a resposta
7. **Nginx** devolve a resposta ao Cloudflare → usuário

---

## Arquivos Alterados

### 1. `djangoapp/requirements.txt`

Adicionado Gunicorn como última linha:

```txt
asgiref==3.11.1
Django==6.0.4
sqlparse==0.5.5
dotenv==0.9.9
python-dotenv==1.2.2
psycopg2-binary==2.9.10
pillow==10.4.0
django-summernote==0.8.20.0
django-axes==8.3.1
gunicorn==25.3.0
```

### 2. `scripts/commands.sh`

Substituído `runserver` por `gunicorn`:

```sh
#!/bin/sh
set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo 'Waiting for Database ...'
  sleep 2
done

echo 'Database Started Successfully'

python3 manage.py collectstatic --noinput
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
gunicorn project.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
```

### 3. `.env`

Adicionado o domínio ao `ALLOWED_HOSTS`:

```env
ALLOWED_HOSTS="127.0.0.1, localhost, 34.228.105.77, blog.samaramutielli.site"
```

### 4. `psql_docker-compose.yml`

Removida a porta pública e adicionado mapeamento **apenas em localhost** (nginx acessa internamente):

```yaml
services:
  djangoapp_psql:
    container_name: djangoapp_psql
    restart: unless-stopped
    build:
      context: .
    ports:
      - "127.0.0.1:8000:8000"
    volumes:
      - ./djangoapp:/djangoapp
      - ./data/web/static:/data/web/static/
      - ./data/web/media:/data/web/media/
    env_file:
      - ./.env
    depends_on:
      - psql

  psql:
    container_name: psql
    image: postgres:16-alpine
    volumes:
      - ./data/postgres/data:/var/lib/postgresql/data/
    env_file:
      - ./.env

volumes:
  static_data:
  media_data:
  postgres_data:
```

---

## Arquivos Criados

### 5. `/etc/nginx/sites-available/blog.samaramutielli.site`

*(Criado com `sudo`)* — Configuração do vhost nginx:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name blog.samaramutielli.site www.blog.samaramutielli.site;

    root /home/ubuntu/projeto_blog/data/web;

    location /static/ {
        alias /home/ubuntu/projeto_blog/data/web/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /home/ubuntu/projeto_blog/data/web/media/;
        expires 7d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location ~ /\. {
        deny all;
    }

    access_log /var/log/nginx/blog-access.log;
    error_log  /var/log/nginx/blog-error.log warn;
}
```

O Certbot modificou este arquivo automaticamente após a emissão do SSL, adicionando:
- `listen 443 ssl` e `listen [::]:443 ssl`
- `ssl_certificate` e `ssl_certificate_key`
- `include /etc/letsencrypt/options-ssl-nginx.conf`
- `ssl_dhparam`
- Bloco de redirect HTTP→HTTPS (server block separado)

### 6. Symlink

```bash
sudo ln -sf /etc/nginx/sites-available/blog.samaramutielli.site /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

---

## SSL (Let's Encrypt)

```bash
sudo certbot --nginx -d blog.samaramutielli.site --non-interactive --agree-tos --email rondi@email.com --redirect
```

- Certificado válido até **28/07/2026**
- Renovação automática configurada pelo Certbot
- O domínio `www.blog.samaramutielli.site` **não tem** registro DNS e não foi incluído

---

## Comandos Úteis

### Subir o projeto

```bash
cd /home/ubuntu/projeto_blog
docker compose -f psql_docker-compose.yml up -d --build
```

### Ver logs do Django

```bash
docker logs djangoapp_psql -f
```

### Ver logs do PostgreSQL

```bash
docker logs psql -f
```

### Ver logs do nginx

```bash
sudo tail -f /var/log/nginx/blog-access.log
sudo tail -f /var/log/nginx/blog-error.log
```

### Testar resposta local (bypass Cloudflare)

```bash
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/
curl -s -o /dev/null -w "%{http_code}" -H "Host: blog.samaramutielli.site" http://127.0.0.1/
```

### Testar HTTPS externo

```bash
curl -sI https://blog.samaramutielli.site/
```

### Verificar workers do Gunicorn

```bash
docker exec djangoapp_psql ps aux
```

### Renovar certificado manualmente

```bash
sudo certbot renew --dry-run
sudo certbot renew
```

---

## Detalhes dos Serviços

| Serviço | Tipo | Acesso |
|---|---|---|
| **Gunicorn** | WSGI server | `0.0.0.0:8000` dentro do container, mapeado para `127.0.0.1:8000` no host |
| **Gunicorn workers** | 3 sync workers | PID master (12) + 3 workers (13, 14, 15) |
| **PostgreSQL** | 16-alpine | Container interno, porta não exposta ao host |
| **Nginx** | Reverse proxy | Portas 80/443 públicas |
| **Cloudflare** | CDN + Proxy | Termina SSL, encaminha para origem HTTP |
| **Certbot** | Let's Encrypt | Renovação automática agendada |

---

## Cache de Arquivos Estáticos

Os headers `expires` no nginx configuram cache no navegador:

- **`/static/`** → `expires 30d` — arquivos de CSS, JS, imagens do admin. Cache longo pois mudam raramente.
- **`/media/`** → `expires 7d` — uploads de imagens do blog. Cache menor pois podem ser trocados.

O `Cache-Control "public, immutable"` nos static diz ao navegador que o arquivo **nunca muda** durante o período de cache, evitando revalidações desnecessárias.
