import django
from django.core.management.utils import get_random_secret_key as keygen
key = keygen()
print("New secret: {}".format(key))
