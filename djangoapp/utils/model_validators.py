from django.core.exceptions import ValidationError
from django.db.models import ImageField


def validate_png(image: ImageField):
    
    # Para debug
    print("-"*50,"\n","FAVICON VALIDATION", sep="")
    print(f'Validating image: {image}')
    for chave, valor in image.__dict__.items():
        print(chave, ": " ,valor)
    print("-"*50)
    
    if not image.name.lower().endswith('.png'):
        raise ValidationError('Imagem precisa ser PNG.')