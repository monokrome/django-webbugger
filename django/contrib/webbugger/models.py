from datetime import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Beacon(models.Model):
    """A device that we can use to receive an entity from one source,
    and send it to a target of some sort."""

    # Generic values useful for beacons
    time_created = models.DateTimeField()

    # This is where our entity will be directred to
    target_type = models.ForeignKey(ContentType, related_name='target_beacons')
    target_id = models.PositiveIntegerField()
    target = generic.GenericForeignKey('target_type', 'target_id')

    # This is where we got our entity from
    source_type = models.ForeignKey(ContentType, related_name='source_beacons', null=True)
    source_id = models.PositiveIntegerField(blank=True, null=True)
    source = generic.GenericForeignKey('source_type', 'source_id')

    # Entity that is getting directed to our target
    entity_type = models.ForeignKey(ContentType, related_name='entity_beacons', null=True)
    entity_id = models.PositiveIntegerField(blank=True, null=True)
    entity = generic.GenericForeignKey('entity_type', 'entity_id')

    def save(self, force_insert=False, force_update=False, using=None):
        self.time_created = datetime.now()
        super(Beacon, self).save(force_insert, force_update, using)

    # This is used to get the target that we will be directed to
    def get_absolute_url(self):
        if self.target is not None:
            if hasattr(self.target, 'get_beacon_url'):
                return self.target.get_beacon_url()
            else:
                return self.target.get_absolute_url()

    def __unicode__(self):
        return '#%s' % self.pk

class IP(models.Model):
    """ A very basic model for storing an IP address, and the time
    at which it was owned by our beacon's entity. """
    class Meta(object):
        verbose_name = 'IP'

    # IPv6 addresses are pretty damn long...
    address= models.CharField(max_length=72)
    owned_time = models.DateTimeField()

    def save(self, force_insert=False, force_update=False, using=None):
        self.owned_time = datetime.now()
        super(IP, self).save(force_insert, force_update, using)

    def __unicode__(self):
        return self.address

class IPEntity(models.Model):
    """ A generic entity that does nothing except for storing IP addresses for
    a given beacon. Multiple IPs are accepted in case we are passed an existing
    entity ID to the trigger view. This allows web bugging to be more efficient
    when the entity uses our link multiple times, if required. """
    class Meta(object):
        verbose_name = 'IP entity'
        verbose_name_plural = 'IP entities'

    ip_addresses = models.ManyToManyField(IP, related_name='entities', null=True)

    # Entities need an update method that accepts the request passed to it
    def beacon_update(self, request):
        ip_address = address=request.META.get('REMOTE_ADDR')
        next_ip, created = IP.objects.get_or_create(address=ip_address)

        self.ip_addresses.add(next_ip)

    def __unicode__(self):
        return '%s IP addresses' % len(self.ip_addresses.all())


### This is a target that can be used for testing purposes:

# class DemoTarget(models.Model):
#     """ This is a target that should only be used for demonstration purposes. It
#     simply sets our target to Google."""
#     def get_absolute_url(self):
#         return 'http://google.com/'

#     def __unicode__(self):
#         return 'http://google.com/'

#     # get_beacon_url is used to decide where to go. get_absolute_url is
#     # used when get_beacon_url doesn't exist.
#     get_beacon_url = get_absolute_url


