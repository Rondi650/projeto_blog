import io
from PIL import Image
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from blog.models import Tag, Category, Page, Post, PostAttachment


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

    def test_get_absolute_url_for_unpublished_post(self):
        post = Post(
            title='Rascunho', slug='rascunho',
            excerpt='Resumo', content='Conteúdo',
            is_published=False
        )
        url = post.get_absolute_url()
        self.assertEqual(url, reverse('blog:index'))

    def test_post_save_with_cover(self):
        img = Image.new('RGB', (100, 100), color='red')
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        cover = SimpleUploadedFile(
            'test-cover.jpg', buf.getvalue(), content_type='image/jpeg'
        )
        post = Post(
            title='Cover Post', excerpt='Resumo',
            content='Conteúdo', cover=cover
        )
        post.save()
        self.assertIsNotNone(post.pk)
        self.assertIn('test-cover', post.cover.name)


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

    def test_created_by_list_view_shows_full_name_when_user_has_first_name(self):
        user = User.objects.create_user(
            username='joao', password='testpass123',
            first_name='João', last_name='Silva'
        )
        Post.objects.create(
            title='Post do João', excerpt='Resumo',
            content='Conteúdo', is_published=True,
            created_by=user
        )
        response = self.client.get(
            reverse('blog:created_by', args=(user.pk,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('João Silva', response.context['page_title'])


class BlogURLsTest(TestCase):
    """Testes simples para verificar se as URLs existem"""

    def test_index_url_exists(self):
        """Verifica se a URL / existe"""
        response = self.client.get('/')
        # Pode ser 200 ou 404 dependendo se há posts, mas não deve dar erro 500
        self.assertIn(response.status_code, [200, 404])


class PostAdminTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username='admin', password='adminpass', email='admin@example.com'
        )
        self.client.force_login(self.superuser)
        self.category = Category.objects.create(name='Teste')

    def test_link_returns_dash_for_post_without_pk(self):
        from django.contrib.admin import site as admin_site
        from blog.admin import PostAdmin
        post_admin = PostAdmin(model=Post, admin_site=admin_site)
        result = post_admin.link(Post())
        self.assertEqual(result, '-')

    def test_link_returns_link_for_existing_post(self):
        post = Post.objects.create(
            title='Test Post', slug='test-post',
            excerpt='Resumo', content='Conteúdo',
            is_published=True, created_by=self.superuser,
            category=self.category
        )
        response = self.client.get(
            reverse('admin:blog_post_change', args=(post.pk,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ver post')

    def test_admin_create_post_sets_created_by(self):
        post_data = {
            'title': 'Admin Post',
            'slug': 'admin-post',
            'excerpt': 'Resumo',
            'content': 'Conteúdo',
            'is_published': True,
            'category': self.category.pk,
            '_save': 'Save',
        }
        response = self.client.post(
            reverse('admin:blog_post_add'), post_data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        post = Post.objects.get(slug='admin-post')
        self.assertEqual(post.created_by, self.superuser)

    def test_admin_update_post_sets_updated_by(self):
        post = Post.objects.create(
            title='Original', slug='original',
            excerpt='Resumo', content='Conteúdo',
            created_by=self.superuser, category=self.category
        )
        post_data = {
            'title': 'Updated',
            'slug': 'original',
            'excerpt': 'Updated excerpt',
            'content': 'Updated content',
            'is_published': True,
            'category': self.category.pk,
            '_save': 'Save',
        }
        response = self.client.post(
            reverse('admin:blog_post_change', args=(post.pk,)),
            post_data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        post.refresh_from_db()
        self.assertEqual(post.updated_by, self.superuser)


class PostAttachmentTest(TestCase):
    def test_save_sets_name_from_file_when_name_not_set(self):
        img = Image.new('RGB', (100, 100), color='red')
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        attachment = PostAttachment()
        attachment.file = SimpleUploadedFile(
            'attached.jpg', buf.getvalue(), content_type='image/jpeg'
        )
        attachment.save()
        self.assertIsNotNone(attachment.pk)
        self.assertTrue(attachment.name.endswith('attached.jpg'))


class ProjectURLsTest(TestCase):
    def test_debug_mode_includes_static_and_media_urls(self):
        from django.conf import settings
        if settings.DEBUG:
            from project.urls import urlpatterns
            self.assertEqual(len(urlpatterns), 5)
