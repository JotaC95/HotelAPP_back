from rest_framework import serializers
from .models import Room, RoomType, CleaningAssignment, ServiceType, CleaningStatus


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ["id", "name"]


class RoomSerializer(serializers.ModelSerializer):
    room_type = RoomTypeSerializer()

    class Meta:
        model = Room
        fields = ["id", "number", "room_type", "default_configuration"]


class CleaningAssignmentListSerializer(serializers.ModelSerializer):
    """
    Serializer para la lista de 'Mis Habitaciones'.
    Incluye info de la habitación.
    """
    room = RoomSerializer()
    service_type_label = serializers.CharField(source="get_service_type_display", read_only=True)
    status_label = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = CleaningAssignment
        fields = [
            "id",
            "date",
            "room",
            "service_type",
            "service_type_label",
            "status",
            "status_label",
            "estimated_minutes",
        ]