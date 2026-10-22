from rest_framework import serializers
from .models import Doctor
import re


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            'id',
            'name',
            'specialization',
            'email',
            'phone_number',
            'years_of_experience',
            'hospital_affiliation',
            'bio',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Doctor name cannot be empty.")
        return value.strip()

    def validate_specialization(self, value):
        if not value.strip():
            raise serializers.ValidationError("Specialization cannot be empty.")
        return value.strip()

    def validate_email(self, value):
        normalized = value.strip().lower()
        query = Doctor.objects.filter(email__iexact=normalized)
        if self.instance:
            query = query.exclude(pk=self.instance.pk)
        if query.exists():
            raise serializers.ValidationError("A doctor with this email address already exists.")
        return normalized

    def validate_phone_number(self, value):
        cleaned = re.sub(r'[\s\-\(\)\+]', '', value)
        if not cleaned.isdigit() or len(cleaned) < 7 or len(cleaned) > 15:
            raise serializers.ValidationError("Please provide a valid phone number (7 to 15 digits).")
        return value.strip()

    def validate_years_of_experience(self, value):
        if value < 0 or value > 80:
            raise serializers.ValidationError("Years of experience must be between 0 and 80.")
        return value
