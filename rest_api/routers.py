from django.urls import path
from rest_framework import routers
from .views import EventViewSet, ActorAPIViewSet, delete

app_name = 'api-rest'
router = routers.SimpleRouter(trailing_slash=False)
router.register(r'events', EventViewSet, basename='events')
router.register(r'actors', ActorAPIViewSet, basename='actors')

urlpatterns = router.urls + [
    path('erase', delete)
]
