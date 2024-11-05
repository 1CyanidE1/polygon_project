from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
import json

from .models import PolygonModel
from .serializers import PolygonSerializer


class PolygonView(TemplateView):
    template_name = 'polygon_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['polygons'] = PolygonModel.objects.all()
        return context


class PolygonViewSet(viewsets.ModelViewSet):
    queryset = PolygonModel.objects.all()
    serializer_class = PolygonSerializer

@csrf_exempt
def save_polygon(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        polygon = PolygonModel(
            name=data['name'],
            polygon=data['polygon']
        )
        polygon.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
