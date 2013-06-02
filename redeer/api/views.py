import datetime
import time
import json

from django.db.models import Max
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from redeer.api.forms import MarkForm
from redeer.api.models import ApiKey
from redeer.feeds.models import Group, Feed, Item, to_comma_separated


def to_timestamp(dt):
    return int(time.mktime(dt.timetuple()))


def last_refreshed():
    return to_timestamp(datetime.datetime.now())


def json_response(data):
    return HttpResponse(json.dumps(data))


def get_int(string):
    try:
        return int(string)
    except (ValueError, TypeError):
        return 0


def get_list(string):
    return [get_int(s) for s in string.split(',')]


@csrf_exempt
def api(request):
    # print 'GET', request.GET
    # print 'POST', request.POST
    api_key = request.POST.get('api_key')
    try:
        user = ApiKey.objects.get(md5=api_key).user
    except ApiKey.DoesNotExist:
        return HttpResponseForbidden("Invalid API key")

    last_refreshed = Feed.objects.for_user(user).aggregate(
        updated=Max('last_updated'))['updated']

    response = {
        "api_version": 3,
        "auth": 1,
        "last_refreshed_on_time": last_refreshed,
    }

    if 'groups' in request.GET:
        groups = [group.to_dict() for group in Group.objects.for_user(user)]
        response['groups'] = groups

    if 'feeds' in request.GET:
        feeds = [feed.to_dict() for feed in Feed.objects.for_user(user)]
        feeds_groups = [group.to_feedgroup_dict()
            for group in Group.objects.for_user(user)]
        response['feeds'] = feeds
        response['feeds_groups'] = feeds_groups

    if 'links' in request.GET:
        # not supported
        response['links'] = []

    if 'items' in request.GET:
        items = []
        if 'since_id' in request.GET:
            since_id = get_int(request.GET['since_id'])
            items = Item.objects.for_user(user).filter(
                pk__gt=since_id).order_by('pk')[:50]

        elif 'max_id' in request.GET:
            max_id = get_int(request.GET['max_id'])
            items = Item.objects.for_user(user).filter(
                pk__lt=max_id).order_by('-pk')[:50]

        elif 'with_ids' in request.GET:
            ids = get_list(request.GET['with_ids'])
            items = Item.objects.for_user(user).filter(pk__in=ids)

        response['items'] = [item.to_dict() for item in items]

    if 'unread_item_ids' in request.GET:
        response['unread_item_ids'] = to_comma_separated(
            Item.objects.for_user(user).filter(
                is_read=False).values_list('pk', flat=True))

    mark_form = MarkForm(request.POST or None)
    mark_form.do_action()

    # print "returning"
    # import pprint
    # pprint.pprint(response)

    return json_response(response)
