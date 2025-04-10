from django.shortcuts import render
from .route import makeroute


def home(request):
    return render(request, 'base.html')


# Показ маршрута
def showroute(request):
    data = request.POST
    figure = makeroute(data)
    context = {
        'map': figure._repr_html_()
        }
    return render(request, 'showroute.html', context)
