import random
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.authentication.serializers import UserSerializer


@api_view(['GET'])
def launch_giveaway(request):
    users_id = [user['id'] for user in User.objects.values('id')]
    winner_pk = random.choice(users_id)
    return Response({
        'winner': UserSerializer(User.objects.get(pk=winner_pk)).data
    })
