from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer, AssignedDoctorRecordSerializer
from patients.models import Patient
from doctors.models import Doctor
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter


class MappingListCreateView(APIView):
    """
    POST /api/mappings/ - Assign a doctor to a patient.
    GET /api/mappings/ - Retrieve all patient-doctor mappings.
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="Retrieve all patient-doctor mappings.",
        responses={200: PatientDoctorMappingSerializer(many=True)}
    )
    def get(self, request):
        mappings = PatientDoctorMapping.objects.select_related('patient', 'doctor').all()
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response({
            "success": True,
            "count": mappings.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @extend_schema(
        description="Assign a doctor to a patient.",
        request=PatientDoctorMappingSerializer,
        responses={
            201: PatientDoctorMappingSerializer,
            400: OpenApiResponse(description="Validation error or already assigned")
        }
    )
    def post(self, request):
        serializer = PatientDoctorMappingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mapping = serializer.save()
        return Response({
            "success": True,
            "message": "Doctor assigned to patient successfully.",
            "data": PatientDoctorMappingSerializer(mapping).data
        }, status=status.HTTP_201_CREATED)


class MappingDetailOrPatientMappingsView(APIView):
    """
    Handles:
    - GET /api/mappings/<patient_id>/ - Get all doctors assigned to a specific patient.
    - DELETE /api/mappings/<id>/ - Remove a doctor from a patient by mapping ID.
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="Get all doctors assigned to a specific patient by patient ID.",
        parameters=[OpenApiParameter("id", int, description="Patient ID")],
        responses={200: AssignedDoctorRecordSerializer(many=True)}
    )
    def get(self, request, id):
        # Verify patient exists
        try:
            patient = Patient.objects.get(pk=id)
        except Patient.DoesNotExist:
            raise NotFound(detail=f"Patient with ID {id} does not exist.")

        mappings = PatientDoctorMapping.objects.select_related('doctor', 'patient').filter(patient=patient)
        serializer = AssignedDoctorRecordSerializer(mappings, many=True)
        return Response({
            "success": True,
            "patient_id": patient.id,
            "patient_name": patient.name,
            "assigned_doctors_count": mappings.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @extend_schema(
        description="Remove a doctor from a patient by mapping ID.",
        parameters=[OpenApiParameter("id", int, description="Mapping ID")],
        responses={200: OpenApiResponse(description="Doctor unassigned successfully")}
    )
    def delete(self, request, id):
        try:
            mapping = PatientDoctorMapping.objects.select_related('patient', 'doctor').get(pk=id)
            mapping_id = mapping.id
            patient_name = mapping.patient.name
            doctor_name = mapping.doctor.name
            mapping.delete()
            return Response({
                "success": True,
                "message": f"Mapping {mapping_id} removed successfully. Dr. {doctor_name} unassigned from patient '{patient_name}'."
            }, status=status.HTTP_200_OK)
        except PatientDoctorMapping.DoesNotExist:
            raise NotFound(detail=f"Mapping with ID {id} does not exist.")
