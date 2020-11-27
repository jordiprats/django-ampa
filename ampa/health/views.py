from django.http import HttpResponse

def liveness(request):
    return HttpResponse("OK")

def readiness(request):
    # TODO
    return HttpResponse("OK")
