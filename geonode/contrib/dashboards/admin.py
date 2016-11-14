from django.contrib import admin

from guardian.admin import GuardedModelAdmin

from geonode.contrib.dashboards.models import GeoDashDashboard

class GeoDashDashboardAdmin(GuardedModelAdmin):
    model = GeoDashDashboard
    list_display_links = ('id', 'title',)
    list_display = ('id', 'title', 'slug',)

admin.site.register(GeoDashDashboard, GeoDashDashboardAdmin)
