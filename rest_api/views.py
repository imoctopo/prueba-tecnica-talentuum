from django.db.models import Count
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ParseError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Event, Actor
from .serializers import EventSerializer, ActorSerializer, RepoSerializer, ActorUpdateSerializer


class EventViewSet(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Event.objects.all().order_by('id')
    serializer_class = EventSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ActorSerializer(data=request.data.get('actor', None)).is_valid(raise_exception=True)
        RepoSerializer(data=request.data.get('repo', None)).is_valid(raise_exception=True)

        if self.get_queryset().filter(pk=serializer.validated_data['id']):
            raise ParseError(detail='An event with the same ID already exists.')

        event = serializer.save()
        return Response(self.get_serializer(event).data, status=status.HTTP_201_CREATED)

    @action(detail=False, url_path='actors/(?P<actor_pk>[^/.]+)', methods=['GET'])
    def actors(self, request, actor_pk):
        get_object_or_404(Actor, pk=actor_pk)
        events = Event.objects.filter(actor_id=actor_pk)
        return Response(self.get_serializer(events, many=True).data)


@api_view(['DELETE'])
def delete(request):
    Event.objects.all().delete()
    return Response()


class ActorAPIViewSet(viewsets.GenericViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def list(self, request):
        actors = self.get_queryset().annotate(total_events=Count('events'))
        actors = actors.order_by('-total_events', '-events__created_at', 'login')
        return Response(self.get_serializer(actors, many=True).data)

    def update(self, request, pk=None):
        actor = get_object_or_404(Actor, pk=pk)

        if 'avatar_url' in request.data and len(request.data) > 1:
            raise ParseError(detail='You can only update avatar_url field.')

        serializer = ActorUpdateSerializer(actor, data=request.data)
        serializer.is_valid(raise_exception=True)
        actor = serializer.save()
        return Response(self.get_serializer(actor).data)
