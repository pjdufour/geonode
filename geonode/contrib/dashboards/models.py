from django.db import models

from geonode.base.models import ResourceBase
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse


#class GeoDashDashboard(models.Model):
#    title = models.CharField(max_length=255, null=True, blank=True)
#    slug = models.CharField(max_length=255, null=True, blank=True)
#    config = models.TextField(null=True, blank=True)
#    advertised = models.BooleanField()
#    published = models.BooleanField()

#    def __str__(self):
#        return "%s" % self.title.encode('utf-8')

#    class Meta:
#        ordering = ("title",)
#        verbose_name = ("GeoDash Dashboard")
#        verbose_name_plural = ("GeoDash Dashboards")
#        permissions = (
#            ('view_geodashdashboard', 'View GeoDash Dashboard'),
            # ('add_geodashdashboard', 'Add GeoDash Dashboard'),
            # ('change_geodashdashboard', 'Change GeoDash Dashboard'),
            # ('delete_geodashdashboard', 'Delete GeoDash Dashboard'),
#        )


class Dashboard(ResourceBase):

    """
    A dashboard is a customized view of map data.
    """

    # Relation to the resource model
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    resource = generic.GenericForeignKey('content_type', 'object_id')

    # Dashboard specific fields
    slug = models.CharField(max_length=255, null=True, blank=True)
    config = models.TextField(null=True, blank=True)
    advertised = models.BooleanField()
    published = models.BooleanField()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('document_detail', args=(self.id,))

    @property
    def name_long(self):
        if not self.title:
            return str(self.id)
        else:
            return '%s (%s)' % (self.title, self.id)

    def _render_thumbnail(self):
        return None

    @property
    def class_name(self):
        return self.__class__.__name__

    class Meta(ResourceBase.Meta):
        ordering = ("title",)
        verbose_name = ("Dashboard")
        verbose_name_plural = ("Dashboards")
        permissions = (
            ('view_dashboard', 'View Dashboard'),
            # ('add_geodashdashboard', 'Add GeoDash Dashboard'),
            # ('change_geodashdashboard', 'Change GeoDash Dashboard'),
            # ('delete_geodashdashboard', 'Delete GeoDash Dashboard'),
        )


    #title = models.CharField(max_length=255, null=True, blank=True)
    #slug = models.CharField(max_length=255, null=True, blank=True)
    #config = models.TextField(null=True, blank=True)
    #advertised = models.BooleanField()
    #published = models.BooleanField()

    #def __str__(self):
    #    return "%s" % self.title.encode('utf-8')

    #class Meta:
    #    ordering = ("title",)
    #    verbose_name = ("GeoDash Dashboard")
    #    verbose_name_plural = ("GeoDash Dashboards")
    #    permissions = (
    #        ('view_geodashdashboard', 'View GeoDash Dashboard'),
            # ('add_geodashdashboard', 'Add GeoDash Dashboard'),
            # ('change_geodashdashboard', 'Change GeoDash Dashboard'),
            # ('delete_geodashdashboard', 'Delete GeoDash Dashboard'),
    #    )
