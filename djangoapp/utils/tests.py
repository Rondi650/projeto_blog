import os
import tempfile
import shutil
from pathlib import Path
from PIL import Image
from django.test import TestCase
from django.core.exceptions import ValidationError
from utils.images import resize_image
from utils.model_validators import validate_png


class ResizeImageTest(TestCase):
    def test_resize_image_reduces_width_when_larger(self):
        media_root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, str(media_root))

        img = Image.new('RGB', (1600, 1200), color='red')
        file_path = media_root / 'test-large.jpg'
        img.save(file_path)

        class FakeFieldFile:
            name = 'test-large.jpg'

        with self.settings(MEDIA_ROOT=media_root):
            resize_image(FakeFieldFile(), new_width=800)

        resized = Image.open(file_path)
        self.assertEqual(resized.width, 800)
        self.assertEqual(resized.height, 600)
        resized.close()

    def test_resize_image_does_not_enlarge_small_image(self):
        media_root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, str(media_root))

        img = Image.new('RGB', (400, 300), color='blue')
        file_path = media_root / 'test-small.jpg'
        img.save(file_path)

        class FakeFieldFile:
            name = 'test-small.jpg'

        with self.settings(MEDIA_ROOT=media_root):
            resize_image(FakeFieldFile(), new_width=800)

        resized = Image.open(file_path)
        self.assertEqual(resized.width, 400)
        self.assertEqual(resized.height, 300)
        resized.close()


class ValidatePNGTest(TestCase):
    def test_png_extension_passes(self):
        class FakeImage:
            name = 'favicon.png'
        validate_png(FakeImage())

    def test_non_png_raises_validation_error(self):
        class FakeImage:
            name = 'favicon.jpg'
        with self.assertRaises(ValidationError):
            validate_png(FakeImage())
