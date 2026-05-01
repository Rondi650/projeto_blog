# 🧪 Guia Básico de Testes Django

## O que são testes?

Testes são códigos que verificam se seu código funciona corretamente. Eles ajudam a:
- Garantir que tudo funciona antes de publicar
- Encontrar bugs antes dos usuários
- Ter confiança para fazer mudanças no código

---

## 🏃 Como rodar os testes

### 1. Rodar TODOS os testes
```bash
cd /home/rondi/dev/python_projects/django/blog/djangoapp
python manage.py test
```

### 2. Rodar testes de UM app específico
```bash
# Testes do app blog
python manage.py test blog

# Testes do app site_setup
python manage.py test site_setup
```

### 3. Rodar UMA classe de teste específica
```bash
# Testar só os modelos de Tag
python manage.py test blog.tests.TagModelTest

# Testar só as views
python manage.py test blog.tests.BlogViewsTest
```

### 4. Rodar UM teste específico
```bash
# Testar só um método específico
python manage.py test blog.tests.TagModelTest.test_tag_str_returns_name
```

### 5. Rodar com mais detalhes (verbose)
```bash
# Mostra o nome de cada teste
python manage.py test --verbosity=2
```

### 6. Rodar e parar no primeiro erro
```bash
python manage.py test --failfast
```

---

## 📊 Entendendo o resultado

### ✅ SUCESSO
```
Ran 10 tests in 0.523s

OK
```

### ❌ FALHA
```
======================================================================
FAIL: test_tag_str_returns_name (blog.tests.TagModelTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  AssertionError: 'Python' != 'Java'
----------------------------------------------------------------------
Ran 10 tests in 0.523s

FAILED (failures=1)
```

---

## 📝 Explicando os testes criados

### Testes de Modelo (Models)

```python
class TagModelTest(TestCase):
    def setUp(self):
        # Cria uma tag antes de cada teste
        self.tag = Tag.objects.create(name="Python")
    
    def test_tag_str_returns_name(self):
        # Verifica se str(tag) retorna "Python"
        self.assertEqual(str(self.tag), "Python")
```

**O que testa:**
- Se o método `__str__` funciona
- Se o slug é gerado automaticamente
- Se a URL absoluta está correta

---

### Testes de View (Views)

```python
def test_index_view_status_code(self):
    # Faz uma requisição GET para a URL 'index'
    response = self.client.get(reverse('blog:index'))
    # Verifica se retornou código 200 (sucesso)
    self.assertEqual(response.status_code, 200)
```

**O que testa:**
- Se a página carrega (status 200)
- Se usa o template correto
- Se o contexto tem os dados certos
- Se página não publicada retorna 404

---

## 🔧 Comandos úteis para lembrar

| Comando | Descrição |
|---------|-----------|
| `python manage.py test` | Roda todos os testes |
| `python manage.py test blog` | Roda testes do app blog |
| `python manage.py test --verbosity=2` | Mostra mais detalhes |
| `python manage.py test --failfast` | Para no primeiro erro |
| `python manage.py test -k nome_do_teste` | Roda testes com nome específico |

---

## 🎯 Cenários comuns de teste

### 1. Testar se uma página existe
```python
def test_page_exists(self):
    response = self.client.get('/sobre/')
    self.assertEqual(response.status_code, 200)
```

### 2. Testar se modelo salva corretamente
```python
def test_model_creation(self):
    tag = Tag.objects.create(name="Teste")
    self.assertEqual(Tag.objects.count(), 1)
    self.assertEqual(tag.name, "Teste")
```

### 3. Testar se login é necessário
```python
def test_protected_page_requires_login(self):
    response = self.client.get('/admin/')
    self.assertEqual(response.status_code, 302)  # Redireciona para login
```

---

## 💡 Dicas

1. **Sempre use `setUp()`** para criar dados de teste - ele roda antes de cada teste
2. **Nomeie os testes de forma descritiva** - `test_user_can_create_post` é melhor que `test_create`
3. **Um teste deve verificar UMA coisa** - mantenha os testes simples
4. **Use `self.client`** para simular requisições HTTP
5. **Use `reverse()`** para URLs - não escreva URLs hardcoded

---

## 📚 Links úteis

- [Documentação de Testes Django](https://docs.djangoproject.com/en/5.0/topics/testing/)
- [Tipos de assertivas](https://docs.djangoproject.com/en/5.0/topics/testing/tools/#assertions)

---

## 🚀 Próximos passos

Depois de entender esses testes básicos, você pode aprender:

1. **Testes de formulários** - verificar se formulários validam corretamente
2. **Testes de API** - se você usar Django REST Framework
3. **Testes de JavaScript** - para a parte frontend
4. **Cobertura de código** - medir quanto do código está testado

---

**Pronto! Agora é só rodar `python manage.py test` e ver seus testes passando! 🎉**
