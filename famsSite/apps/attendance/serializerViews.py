from rest_framework import generics
from .models import Employee_DTR
from .serializers import Employee_DTR_Serializer
from .permissions import IsAdminOrReadOnly

class Employee_DTR_SerializerList(generics.ListCreateAPIView):
    queryset = Employee_DTR.objects.all()
    serializer_class = Employee_DTR_Serializer
    permission_classes = [IsAdminOrReadOnly]

class Employee_DTR_SerializerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee_DTR.objects.all()
    serializer_class = Employee_DTR_Serializer
    permission_classes = [IsAdminOrReadOnly]