from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import EBForm
from .serializers import EBFormSerializer


class EBFormAPIView(generics.CreateAPIView):
    serializer_class = EBFormSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        ebform = EBForm.objects.create(
            full_name=request.data['full_name'],
            phone_number=request.data['phone_number'],
            email=request.data['email'],
            org=request.data['org'],
            permanent_address=request.data['permanent_address'],
            exp_eb=request.data['exp_eb'],
            exp_delegate=request.data['exp_delegate'],
            preferred_comm=request.data['preferred_comm']
        )
        ebform.save()

        return Response({"message": "Form Filled Successfully!"}, status=status.HTTP_201_CREATED)
