# Create your views here.
from django.http import HttpResponse


def is_logged_in(request):
    print(request.GET)
    print(request.POST)
    return HttpResponse("Hello, world. You're at the polls index.")
