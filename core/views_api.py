from rest_framework import viewsets, permissions
from .models import DynamicForm, Employee
from .serializers import DynamicFormSerializer, EmployeeSerializer

class DynamicFormViewSet(viewsets.ModelViewSet):
    queryset = DynamicForm.objects.all()
    serializer_class = DynamicFormSerializer
    permission_classes = [permissions.IsAuthenticated]


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
