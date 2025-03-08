from django.shortcuts import render, redirect
from .models import *
import datetime
from django.http import JsonResponse
from django.contrib import messages

# Helper function to generate student ID based on session
def generate_student_id_for_session(session):
    # Extract the year and month from the session (e.g., "25-JAN" -> "25", "JAN")
    session_year = session.split('-')[0]
    session_month = session.split('-')[1]
    
    # Find the highest sequential number for this session format
    session_id_pattern = f"{session_year}{session_month}"
    try:
        # Find the highest student_id that starts with this session pattern
        existing_ids = Student.objects.filter(student_id__regex=f'^{session_year}{session_month}[0-9]{{3}}$')
        
        if existing_ids.exists():
            max_seq_num = 0
            for student in existing_ids:
                # Try to parse existing IDs in our format
                try:
                    student_id_str = str(student.student_id)
                    if len(student_id_str) >= 8 and student_id_str[:5] == session_id_pattern:
                        seq_num = int(student_id_str[5:])
                        if seq_num > max_seq_num:
                            max_seq_num = seq_num
                except (ValueError, IndexError):
                    continue
            
            next_seq_num = max_seq_num + 1
        else:
            next_seq_num = 1
    except Exception:
        # In case of any error, default to 1
        next_seq_num = 1
    
    # Format the sequential number with leading zeros
    return f"{session_year}{session_month}{next_seq_num:03d}"

# Create your views here.
def home(request):
    # Get total number of students
    total_students = Student.objects.count()
    context = {
        'total_students': total_students
    }
    return render(request, 'index.html', context)

def list(request):
    # Get all students from the database, ordered by ID
    students = Student.objects.all().order_by('-id')
    
    # Pass the students to the template
    context = {
        'student_list': students
    }
    
    return render(request, 'student-list.html', context)

def add(request):
    # Get session choices from the model
    student_session_choices = Student._meta.get_field('student_session').choices
    
    # Determine default session based on current month
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    year = int(str(current_year)[-2:])  # Get last two digits of year
    
    # Default session logic: Jan-Jun uses current year's JAN session, Jul-Dec uses current year's JUL session
    default_session = f"{year}-JAN" if current_month <= 6 else f"{year}-JUL"
    
    # Check if this is an AJAX request for a specific session ID
    if request.method == 'GET' and 'get_id_for_session' in request.GET:
        selected_session = request.GET.get('get_id_for_session')
        if selected_session:
            # Generate ID for the specified session
            auto_id = generate_student_id_for_session(selected_session)
            # Return the new ID as JSON
            return JsonResponse({'auto_id': auto_id})
    
    # Generate auto ID based on the default session
    auto_id = generate_student_id_for_session(default_session)
    
    # Process form submission
    if request.method == 'POST':
        # Get the selected session from the form
        selected_session = request.POST.get('student_session', default_session)
        
        # If session is different from the default, regenerate the ID for the selected session
        if selected_session != default_session:
            auto_id = generate_student_id_for_session(selected_session)
        
        try:
            # Create a new Student object with the form data
            student = Student(
                f_name=request.POST.get('first_name'),
                l_name=request.POST.get('last_name'),
                student_id=request.POST.get('student_id'),
                gender=request.POST.get('gender'),
                dob=request.POST.get('date_of_birth'),
                student_session=request.POST.get('student_session'),
                religion=request.POST.get('religion'),
                phone=request.POST.get('phone_number'),
                email=request.POST.get('email'),
                father_name=request.POST.get('father_name'),
                father_occupation=request.POST.get('father_occupation'),
                father_phone=request.POST.get('father_phone'),
                mother_name=request.POST.get('mother_name'),
                mother_occupation=request.POST.get('mother_occupation'),
                mother_phone=request.POST.get('mother_phone'),
                present_address=request.POST.get('present_address'),
                permanent_address=request.POST.get('permanent_address')
            )
            
            # Handle image upload if provided
            if 'student_image' in request.FILES and request.FILES['student_image']:
                student.image = request.FILES['student_image']
                print(f"Image uploaded: {request.FILES['student_image'].name}")
                
            # Save the student to the database
            student.save()
            print(f"Student saved with ID: {student.student_id}")
            if student.image:
                print(f"Image path: {student.image.path}")
                print(f"Image URL: {student.image.url}")
            
            # Redirect to the student list page after successful submission
            return redirect('student-list')
            
        except Exception as e:
            # If there's an error, add it to the context
            context = {
                'student_session': student_session_choices,
                'default_session': default_session,
                'auto_id': auto_id,
                'error_message': f"Error creating student: {str(e)}"
            }
            return render(request, 'student-add.html', context)
    
    context = {
        'student_session': student_session_choices,
        'default_session': default_session,
        'auto_id': auto_id,
        'current_time':timezone.now(),
    }
    
    return render(request, 'student-add.html', context)

def edit(request, student_id):
    try:
        student = Student.objects.get(student_id=student_id)
        # Get session choices from the model
        student_session_choices = Student._meta.get_field('student_session').choices
        
        if request.method == 'POST':
            # Update student information
            student.f_name = request.POST.get('first_name')
            student.l_name = request.POST.get('last_name')
            student.student_id = request.POST.get('student_id')
            student.gender = request.POST.get('gender')
            student.dob = request.POST.get('date_of_birth')
            student.student_session = request.POST.get('student_session')
            student.religion = request.POST.get('religion')
            student.phone = request.POST.get('phone_number')
            student.email = request.POST.get('email')
            student.father_name = request.POST.get('father_name')
            student.father_occupation = request.POST.get('father_occupation')
            student.father_phone = request.POST.get('father_phone')
            student.mother_name = request.POST.get('mother_name')
            student.mother_occupation = request.POST.get('mother_occupation')
            student.mother_phone = request.POST.get('mother_phone')
            student.present_address = request.POST.get('present_address')
            student.permanent_address = request.POST.get('permanent_address')
            
            # Handle image upload if provided
            if 'student_image' in request.FILES:
                student.image = request.FILES['student_image']
            
            student.save()
            from django.shortcuts import redirect
            return redirect('student-details', student_id=student.student_id)
        
        context = {
            'student': student,
            'session_choices': student_session_choices
        }
        return render(request, 'student-edit.html', context)
    except Student.DoesNotExist:
        from django.shortcuts import redirect
        return redirect('student-list')

def details(request, student_id=None):
    try:
        student = Student.objects.get(student_id=student_id)
        # Get all payments for this student
        payments = Payment.objects.filter(student=student).select_related('course')
        total_paid = sum(payment.amount_paid for payment in payments)
        total_fees = sum(payment.course.fees for payment in payments if payment.course)
        
        # Get the latest course from payments
        latest_course = None
        if payments.exists():
            latest_payment = payments.order_by('-payment_date').first()
            latest_course = latest_payment.course
        
        context = {
            'student': student,
            'payments': payments,
            'total_paid': total_paid,
            'total_fees': total_fees,
            'total_remaining': total_fees - total_paid,
            'latest_course': latest_course
        }
        return render(request, 'student-details.html', context)
    except Student.DoesNotExist:
        # If student doesn't exist, redirect to student list
        from django.shortcuts import redirect
        return redirect('student-list')

def delete_student(request, student_id):
    if request.method == 'POST':
        try:
            student = Student.objects.get(student_id=student_id)
            # Delete the student's image if it exists
            if student.image:
                student.image.delete()
            student.delete()
            return redirect('student-list')
        except Student.DoesNotExist:
            pass
    return redirect('student-list')

def fees_collections(request):
    return render(request, 'fees-collections.html')

def add_fees_collection(request):
    return render(request, 'add-fees-collection.html')

def view_fees(request):
    return render(request, 'view-fees.html')

def login(request):
    return render(request, 'login.html')

def forgot_password(request):
    return redirect('login')

def register_new_admin(request):
    return render(request, 'register.html')