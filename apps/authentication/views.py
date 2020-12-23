from django.contrib import messages
from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from rest_framework import viewsets, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from .helpers import sign_up_confirm_account_token

from .serializers import SignUpSerializer
from .tasks import task_send_account_confirmation_email


class SignUpGenericGenericViewSet(mixins.RetrieveModelMixin,
                                  mixins.ListModelMixin,
                                  viewsets.GenericViewSet):
    serializer_class = SignUpSerializer
    queryset = User.objects.all()

    @atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        task_send_account_confirmation_email.delay(user_id=user.id)
        return Response({
            'user': self.get_serializer(user).data,
            'message': 'Usuario creado correctamente. Por favor revise su email para activar su cuenta.'
        }, status=status.HTTP_201_CREATED)


def change_password(request):
    # Get uid (user id) and token
    uid = request.GET.get('uid') if request.method == 'GET' else request.POST.get('uid')
    token = request.GET.get('token') if request.method == 'GET' else request.POST.get('token')

    # GET
    if request.method == 'GET':
        # If there aren't uid or token, return an error
        if not uid or not token:
            return HttpResponse('No se entregó el token de confirmación.')
        return render(request, 'authentication/change_password.html', {
            'uid': uid,
            'token': token
        })

    # POST
    pk = force_bytes(urlsafe_base64_decode(uid))
    user = get_object_or_404(User, pk=pk)

    # Check if token is valid
    if sign_up_confirm_account_token.check_token(user, token):
        user.is_active = True
        user.set_password(request.POST.get('password'))
        user.save()
        messages.success(request, 'Cuenta creada correctamente.')
    else:
        messages.error(request, 'El token no es válido.')
    return render(request, 'authentication/change_password.html', {
        'uid': uid,
        'token': token
    })
