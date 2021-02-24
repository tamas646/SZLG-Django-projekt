from django.contrib import admin
from koxapp.models import Felhasznalo, Bevitel, MozgasTipus, Mozgas, Etel

# Register your models here.

admin.site.register(Felhasznalo)
admin.site.register(Bevitel)
admin.site.register(MozgasTipus)
admin.site.register(Mozgas)
admin.site.register(Etel)
