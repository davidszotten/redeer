import datetime
import time
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from reeder.feeds.models import Group, Feed


def to_timestamp(dt):
    return int(time.mktime(dt.timetuple()))


def last_refreshed():
    return to_timestamp(datetime.datetime.now())


def json_response(data):
    return HttpResponse(json.dumps(data))


@csrf_exempt
def index(request):

    response = {
        "api_version": 3,
        "auth": 1,
        "last_refreshed_on_time": last_refreshed(),
    }

    if 'groups' in request.GET:
        groups = [group.to_dict() for group in Group.objects.all()]
        response['groups'] = groups

    if 'feeds' in request.GET:
        groups = Group.objects.all()
        # feeds = [group.to_dict() for group in groups]
        feeds = [feed.to_dict() for feed in Feed.objects.all()]
        feeds_groups = [group.to_feedgroup_dict() for group in groups]
        response['feeds'] = feeds
        response['feeds_groups'] = feeds_groups

    if 'links' in request.GET:
        # not supported
        response['links'] = []

    if 'items' in request.GET:
        response['items'] = []

    print
    print
    print request.GET
    print request.POST
    print "returning"
    import pprint
    pprint.pprint(response)

    return json_response(response)
