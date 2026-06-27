import io
from PIL import Image
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from site_setup.models import SiteSetup, MenuLink


class SiteSetupModelTest(TestCase):
    def test_str_returns_title(self):
        setup = SiteSetup.objects.create(
            title='Meu Site', description='Descrição'
        )
        self.assertEqual(str(setup), 'Meu Site')

    def test_save_without_favicon(self):
        setup = SiteSetup(title='Site', description='Desc')
        setup.save()
        self.assertIsNotNone(setup.pk)

    def test_save_with_favicon(self):
        img = Image.new('RGB', (32, 32), color='blue')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        favicon = SimpleUploadedFile(
            'favicon.png', buf.getvalue(), content_type='image/png'
        )
        setup = SiteSetup(
            title='Site', description='Desc', favicon=favicon
        )
        setup.save()
        self.assertIsNotNone(setup.pk)
        self.assertIn('favicon', setup.favicon.name)

    def test_menulink_str_returns_text(self):
        setup = SiteSetup.objects.create(
            title='Site', description='Desc'
        )
        link = MenuLink.objects.create(
            text='Home', url_or_path='/', site_setup=setup
        )
        self.assertEqual(str(link), 'Home')


class SiteSetupAdminTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username='admin', password='adminpass', email='admin@example.com'
        )
        self.client.force_login(self.superuser)

    def test_has_add_permission_returns_false_when_setup_exists(self):
        SiteSetup.objects.create(title='Setup', description='Desc')
        response = self.client.get(
            reverse('admin:site_setup_sitesetup_add')
        )
        self.assertEqual(response.status_code, 403)

    def test_has_add_permission_returns_true_when_no_setup(self):
        response = self.client.get(
            reverse('admin:site_setup_sitesetup_add')
        )
        self.assertEqual(response.status_code, 200)
