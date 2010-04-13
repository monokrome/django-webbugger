from models import Beacon
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect

def trigger(request, target_type, target_id, source_type=None, source_id=None, 
    entity_type=None, entity_id=None, ignore_errors=False):
    """ Takes a set of beaconing criteria and creates a beacon from the current
    request. """

    target = get_object_or_404(target_type, pk=target_id)

    entity = None
    beacon = None
    source = None

    # If we were passed a valid beacon source, we need to make use of it.
    if source_type is not None and source_id is not None:
        try:
            source = source_type.objects.get(pk=source_id)
        except:
            if ignore_errors is False:
                raise Http404('The specified source could not be retreived.')

    # If we were asked to use an entity, do that too.
    if entity_type is not None:
        # The system attempts to use preexisting entities when possible
        if entity_id is not None:
            entity, created = entity_type.objects.get_or_create(pk=entity_id)
        else:
            entity = entity_type()

        # TODO: Find a better name for beacon_update. update is too generic.
        if hasattr(entity, 'beacon_update') and callable(entity.beacon_update):
            entity.beacon_update(request)

        entity.save()

    # Generate an argument list for unpacking into our class constructor later
    beacon_arguments = {
        'target_type': ContentType.objects.get_for_model(target_type),
        'target_id': target.pk,
    }

    # Sometimes people want a bug and they don't need to link it to a source.
    if source is not None:
        beacon_arguments.update({
            'source_type': ContentType.objects.get_for_model(source_type),
            'source_id': source.pk,
        })

    # Sometimes a more descript entity isn't needed to webbug our entity
    if entity is not None:
        beacon_arguments.update({
            'entity_type': ContentType.objects.get_for_model(entity_type),
            'entity_id': entity.pk,
        })

    try:
        beacon = Beacon(**beacon_arguments)
        beacon.save()
    except:
        if ignore_errors is False:
            raise Http404('The requested beacon could not be created.')

    try:
        return HttpResponseRedirect(beacon.get_absolute_url())
    except:
        try:
            # Attempt to redirect to the target if the beacon had issues
            return HttpResponseRedirect(target.get_absolute_url())
        except:
            # We can't ignore this error, because we have no valid target
            raise Http404('The specified target was not found.')

