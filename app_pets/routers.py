from rest_framework.routers import DefaultRouter, Route


class MyRouter(DefaultRouter):

    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create',
                'delete': 'destroy_list'
            },
            name='{basename}-list',
            initkwargs={'suffix': 'List'},
            detail=False,
        ),
    ]
