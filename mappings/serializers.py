from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and listing patient-doctor mappings.
    Accepts patient ID and doctor ID, with detailed nested representations on read.
    """
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    patient_details = PatientSerializer(source='patient', read_only=True)
    doctor_details = DoctorSerializer(source='doctor', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id',
            'patient',
            'doctor',
            'patient_details',
            'doctor_details',
            'assigned_date',
            'notes',
        ]
        read_only_fields = ['id', 'assigned_date', 'patient_details', 'doctor_details']

    def validate(self, attrs):
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')

        query = PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor)
        if self.instance:
            query = query.exclude(pk=self.instance.pk)

        if query.exists():
            raise serializers.ValidationError({
                "detail": f"Doctor '{doctor.name}' is already assigned to Patient '{patient.name}'."
            })
        return attrs


class AssignedDoctorRecordSerializer(serializers.ModelSerializer):
    """
    Serializer representing an assigned doctor record for a specific patient.
    Used for GET /api/mappings/<patient_id>/
    """
    mapping_id = serializers.IntegerField(source='id')
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = [
            'mapping_id',
            'assigned_date',
            'notes',
            'doctor',
        ]
