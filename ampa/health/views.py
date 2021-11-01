from django.db.utils import OperationalError
from django.http import HttpResponse
from django.db import connections

def liveness(request):
    return HttpResponse("OK")

def readiness(request):
    db_conn = connections['default']
    try:
        c = db_conn.cursor()
    except OperationalError:
        return HttpResponse("please check DB", status=500)
    else:
        return HttpResponse("OK")

def startup(request):
    db_conn = connections['default']
    try:
        c = db_conn.cursor()
    except OperationalError:
        return HttpResponse("please check DB", status=500)
    else:
        return HttpResponse("OK")