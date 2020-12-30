from rest_framework import serializers
from .models import Event, Actor, Repo


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'read_only': False
            }
        }

    def validate(self, attrs):
        actor = Actor.objects.filter(login=attrs['login']).first()
        if actor and actor.id != attrs['id']:
            raise serializers.ValidationError({'actor': {'login': 'Login name already taken.'}})
        return attrs


class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'read_only': False
            }
        }


class EventSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(required=True)
    repo = RepoSerializer(required=True)

    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'read_only': False
            }
        }

    def create(self, validated_data):
        actor = validated_data.pop('actor', None)
        actor = Actor.objects.filter(pk=actor['id']).first() or Actor.objects.create(**actor)

        repo = validated_data.pop('repo', None)
        repo = Repo.objects.filter(pk=repo['id']).first() or Repo.objects.create(**repo)

        return Event.objects.create(actor=actor, repo=repo, **validated_data)


class ActorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'avatar_url']
