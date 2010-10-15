from django.contrib import admin
from models import Beacon, IPEntity, IP

class BeaconAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'target', 'entity')

admin.site.register(Beacon, BeaconAdmin)
admin.site.register(IPEntity)
admin.site.register(IP)

