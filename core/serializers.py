from rest_framework import serializers
from django.contrib.auth.models import User
from .models import DynamicForm, FormField, Employee


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ['id', 'label', 'field_type', 'required', 'order']


class DynamicFormSerializer(serializers.ModelSerializer):
    fields = FormFieldSerializer(many=True)

    class Meta:
        model = DynamicForm
        fields = ['id', 'name', 'fields']

    def create(self, validated_data):
        fields_data = validated_data.pop('fields')
        form = DynamicForm.objects.create(**validated_data)
        for i, field_data in enumerate(fields_data):
            FormField.objects.create(form=form, order=i, **field_data)
        return form


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'form', 'data', 'created_at']
