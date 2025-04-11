from django.shortcuts import render
from .route import makeroute
from .forms import IntForm
from django.views.decorators.csrf import csrf_exempt


def home(request):
    form = IntForm()
    return render(request, 'form.html', context={
        "form": form
    })


# Показ маршрута
@csrf_exempt
def showroute(request):
    data = request.POST
    figure = makeroute(data)
    context = {
        'map': figure._repr_html_()
        }
    return render(request, 'showroute.html', context)
