from utils.rands import slugify_new

from django.db import models

# Create your models here.


class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,
                            unique=True,
                            default=None,
                            null=True,
                            blank=True,)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new((self.name))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,
                            unique=True,
                            default=None,
                            null=True,
                            blank=True,)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Page(models.Model):
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,
                            unique=True,
                            default=None,
                            null=True,
                            blank=True,)
    is_published = models.BooleanField(
        default=False,
        help_text='Indica se a página está publicada ou não.',
    )
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
