from django.utils.text import slugify


# generating random character
import string
import random
def generate_random_string(n):
    res=''.join(random.choices(string.ascii_uppercase + string.digits,k=n))
    return res
def generate_slug(text):
    from blogApp.models import Post
    new_slug=slugify(text)
    if Post.objects.filter(slug=new_slug).first():
        return generate_slug(text + generate_random_string(5))
    return new_slug