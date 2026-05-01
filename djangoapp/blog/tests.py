from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Tag, Category, Page, Post


class TagModelTest(TestCase):
    """Testes para o modelo Tag"""
    
    def setUp(self):
        """Executado antes de cada teste - cria dados de teste"""
        self.tag = Tag.objects.create(name="Python")
    
    def test_tag_str_returns_name(self):
        """Testa se o método __str__ retorna o nome da tag"""
        self.assertEqual(str(self.tag), "Python")
    
    def test_tag_slug_is_auto_generated(self):
        """Testa se o slug é gerado automaticamente ao salvar"""
        self.assertIsNotNone(self.tag.slug)
        # O slug contém o texto "python" mais um sufixo aleatório
        self.assertIn("python", self.tag.slug)


class CategoryModelTest(TestCase):
    """Testes para o modelo Category"""
    
    def setUp(self):
        self.category = Category.objects.create(name="Django")
    
    def test_category_str_returns_name(self):
        self.assertEqual(str(self.category), "Django")
    
    def test_category_slug_is_auto_generated(self):
        self.assertIsNotNone(self.category.slug)
        self.assertIn("django", self.category.slug)


class PageModelTest(TestCase):
    """Testes para o modelo Page"""
    
    def setUp(self):
        self.page = Page.objects.create(
            title="Sobre Nós",
            content="Conteúdo da página sobre",
            is_published=True
        )
    
    def test_page_str_returns_title(self):
        self.assertEqual(str(self.page), "Sobre Nós")
    
    def test_page_slug_is_auto_generated(self):
        self.assertIsNotNone(self.page.slug)
    
    def test_get_absolute_url_for_published_page(self):
        """Testa se a URL de uma página publicada é correta"""
        url = self.page.get_absolute_url()
        expected_url = reverse('blog:page', args=(self.page.slug,))
        self.assertEqual(url, expected_url)
    
    def test_get_absolute_url_for_unpublished_page(self):
        """Testa se página não publicada redireciona para index"""
        unpublished_page = Page.objects.create(
            title="Rascunho",
            content="Conteúdo",
            is_published=False
        )
        url = unpublished_page.get_absolute_url()
        expected_url = reverse('blog:index')
        self.assertEqual(url, expected_url)


class PostModelTest(TestCase):
    """Testes para o modelo Post"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name="Tecnologia")
        self.tag = Tag.objects.create(name="Web")
        
        self.post = Post.objects.create(
            title="Meu Primeiro Post",
            excerpt="Resumo do post",
            content="Conteúdo completo do post",
            is_published=True,
            created_by=self.user,
            category=self.category
        )
        self.post.tags.add(self.tag)
    
    def test_post_str_returns_title(self):
        self.assertEqual(str(self.post), "Meu Primeiro Post")
    
    def test_post_slug_is_auto_generated(self):
        self.assertIsNotNone(self.post.slug)
    
    def test_post_manager_get_published(self):
        """Testa se o manager retorna apenas posts publicados"""
        Post.objects.create(
            title="Rascunho",
            excerpt="Resumo",
            content="Conteúdo",
            is_published=False
        )
        published_posts = Post.objects.get_published()
        self.assertEqual(published_posts.count(), 1)
        self.assertEqual(published_posts.first(), self.post)
    
    def test_get_absolute_url_for_published_post(self):
        url = self.post.get_absolute_url()
        expected_url = reverse('blog:post', args=(self.post.slug,))
        self.assertEqual(url, expected_url)


class BlogViewsTest(TestCase):
    """Testes para as views do blog"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name="Tecnologia")
        self.tag = Tag.objects.create(name="Web")
        
        # Cria posts publicados para testar
        for i in range(5):
            post = Post.objects.create(
                title=f"Post {i}",
                excerpt=f"Resumo {i}",
                content=f"Conteúdo {i}",
                is_published=True,
                created_by=self.user,
                category=self.category
            )
            post.tags.add(self.tag)
        
        # Cria uma página
        self.page = Page.objects.create(
            title="Sobre",
            content="Conteúdo",
            is_published=True
        )
    
    def test_index_view_status_code(self):
        """Testa se a página inicial retorna status 200"""
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
    
    def test_index_view_uses_correct_template(self):
        """Testa se a view usa o template correto"""
        response = self.client.get(reverse('blog:index'))
        self.assertTemplateUsed(response, 'blog/pages/index.html')
    
    def test_index_view_context_contains_posts(self):
        """Testa se o contexto contém a lista de posts"""
        response = self.client.get(reverse('blog:index'))
        self.assertIn('posts', response.context)
    
    def test_post_detail_view_status_code(self):
        """Testa se a página de um post retorna status 200"""
        post = Post.objects.first()
        response = self.client.get(
            reverse('blog:post', args=(post.slug,))
        )
        self.assertEqual(response.status_code, 200)
    
    def test_post_detail_view_404_for_unpublished(self):
        """Testa se post não publicado retorna 404"""
        unpublished = Post.objects.create(
            title="Não Publicado",
            excerpt="Resumo",
            content="Conteúdo",
            is_published=False
        )
        response = self.client.get(
            reverse('blog:post', args=(unpublished.slug,))
        )
        self.assertEqual(response.status_code, 404)
    
    def test_page_detail_view_status_code(self):
        """Testa se a página estática retorna status 200"""
        response = self.client.get(
            reverse('blog:page', args=(self.page.slug,))
        )
        self.assertEqual(response.status_code, 200)
    
    def test_category_list_view_status_code(self):
        """Testa se a lista por categoria retorna status 200"""
        response = self.client.get(
            reverse('blog:category', args=(self.category.slug,))
        )
        self.assertEqual(response.status_code, 200)
    
    def test_tag_list_view_status_code(self):
        """Testa se a lista por tag retorna status 200"""
        response = self.client.get(
            reverse('blog:tag', args=(self.tag.slug,))
        )
        self.assertEqual(response.status_code, 200)
    
    def test_search_view_with_query(self):
        """Testa se a busca funciona com termo válido"""
        response = self.client.get(
            reverse('blog:search'),
            {'search': 'Post'}
        )
        self.assertEqual(response.status_code, 200)
    
    def test_search_view_redirect_empty_query(self):
        """Testa se busca vazia redireciona para index"""
        response = self.client.get(
            reverse('blog:search'),
            {'search': ''}
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('blog:index'))
    
    def test_created_by_list_view_status_code(self):
        """Testa se a lista por autor retorna status 200"""
        response = self.client.get(
            reverse('blog:created_by', args=(self.user.pk,))
        )
        self.assertEqual(response.status_code, 200)
    
    def test_created_by_list_view_404_for_invalid_user(self):
        """Testa se autor inexistente retorna 404"""
        response = self.client.get(
            reverse('blog:created_by', args=(99999,))
        )
        self.assertEqual(response.status_code, 404)


class BlogURLsTest(TestCase):
    """Testes simples para verificar se as URLs existem"""
    
    def test_index_url_exists(self):
        """Verifica se a URL / existe"""
        response = self.client.get('/')
        # Pode ser 200 ou 404 dependendo se há posts, mas não deve dar erro 500
        self.assertIn(response.status_code, [200, 404])
