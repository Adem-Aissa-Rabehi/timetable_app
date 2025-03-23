from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Room, Domain, Formation, Module, Teacher, Group, Course, Session, TimeSlot, ManualSession
from .forms import RoomForm, DomainForm, FormationForm, ModuleForm, TeacherForm, GroupForm, CourseForm
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import timedelta

# Page d'accueil
def index(request):
    return render(request, 'resources/index.html')

# Salles
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'resources/room_list.html', {'rooms': rooms})

def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "La salle a été ajoutée avec succès.")
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'resources/add_room.html', {'form': form})

def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "La salle a été modifiée avec succès.")
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'resources/edit_room.html', {'form': form})

def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        room.delete()
        messages.success(request, "La salle a été supprimée avec succès.")
        return redirect('room_list')
    return render(request, 'resources/delete_confirmation.html', {'object': room})

# Domaines
def domain_list(request):
    domains = Domain.objects.all()
    return render(request, 'resources/domain_list.html', {'domains': domains})

def add_domain(request):
    if request.method == 'POST':
        form = DomainForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le domaine a été ajouté avec succès.")
            return redirect('domain_list')
    else:
        form = DomainForm()
    return render(request, 'resources/add_domain.html', {'form': form})

def edit_domain(request, domain_id):
    domain = get_object_or_404(Domain, id=domain_id)
    if request.method == 'POST':
        form = DomainForm(request.POST, instance=domain)
        if form.is_valid():
            form.save()
            messages.success(request, "Le domaine a été modifié avec succès.")
            return redirect('domain_list')
    else:
        form = DomainForm(instance=domain)
    return render(request, 'resources/edit_domain.html', {'form': form})

def delete_domain(request, domain_id):
    domain = get_object_or_404(Domain, id=domain_id)
    if request.method == 'POST':
        domain.delete()
        messages.success(request, "Le domaine a été supprimé avec succès.")
        return redirect('domain_list')
    return render(request, 'resources/delete_confirmation.html', {'object': domain})

# Formations
def formation_list(request):
    formations = Formation.objects.all()
    return render(request, 'resources/formation_list.html', {'formations': formations})

def add_formation(request):
    if request.method == 'POST':
        form = FormationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "La formation a été ajoutée avec succès.")
            return redirect('formation_list')
    else:
        form = FormationForm()
    return render(request, 'resources/add_formation.html', {'form': form})

def edit_formation(request, formation_id):
    formation = get_object_or_404(Formation, id=formation_id)
    if request.method == 'POST':
        form = FormationForm(request.POST, instance=formation)
        if form.is_valid():
            form.save()
            messages.success(request, "La formation a été modifiée avec succès.")
            return redirect('formation_list')
    else:
        form = FormationForm(instance=formation)
    return render(request, 'resources/edit_formation.html', {'form': form})

def delete_formation(request, formation_id):
    formation = get_object_or_404(Formation, id=formation_id)
    if request.method == 'POST':
        formation.delete()
        messages.success(request, "La formation a été supprimée avec succès.")
        return redirect('formation_list')
    return render(request, 'resources/delete_confirmation.html', {'object': formation})

# Modules
def module_list(request):
    modules = Module.objects.all()
    return render(request, 'resources/module_list.html', {'modules': modules})

def add_module(request):
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le module a été ajouté avec succès.")
            return redirect('module_list')
    else:
        form = ModuleForm()
    return render(request, 'resources/add_module.html', {'form': form})

def edit_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            messages.success(request, "Le module a été modifié avec succès.")
            return redirect('module_list')
    else:
        form = ModuleForm(instance=module)
    return render(request, 'resources/edit_module.html', {'form': form})

def delete_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        module.delete()
        messages.success(request, "Le module a été supprimé avec succès.")
        return redirect('module_list')
    return render(request, 'resources/delete_confirmation.html', {'object': module})

# Professeurs
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'resources/teacher_list.html', {'teachers': teachers})

def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            Teacher.objects.create(user=user, name=form.cleaned_data['name'])
            messages.success(request, "Le professeur a été ajouté avec succès.")
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'resources/add_teacher.html', {'form': form})

def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, "Le professeur a été modifié avec succès.")
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'resources/edit_teacher.html', {'form': form})

def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        teacher.user.delete()  # Supprimer l'utilisateur Django associé
        teacher.delete()
        messages.success(request, "Le professeur a été supprimé avec succès.")
        return redirect('teacher_list')
    return render(request, 'resources/delete_confirmation.html', {'object': teacher})

# Groupes
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'resources/group_list.html', {'groups': groups})

def add_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le groupe a été ajouté avec succès.")
            return redirect('group_list')
    else:
        form = GroupForm()
    return render(request, 'resources/add_group.html', {'form': form})

def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Le groupe a été modifié avec succès.")
            return redirect('group_list')
    else:
        form = GroupForm(instance=group)
    return render(request, 'resources/edit_group.html', {'form': form})

def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        group.delete()
        messages.success(request, "Le groupe a été supprimé avec succès.")
        return redirect('group_list')
    return render(request, 'resources/delete_confirmation.html', {'object': group})

# Cours
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'resources/course_list.html', {'courses': courses})

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            try:
                sessions = course.generate_sessions()
                for session in sessions:
                    Session.objects.create(
                        course=course,
                        start_time=session['start'],
                        end_time=session['end']
                    )
                messages.success(request, "Le cours a été ajouté avec succès et les sessions ont été générées.")
            except Exception as e:
                messages.error(request, f"Erreur lors de la génération des sessions : {str(e)}")
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'resources/add_course.html', {'form': form})

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Le cours a été modifié avec succès.")
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'resources/edit_course.html', {'form': form})

def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, "Le cours a été supprimé avec succès.")
        return redirect('course_list')
    return render(request, 'resources/delete_confirmation.html', {'object': course})

# Exportation CSV
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

# Exportation PDF
def export_courses_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="courses.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Liste des Cours")
    y_position = height - 100
    courses = Course.objects.all()
    for course in courses:
        p.setFont("Helvetica", 12)
        p.drawString(50, y_position, f"Module: {course.module.name}")
        p.drawString(50, y_position - 20, f"Professeur: {course.teacher.name}")
        p.drawString(50, y_position - 40, f"Salle: {course.room.name}")
        p.drawString(50, y_position - 60, f"Groupe: {course.group.name}")
        p.drawString(50, y_position - 80, f"Début: {course.start_time}")
        p.drawString(50, y_position - 100, f"Fin: {course.end_time}")
        y_position -= 120
        if y_position < 50:
            p.showPage()
            y_position = height - 50
    p.save()
    return response

# Calendrier
def calendar_data(request):
    sessions = Session.objects.all()
    events = []
    for session in sessions:
        events.append({
            'title': f"{session.course.module.name} - {session.course.teacher}",
            'start': session.start_time.isoformat(),
            'end': session.end_time.isoformat(),
            'color': '#378006',
        })
    return JsonResponse(events, safe=False)

def calendar_view(request):
    hours = ['08:30', '10:00', '11:30', '12:30', '14:00', '15:30']
    days = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
    sessions = Session.objects.all()
    return render(request, 'resources/calendar.html', {
        'hours': hours,
        'days': days,
        'sessions': sessions,
    })

# Planification Automatique
def auto_schedule_course(request, course_id):
    time_slots = TimeSlot.objects.all()
    course = get_object_or_404(Course, id=course_id)
    try:
        sessions = course.auto_schedule_sessions(time_slots)
        for session in sessions:
            Session.objects.create(
                course=course,
                start_time=session['start'],
                end_time=session['end']
            )
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def auto_schedule_all_courses(request):
    time_slots = TimeSlot.objects.all()
    courses = Course.objects.all()
    for course in courses:
        try:
            sessions = course.auto_schedule_sessions(time_slots)
            for session in sessions:
                Session.objects.create(
                    course=course,
                    start_time=session['start'],
                    end_time=session['end']
                )
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'success'})

# Sessions Manuelles
def save_manual_session(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        course = get_object_or_404(Course, id=course_id)
        ManualSession.objects.create(
            course=course,
            start_time=start_time,
            end_time=end_time
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
def dashboard(request):
    # Récupérer toutes les entités depuis la base de données
    rooms = Room.objects.all()
    domains = Domain.objects.all()
    formations = Formation.objects.all()
    modules = Module.objects.all()
    teachers = Teacher.objects.all()
    groups = Group.objects.all()
    courses = Course.objects.all()

    # Passer les données au template
    context = {
        'rooms': rooms,
        'domains': domains,
        'formations': formations,
        'modules': modules,
        'teachers': teachers,
        'groups': groups,
        'courses': courses,
    }
    return render(request, 'resources/dashboard.html', context)