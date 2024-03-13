# api/models.py
from django.db import models

class CodeExecutionRequest(models.Model):
    code = models.TextField()
    input_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
