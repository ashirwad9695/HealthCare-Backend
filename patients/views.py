from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Patient
from .serializers import PatientSerializer
from .permissions import IsPatientOwnerOrStaff
from drf_spectacular.utils import extend_schema, OpenApiResponse


class PatientListCreateView(generics.ListCreateAPIView):
    """
    POST /api/patients/ - Add a new patient (Authenticated users only).
    GET /api/patients/ - Retrieve all patients created by the authenticated user.
    """
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retrieve all patients created by the authenticated user
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @extend_schema(
        description="Retrieve all patients created by the authenticated user.",
        responses={200: PatientSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "count": queryset.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @extend_schema(
        description="Add a new patient (Authenticated users only).",
        request=PatientSerializer,
        responses={
            201: PatientSerializer,
            400: OpenApiResponse(description="Validation error")
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "success": True,
            "message": "Patient record created successfully.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/patients/<id>/ - Get details of a specific patient.
    PUT /api/patients/<id>/ - Update patient details.
    DELETE /api/patients/<id>/ - Delete a patient record.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatientOwnerOrStaff]

    @extend_schema(
        description="Get details of a specific patient.",
        responses={200: PatientSerializer}
    )
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @extend_schema(
        description="Update patient details.",
        request=PatientSerializer,
        responses={200: PatientSerializer}
    )
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "message": "Patient updated successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @extend_schema(
        description="Partially update patient details.",
        request=PatientSerializer,
        responses={200: PatientSerializer}
    )
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "message": "Patient updated successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @extend_schema(
        description="Delete a patient record.",
        responses={200: OpenApiResponse(description="Deleted successfully")}
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        patient_id = instance.id
        patient_name = instance.name
        instance.delete()
        return Response({
            "success": True,
            "message": f"Patient '{patient_name}' (ID: {patient_id}) deleted successfully."
        }, status=status.HTTP_200_OK)
