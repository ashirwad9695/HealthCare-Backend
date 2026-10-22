from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Doctor
from .serializers import DoctorSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse


class DoctorListCreateView(generics.ListCreateAPIView):
    """
    POST /api/doctors/ - Add a new doctor (Authenticated users only).
    GET /api/doctors/ - Retrieve all doctors.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="Retrieve all doctors.",
        responses={200: DoctorSerializer(many=True)}
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
        description="Add a new doctor (Authenticated users only).",
        request=DoctorSerializer,
        responses={
            201: DoctorSerializer,
            400: OpenApiResponse(description="Validation error")
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "message": "Doctor record created successfully.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/doctors/<id>/ - Get details of a specific doctor.
    PUT /api/doctors/<id>/ - Update doctor details.
    DELETE /api/doctors/<id>/ - Delete a doctor record.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="Get details of a specific doctor.",
        responses={200: DoctorSerializer}
    )
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @extend_schema(
        description="Update doctor details.",
        request=DoctorSerializer,
        responses={200: DoctorSerializer}
    )
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "message": "Doctor record updated successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @extend_schema(
        description="Partially update doctor details.",
        request=DoctorSerializer,
        responses={200: DoctorSerializer}
    )
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "message": "Doctor record updated successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @extend_schema(
        description="Delete a doctor record.",
        responses={200: OpenApiResponse(description="Deleted successfully")}
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        doc_id = instance.id
        doc_name = instance.name
        instance.delete()
        return Response({
            "success": True,
            "message": f"Doctor '{doc_name}' (ID: {doc_id}) deleted successfully."
        }, status=status.HTTP_200_OK)
