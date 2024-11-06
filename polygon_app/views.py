from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status
from rest_framework.response import Response
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

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return response
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@csrf_exempt
def save_polygon(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            serializer = PolygonSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'errors': serializer.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
