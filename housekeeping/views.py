from django.shortcuts import render

# Create your views here.
from datetime import date as date_class

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import CleaningAssignment, CleaningStatus
from .serializers import CleaningAssignmentListSerializer


class MyAssignmentsView(APIView):
    """
    Devuelve la lista de habitaciones asignadas al cleaner para una fecha.
    También calcula 'progreso del día' y 'tiempo total restante' parecido
    a tus pantallas.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Tomamos la fecha desde query param ?date=YYYY-MM-DD
        date_str = request.query_params.get("date")
        if date_str:
            target_date = date_class.fromisoformat(date_str)
        else:
            target_date = date_class.today()

        # Filtramos por usuario logueado y fecha
        qs = CleaningAssignment.objects.filter(
            assigned_to=request.user,
            date=target_date,
        ).select_related("room", "room__room_type")

        serializer = CleaningAssignmentListSerializer(qs, many=True)

        total_assignments = qs.count()
        finished_count = qs.filter(status=CleaningStatus.FINISHED).count()

        # Tiempo total restante: suma de estimados de las no finalizadas
        remaining_minutes = qs.exclude(status=CleaningStatus.FINISHED).aggregate(
            total=models.Sum("estimated_minutes")
        )["total"] or 0

        data = {
            "date": target_date,
            "total_assignments": total_assignments,
            "finished_assignments": finished_count,
            "remaining_minutes": remaining_minutes,
            "assignments": serializer.data,
        }
        return Response(data)