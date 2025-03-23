from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import timedelta, datetime ,time, date

# Modèle pour les salles
class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} (Capacité: {self.capacity})"

# Modèle pour les domaines
class Domain(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Modèle pour les formations
class Formation(models.Model):
    name = models.CharField(max_length=100)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="formations")

    def __str__(self):
        return f"{self.name} ({self.domain})"

# Modèle pour les modules
class Module(models.Model):
    SESSION_DURATION_CHOICES = [
        (90, '1h30'),
        (180, '3h'),
    ]

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE, related_name="modules")
    total_duration = models.PositiveIntegerField(help_text="Durée totale du module en heures")
    session_duration = models.PositiveIntegerField(
        choices=SESSION_DURATION_CHOICES,
        default=90,
        help_text="Durée d'une session de cours en minutes"
    )

    def __str__(self):
        return f"{self.code} - {self.name} ({self.total_duration}h total, sessions de {self.get_session_duration_display()})"
    
    def calculate_end_date(self, start_time):
        """
        Calcule la date de fin du module en fonction de l'heure de début.
        """
        total_minutes = self.total_duration * 60  # Convertir les heures en minutes
        session_count = total_minutes // self.session_duration  # Nombre de sessions nécessaires
        remaining_minutes = total_minutes % self.session_duration  # Minutes restantes

        # Calculer la date de fin en ajoutant les sessions
        current_time = start_time
        for _ in range(session_count):
            current_time += timedelta(minutes=self.session_duration)

        # Ajouter les minutes restantes
        if remaining_minutes > 0:
            current_time += timedelta(minutes=remaining_minutes)

        return current_time

# Modèle pour les professeurs
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Modèle pour les groupes d'étudiants
class Group(models.Model):
    name = models.CharField(max_length=100)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name="groups")
    student_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.formation})"

# Modèle pour les cours
class Course(models.Model):

    DAYS_OF_WEEK = [
        (0, 'Lundi'),
        (1, 'Mardi'),
        (2, 'Mercredi'),
        (3, 'Jeudi'),
        (4, 'Vendredi'),
        (5, 'Samedi'),
        (6, 'Dimanche'),
    ]
    module = models.ForeignKey('Module', on_delete=models.CASCADE, related_name="courses")
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name="courses")
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name="courses")
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name="courses")
    start_time = models.TimeField(
        default=time(8, 30),  # Heure par défaut : 8h30
        null=True, blank=True,
        help_text="Heure de début du cours"
    )
    end_time = models.TimeField(
        default=time(11, 30),  # Heure par défaut : 11h30
        null=True, blank=True,
        help_text="Heure de fin du cours"
    )
    day_of_week = models.IntegerField(
        choices=DAYS_OF_WEEK,
        null=True, blank=True,
        help_text="Jour de la semaine où le cours se déroule"
    )
    start_date = models.DateField(
        default=date(2023, 1, 1),  # Date par défaut : 2023-01-01
        null=True, blank=True,
        help_text="Date de début des sessions"
    )
    total_sessions = models.PositiveIntegerField(
        default=10,  # Nombre de sessions par défaut : 10
        null=True, blank=True,
        help_text="Nombre total de sessions"
    )
    card_color = models.CharField(
        max_length=20,
        default="#378006",  # Couleur par défaut
        help_text="Couleur de la carte pour ce cours"
    )  # Nouveau champ ajouté


    def generate_sessions(self):
        """
        Génère les sessions du cours en fonction de la récurrence hebdomadaire.
        """
        if not all([self.start_date, self.day_of_week, self.start_time, self.end_time, self.total_sessions]):
            raise ValueError("Tous les champs requis pour générer les sessions ne sont pas définis.")

        sessions = []
        current_date = self.start_date
        while len(sessions) < self.total_sessions:
            if current_date.weekday() == self.day_of_week:  # Utilise weekday() pour correspondre à DAYS_OF_WEEK
                session_start = datetime.combine(current_date, self.start_time)
                session_end = datetime.combine(current_date, self.end_time)
                sessions.append({
                    'start': session_start,
                    'end': session_end,
                })
            current_date += timedelta(days=1)
        return sessions
    
    def check_conflicts(self, start_time, end_time):
        """
        Vérifie s'il y a des conflits pour la salle ou le professeur pendant le créneau donné.
        """
        # Vérifier les conflits de salle
        overlapping_room_courses = Course.objects.filter(
            room=self.room,
            sessions__start_time__lt=end_time,
            sessions__end_time__gt=start_time
        )
        if overlapping_room_courses.exists():
            raise ValidationError("La salle est déjà réservée pour ce créneau.")

        # Vérifier les conflits de professeur
        overlapping_teacher_courses = Course.objects.filter(
            teacher=self.teacher,
            sessions__start_time__lt=end_time,
            sessions__end_time__gt=start_time
        )
        if overlapping_teacher_courses.exists():
            raise ValidationError("Le professeur est déjà occupé pour ce créneau.")
        

    def auto_schedule_sessions(self, time_slots):
        """
        Planifie automatiquement les sessions du cours en fonction des créneaux disponibles.
        """
        if not all([self.start_date, self.day_of_week, self.total_sessions, self.module.session_duration]):
            raise ValueError("Tous les champs requis pour planifier les sessions ne sont pas définis.")

        # Convertir la durée de session en minutes
        session_duration_minutes = self.module.session_duration
        total_minutes_required = self.total_sessions * session_duration_minutes

        # Initialiser les variables
        current_date = self.start_date
        scheduled_sessions = []
        remaining_minutes = total_minutes_required

        # Parcourir les jours jusqu'à ce que toutes les sessions soient planifiées
        while remaining_minutes > 0:
            if current_date.weekday() == self.day_of_week:
                # Trouver les créneaux disponibles pour ce jour
                available_slots = [slot for slot in time_slots if slot.day_of_week == current_date.weekday()]

                for slot in available_slots:
                    slot_start = datetime.combine(current_date, slot.start_time)
                    slot_end = datetime.combine(current_date, slot.end_time)
                    slot_duration = (slot_end - slot_start).total_seconds() / 60  # Durée du créneau en minutes

                    # Planifier autant de sessions que possible dans ce créneau
                    while remaining_minutes > 0 and slot_duration >= session_duration_minutes:
                        session_start = slot_start + timedelta(minutes=total_minutes_required - remaining_minutes)
                        session_end = session_start + timedelta(minutes=session_duration_minutes)

                        # Vérifier les conflits avant de planifier
                        try:
                            self.check_conflicts(session_start, session_end)
                        except ValidationError as e:
                            # Ignorer ce créneau et passer au suivant
                            break

                        # Ajouter la session planifiée
                        scheduled_sessions.append({
                            'start': session_start,
                            'end': session_end,
                        })
                        remaining_minutes -= session_duration_minutes

            # Passer au jour suivant
            current_date += timedelta(days=1)

        return scheduled_sessions
    
    
    def __str__(self):
        return f"{self.module} avec {self.teacher} dans {self.room} pour {self.group}"

class Session(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sessions")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Session de {self.course.module} le {self.start_time}"

class TimeSlot(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Lundi'),
        (1, 'Mardi'),
        (2, 'Mercredi'),
        (3, 'Jeudi'),
        (4, 'Vendredi'),
        (5, 'Samedi'),
        (6, 'Dimanche'),
    ]

    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, help_text="Jour de la semaine")
    start_time = models.TimeField(help_text="Heure de début du créneau")
    end_time = models.TimeField(help_text="Heure de fin du créneau")

    def __str__(self):
        return f"{self.get_day_of_week_display()} {self.start_time} - {self.end_time}"
    
class ManualSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="manual_sessions")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

