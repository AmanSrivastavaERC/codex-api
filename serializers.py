from rest_framework import serializers
from .models import CodeExecutionRequest

class CodeExecutionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeExecutionRequest
        fields = '__all__'
