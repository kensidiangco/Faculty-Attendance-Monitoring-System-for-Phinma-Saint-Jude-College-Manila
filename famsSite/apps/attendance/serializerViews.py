from rest_framework import generics
from .models import Employee_DTR, Department, Employee
from .serializers import Employee_DTR_Serializer, Department_Serializer
from .permissions import IsAdminOrReadOnly

class Employee_DTR_Serializer_List(generics.ListCreateAPIView):
    queryset = Employee_DTR.objects.all()
    serializer_class = Employee_DTR_Serializer
    permission_classes = [IsAdminOrReadOnly]

class Employee_DTR_Serializer_Detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee_DTR.objects.all()
    serializer_class = Employee_DTR_Serializer
    permission_classes = [IsAdminOrReadOnly]

class Department_Serializer_Detail(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = Department_Serializer
    permission_classes = [IsAdminOrReadOnly]