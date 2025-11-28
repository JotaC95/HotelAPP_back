from django.conf import settings
from django.db import models


# -------------------------
# Modelos básicos de hotel
# -------------------------

class RoomType(models.Model):
    """Tipo de habitación: Single, Double, Suite, etc."""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    """Habitación física del hotel, por número."""
    number = models.CharField(max_length=10, unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT, related_name="rooms")

    # Configuración por defecto, muy simple al inicio
    # Ejemplo: "2 King beds, sala de estar"
    default_configuration = models.TextField(blank=True)

    def __str__(self):
        return f"Habitación {self.number}"


class GuestStay(models.Model):
    """
    Estancia de un huésped en una habitación.
    Para el cleaner solo necesitamos saber si está 'en habitación' o no.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="stays")
    guest_name = models.CharField(max_length=100)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    # Simplificado: en producción podríamos calcularlo con horarios reales.
    in_house = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.guest_name} en {self.room}"


# -------------------------
# Housekeeping
# -------------------------

class ServiceType(models.TextChoices):
    PRE_ARRIVAL = "pre_arrival", "Pre-arrival"
    STAY_OVER = "stay_over", "Stay-over"
    DEPARTURE = "departure", "Departure"
    VACANT = "vacant", "Vacant"
    WEEKLY = "weekly", "Weekly"


class CleaningStatus(models.TextChoices):
    PENDING = "pending", "Pendiente"
    IN_PROGRESS = "in_progress", "En proceso"
    PAUSED = "paused", "Pausada"
    FINISHED = "finished", "Finalizada"


class CleaningAssignment(models.Model):
    """
    Tarea de limpieza asignada a un cleaner para una fecha concreta.
    Es lo que ves en la lista de 'Mis Habitaciones'.
    """
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="cleaning_assignments")
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cleaning_assignments",
    )

    service_type = models.CharField(
        max_length=20,
        choices=ServiceType.choices,
        default=ServiceType.PRE_ARRIVAL,
    )
    estimated_minutes = models.PositiveIntegerField(default=30)
    status = models.CharField(
        max_length=20,
        choices=CleaningStatus.choices,
        default=CleaningStatus.PENDING,
    )

    # Observaciones simples para la tarjeta de detalle
    observations = models.TextField(blank=True)

    def __str__(self):
        return f"{self.room} ({self.date}) - {self.assigned_to}"


class CleaningSession(models.Model):
    """
    Sesiones de trabajo usadas para el timer de la habitación.
    Cada vez que se inicia/pone en pausa podemos crear/cerrar una sesión.
    """
    assignment = models.ForeignKey(
        CleaningAssignment,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    # Minutos agregados manualmente (+10 min)
    added_minutes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Sesión {self.pk} para {self.assignment}"


class AlertStatus(models.TextChoices):
    OPEN = "open", "Abierta"
    IN_PROGRESS = "in_progress", "En progreso"
    RESOLVED = "resolved", "Resuelta"


class CleaningAlert(models.Model):
    """
    Alerta reportada desde la pantalla 'Reportar alerta'.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="alerts")
    assignment = models.ForeignKey(
        CleaningAssignment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alerts",
    )

    type = models.CharField(max_length=100)  # luego podemos pasarlo a choices
    description = models.TextField()

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_alerts",
    )

    status = models.CharField(
        max_length=20,
        choices=AlertStatus.choices,
        default=AlertStatus.OPEN,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alerta en {self.room} ({self.type})"