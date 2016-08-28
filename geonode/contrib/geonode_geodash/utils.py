from geonode.people.models import Profile


def expand_users(request, map_obj):
    users = []
    if request.user.has_perm("change_geodashdashboard", map_obj):
        users =[{'id': x.username, 'text': x.username} for x in Profile.objects.exclude(username='AnonymousUser')]
    return users
