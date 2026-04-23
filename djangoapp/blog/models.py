from tabnanny import verbose

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
