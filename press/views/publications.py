# -*- coding: utf-8 -*-
from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='publications', request_method='POST')
def publish(request):
    """Publish the contents of a litezip payload."""
    return Response('Recieved', status_code=202)
