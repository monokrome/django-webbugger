from models import Beacon
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import resolve
from django.conf import settings
import base64

# This is the string that gets returned as a transparent gif.
transparent_gif_contents = 'R0lGODlhAQABAPcAAAAAAAAAMwAAZgAAmQAAzAAA/wAzAAAzMwAzZgAzmQAzzAAz/wBmAABmMwBm\nZgBmmQBmzABm/wCZAACZMwCZZgCZmQCZzACZ/wDMAADMMwDMZgDMmQDMzADM/wD/AAD/MwD/ZgD/\nmQD/zAD//zMAADMAMzMAZjMAmTMAzDMA/zMzADMzMzMzZjMzmTMzzDMz/zNmADNmMzNmZjNmmTNm\nzDNm/zOZADOZMzOZZjOZmTOZzDOZ/zPMADPMMzPMZjPMmTPMzDPM/zP/ADP/MzP/ZjP/mTP/zDP/\n/2YAAGYAM2YAZmYAmWYAzGYA/2YzAGYzM2YzZmYzmWYzzGYz/2ZmAGZmM2ZmZmZmmWZmzGZm/2aZ\nAGaZM2aZZmaZmWaZzGaZ/2bMAGbMM2bMZmbMmWbMzGbM/2b/AGb/M2b/Zmb/mWb/zGb//5kAAJkA\nM5kAZpkAmZkAzJkA/5kzAJkzM5kzZpkzmZkzzJkz/5lmAJlmM5lmZplmmZlmzJlm/5mZAJmZM5mZ\nZpmZmZmZzJmZ/5nMAJnMM5nMZpnMmZnMzJnM/5n/AJn/M5n/Zpn/mZn/zJn//8wAAMwAM8wAZswA\nmcwAzMwA/8wzAMwzM8wzZswzmcwzzMwz/8xmAMxmM8xmZsxmmcxmzMxm/8yZAMyZM8yZZsyZmcyZ\nzMyZ/8zMAMzMM8zMZszMmczMzMzM/8z/AMz/M8z/Zsz/mcz/zMz///8AAP8AM/8AZv8Amf8AzP8A\n//8zAP8zM/8zZv8zmf8zzP8z//9mAP9mM/9mZv9mmf9mzP9m//+ZAP+ZM/+ZZv+Zmf+ZzP+Z///M\nAP/MM//MZv/Mmf/MzP/M////AP//M///Zv//mf//zP///////wAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAANgALAAAAAABAAEA\nAAgEALEFBAA7\n'

def trigger(request, target_type, target_id, source_type=None, source_id=None, 
    entity_type=None, entity_id=None, ignore_errors=False, pixel=False):
    """ Takes a set of beaconing criteria and creates a beacon from the current
    request. """

    target = None
    entity = None
    beacon = None
    source = None

    if pixel == False and (target_type is not None and target_id is not None):
        target = get_object_or_404(target_type, pk=target_id)

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
    beacon_arguments = {}

    # If we need to supply a target for this tracking instance, supply it.
    if target is not None:
        beacon_arguments.update({
            'target_type': ContentType.objects.get_for_model(target_type),
            'target_id': target.pk,
        })

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
        if pixel:
            return HttpResponse(base64.decodestring(transparent_gif_contents), mimetype='image/gif')
        else:
            beacon_final_url = beacon.get_absolute_url()

            # This will attempt to detect whether or not this URL is part of the current system.
            # If it is part of the current system, we don't need to redirect at all :)
            if getattr(settings, 'IGNORE_LOCAL_REDIRECTS', True):
                resolve_match = resolve(beacon_final_url)

                if resolve_match:
                    return resolve_match.func(request, *match.args, **match.kwargs)

            return HttpResponseRedirect(beacon_final_url)
    except:
        try:
            # Attempt to redirect to the target if the beacon had issues
            return HttpResponseRedirect(target.get_absolute_url())
        except:
            # We can't ignore this error, because we have no valid target
            raise Http404('The specified target was not found.')

