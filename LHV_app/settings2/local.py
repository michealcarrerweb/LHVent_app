from .base import *

DEBUG = env.bool('DJANGO_DEBUG', default=True)

SECRET_KEY = env('DJANGO_SECRET_KEY', default="hyv*5n&9v&1xql7i7()e+(w5b#07aogy_t6uh#evuhni%xi(@o")