from rest_framework import serializers
from .models import Patient
import re


class PatientSerializer(serializers.ModelSerializer):
    created_by_name = serializers.ReadOnlyField(source='created_by.name')
    created_by_email = serializers.ReadOnlyField(source='created_by.email')

    class Meta:
        model = Patient
        fields = [
            'id',
            'name',
            'date_of_birth',
            'age',
            'gender',
            'contact_number',
            'email',
            'address',
            'medical_history',
            'created_by',
            'created_by_name',
            'created_by_email',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_by_name', 'created_by_email', 'created_at', 'updated_at']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Patient name cannot be empty.")
        return value.strip()

    def validate_contact_number(self, value):
        cleaned = re.sub(r'[\s\-\(\)\+]', '', value)
        if not cleaned.isdigit() or len(cleaned) < 7 or len(cleaned) > 15:
            raise serializers.ValidationError("Please provide a valid contact number (7 to 15 digits).")
        return value.strip()

    def validate_age(self, value):
        if value is not None and (value < 0 or value > 130):
            raise serializers.ValidationError("Age must be between 0 and 130.")
        return value
