from django.conf.urls.defaults import *
from models import IPEntity
# from YOUR_TARGET_MODELS import YOUR_TARGET_MODEL as YourTarget

####
# In order to use the demo URLs, you need to import something that has
# implemented the standard get_absolute_url(), or get_beacon_url(). To
# use these exact URLs you will import the model as YourTarget. An example
# line is included above to show you how to import this properly.
#
# It is best that you simply learn how the URLs are set up so that you can
# write your own URLs with your own models for the beacons.
#
# A target chooses where an entity is redirected. Usually, a client is
# an entity - however this isn't completely "enforced" by the library.
####

urlpatterns = patterns('django_webbugger.views',
    # Receives a target ID
    url(r'^(?P<target_id>\d+)/$', 'trigger',
        {'target_type': YourTarget},
        name='webbugger_beacon_trigger'
    ),

    # Receives a target, and a possibly pre-existing entity ID.
    url(r'^(?P<target_id>\d+)/e(?P<entity_id>\d+)/$', 'trigger',
        {
            'target_type': YourTarget,
            'entity_type': IPEntity,
        },
        name='webbugger_beacon_trigger'
    ),
)

#### YOU CAN USE THESE FORMATS IF YOU NEED TO PASS A "SOURCE".
#### I use marketing "campaigns" as sources. You could also used
#### affiliates or something completely different.

# Receives a target, and source ID.
#    url(r'^(?P<target_id>\d+)/s(?P<source_id>\d+)/$', 'trigger',
#        {
#            'target_type': DemoTarget,
#            'source_type': YourSource,
#        },
#        name='webbugger_beacon_trigger'
#    ),

# Receives a target, source, and entity ID.
#    url(r'^(?P<target_id>\d+)/(?P<source_id>\d+)/(?P<entity_id>\d+)/$',
#        'trigger',
#        {
#            'target_type': DemoTarget,
#            'source_type': YourSource,
#            'entity_type': IPEntity
#        },
#        name='webbugger_beacon_trigger'
#    ),

