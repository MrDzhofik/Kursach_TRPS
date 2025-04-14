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
    sights_name = []
    sights, figure = makeroute(data)
    for sight in sights:
        sights_name.append(sight[0])
    context = {
        'sights': sights_name,
        'map': figure._repr_html_()
        }
    return render(request, 'showroute.html', context)
