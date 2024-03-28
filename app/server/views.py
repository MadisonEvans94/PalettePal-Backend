from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from django.shortcuts import render

import logging
logger = logging.getLogger(__name__)

def home(request):
    logger.info('Home view has been requested.')
    try:
        # Your logic here
        return HttpResponse(status=200, content="welcome to the palette pal api")
    except Exception as e:
        logger.error(f'An error occurred: {e}')
        return HttpResponse(status=500, content="uh oh")
