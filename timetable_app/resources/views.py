from django.shortcuts import render,redirect
from .models import Room ,Domain ,Formation ,Module ,Teacher ,Group ,Course ,Session
from .forms import RoomForm ,DomainForm ,FormationForm ,ModuleForm ,TeacherForm ,GroupForm ,CourseForm
from django.contrib.auth.models import User
import csv
from django.http import HttpResponse ,JsonResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'resources/room_list.html', {'rooms': rooms})


def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room_list')  # Redirection vers la liste des salles
    else:
        form = RoomForm()
    return render(request, 'resources/add_room.html', {'form': form})

def domain_list(request):
    domains = Domain.objects.all()
    return render(request, 'resources/domain_list.html', {'domains': domains})

def add_domain(request):
    if request.method == 'POST':
        form = DomainForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('domain_list')  # Redirection vers la liste des domaines
    else:
        form = DomainForm()
    return render(request, 'resources/add_domain.html', {'form': form})

def formation_list(request):
    formations = Formation.objects.all()
    return render(request, 'resources/formation_list.html', {'formations': formations})

def add_formation(request):
    if request.method == 'POST':
        form = FormationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('formation_list')  # Redirection vers la liste des formations
    else:
        form = FormationForm()
    return render(request, 'resources/add_formation.html', {'form': form})

def module_list(request):
    modules = Module.objects.all()
    return render(request, 'resources/module_list.html', {'modules': modules})

def add_module(request):
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('module_list')  # Redirection vers la liste des modules
    else:
        form = ModuleForm()
    return render(request, 'resources/add_module.html', {'form': form})

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'resources/teacher_list.html', {'teachers': teachers})

def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            # Créer un utilisateur Django
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            # Créer un professeur lié à cet utilisateur
            Teacher.objects.create(user=user, name=form.cleaned_data['name'])
            return redirect('teacher_list')  # Redirection vers la liste des professeurs
    else:
        form = TeacherForm()
    return render(request, 'resources/add_teacher.html', {'form': form})

def group_list(request):
    groups = Group.objects.all()
    return render(request, 'resources/group_list.html', {'groups': groups})

def add_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_list')  # Redirection vers la liste des groupes
    else:
        form = GroupForm()
    return render(request, 'resources/add_group.html', {'form': form})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'resources/course_list.html', {'courses': courses})

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            # Générer les sessions
            sessions = course.generate_sessions()
            for session in sessions:
                # Enregistrer chaque session dans la base de données
                Session.objects.create(
                    course=course,
                    start_time=session['start'],
                    end_time=session['end']
                )
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'resources/add_course.html', {'form': form})


def export_courses_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="courses.csv"'

    writer = csv.writer(response)
    writer.writerow(['Module', 'Professeur', 'Salle', 'Groupe', 'Début', 'Fin'])

    courses = Course.objects.all()
    for course in courses:
        writer.writerow([
            course.module.name,
            course.teacher.name,
            course.room.name,
            course.group.name,
            course.start_time,
            course.end_time
        ])

    return response

def export_courses_pdf(request):
    # Créer une réponse HTTP avec le type de contenu PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="courses.pdf"'

    # Initialiser le fichier PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter  # Dimensions de la page (largeur, hauteur)

    # Titre du PDF
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Liste des Cours")

    # Récupérer les cours depuis la base de données
    courses = Course.objects.all()
    y_position = height - 100  # Position verticale initiale

    for course in courses:
        p.setFont("Helvetica", 12)
        p.drawString(50, y_position, f"Module: {course.module.name}")
        p.drawString(50, y_position - 20, f"Professeur: {course.teacher.name}")
        p.drawString(50, y_position - 40, f"Salle: {course.room.name}")
        p.drawString(50, y_position - 60, f"Groupe: {course.group.name}")
        p.drawString(50, y_position - 80, f"Début: {course.start_time}")
        p.drawString(50, y_position - 100, f"Fin: {course.end_time}")
        y_position -= 120  # Décaler vers le bas pour le prochain cours

        # Si la position dépasse la limite de la page, créer une nouvelle page
        if y_position < 50:
            p.showPage()  # Nouvelle page
            y_position = height - 50  # Réinitialiser la position verticale

    # Terminer le PDF
    p.save()

    return response



def course_calendar(request):
    courses = Course.objects.all()
    events = []
    for course in courses:
        events.append({
            'title': f"{course.module.name} - {course.teacher.name}",
            'start': course.start_time.isoformat(),
            'end': course.end_time.isoformat(),
        })
    return JsonResponse(events, safe=False)