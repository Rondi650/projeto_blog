# Fluxo completo de uma imagem: do upload à tela do usuário

## PARTE 1 — Upload (Django trabalha)

```
Navegador → POST /admin/blog/post/1/change/ (form com imagem)
                             │
                             ▼
                    D J A N G O  (Gunicorn)
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
     1. Recebe o      2. Valida        3. Salva no disco
     arquivo          (tipo,           /data/web/media/
     multipart        tamanho)         posts/2026/07/foto.jpg
            │
            │
            ├── 4. Roda resize_image() com Pillow
            │    Redimensiona pra 900px de largura
            │
            └── 5. Salva o path no PostgreSQL
                 posts.cover = "posts/2026/07/foto.jpg"
```

---

## PARTE 2 — Requisição da página (Django gera HTML com o caminho)

```
                    NAVEGADOR
                         │
                         │ ① GET /post/meu-artigo/
                         ▼
              ┌─────────────────────┐
              │      TRAEFIK        │
              │  Rótulo default →   │
              │  djangoapp:8000     │
              └──────────┬──────────┘
                         │ ②
                         ▼
              ┌─────────────────────┐    ③ consulta     ┌──────────┐
              │  DJANGO (Gunicorn)  │──────────────────▶ │  PSQL    │
              │                     │◀────────────────── │  (banco) │
              │  post.cover =       │     devolve path   └──────────┘
              │  "posts/2026/07/    │
              │   foto.jpg"         │
              │                     │
              │  Template render:   │
              │  <img src="{{       │
              │  post.cover.url }}">│
              │                     │
              │  Gera HTML:         │
              │  <img src="/media/  │
              │  posts/2026/07/     │
              │  foto.jpg">         │
              └──────────┬──────────┘
                         │ ④ HTML pronto
                         │
                         ▼
              ┌─────────────────────┐
              │      TRAEFIK        │
              └──────────┬──────────┘
                         │ ⑤
                         ▼
                    NAVEGADOR
               Renderiza o HTML
               Encontra a tag <img src="...">
```

---

## PARTE 3 — Requisição da imagem (nginx serve do disco)

```
                    NAVEGADOR
                         │
                         │ ⑥ GET /media/posts/2026/07/foto.jpg
                         ▼
              ┌─────────────────────┐
              │      TRAEFIK        │
              │  Lê as labels:      │
              │  PathPrefix /media/ │
              │  → nginx-static:80  │
              └──────────┬──────────┘
                         │ ⑦
                         ▼
              ┌───────────────────────┐
              │   NGINX-STATIC        │
              │                       │
              │  location /media/ {   │
              │    alias /data/web/   │
              │    media/;            │
              │  }                    │
              │                       │
              │  Lê do DISCO:         │
              │  /data/web/media/     │
              │  posts/2026/07/       │
              │  foto.jpg             │
              │                       │
              │  Headers:             │
              │  • Cache-Control:     │
              │    public, immutable  │
              │  • Expires: 1y        │
              └──────────┬────────────┘
                         │ ⑧ bytes da imagem
                         │
                         ▼
              ┌─────────────────────┐
              │      TRAEFIK        │
              └──────────┬──────────┘
                         │ ⑨
                         ▼
                    NAVEGADOR
               Renderiza a imagem na tela
```

---

## E o disco?

```
                    SEU SSD (HOST)
                    ./data/web/media/
                           │
               ┌───────────┴───────────┐
               │                       │
               ▼                       ▼
         djangoapp_psql           nginx-static
         (escreve aqui no        (lê daqui no
          momento do upload)      momento do serve)

         Mesma pasta via bind mount do Docker.
         Nenhum HTTP entre Django e nginx.
```

---

## Resumo dos 9 passos

| Passo | De        | Para      | O que acontece                                   |
| ----- | --------- | --------- | ------------------------------------------------ |
| ①    | Navegador | Traefik   | GET /post/meu-artigo/                            |
| ②    | Traefik   | Django    | Roteia pro Gunicorn (padrão)                    |
| ③    | Django    | PSQL      | Consulta o path da imagem no banco               |
| ④    | Django    | —        | Renderiza template com`<img src="/media/...">` |
| ⑤    | Traefik   | Navegador | Devolve o HTML                                   |
| ⑥    | Navegador | Traefik   | GET /media/posts/2026/07/foto.jpg                |
| ⑦    | Traefik   | nginx     | Roteia via PathPrefix /media/                    |
| ⑧    | nginx     | Traefik   | Lê do disco, devolve bytes                      |
| ⑨    | Traefik   | Navegador | Imagem chega pro usuário                        |
