from rest_framework import generics
from rest_framework.response import Response

from .serializers import SignUpSerializer


class SignUpGenericAPIView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': self.get_serializer(user).data,
            'message': 'Usuario creado correctamente. Por favor revise su email para activar su cuenta.'
        })
