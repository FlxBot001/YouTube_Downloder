from django.http import JsonResponse
from django.core.cache import cache
from health_check.views import MainView
from rest_framework.decorators import action
from sentry_sdk import capture_exception
from rest_framework import viewsets
from .models import YourModel
from .serializers import YourModelSerializer


class HealthCheckView(MainView):
    def get(self, request, *args, **kwargs):
        status = super().get(request, *args, **kwargs)
        return JsonResponse({'status': 'healthy' if status.status_code == 200 else 'unhealthy'})

class DownloadViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        try:
            # Cache check for duplicate downloads
            cache_key = f"download_{request.data.get('url')}_{request.data.get('format_id')}"
            if cache.get(cache_key):
                return Response({'error': 'Duplicate download request'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
            # Set cache to prevent duplicate downloads
            cache.set(cache_key, True, timeout=60)
            
            return super().create(request, *args, **kwargs)
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def video_info(self, request):
        try:
            url = request.query_params.get('url')
            cache_key = f"video_info_{url}"
            
            # Try to get cached info
            cached_info = cache.get(cache_key)
            if cached_info:
                return Response(cached_info)
            
            # If not cached, fetch and cache the info
            info = self._fetch_video_info(url)
            cache.set(cache_key, info, timeout=3600)  # Cache for 1 hour
            
            return Response(info)
        except Exception as e:
            capture_exception(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)