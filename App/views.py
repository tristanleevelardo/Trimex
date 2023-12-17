from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .studentForms import StudentSignUpForm
from .facultyForms import FacultySignUpForm
from .models import Faculty,Student,thirdYear,unit,Mail
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .gradeForms import ThirdYearForm
from .assignForms import ThirdYearFormAssign
from . unitsForms import unitForms
from .mailForms import mailForms
from django.urls import reverse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def home(request):

    if request.method == 'POST':
        username = request.POST['student_username']
        email = request.POST.get('student_email').lower()
        password = request.POST['student_password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            try:
                student = Student.objects.get(email=email, is_faculty=False)
                return redirect('student', student_name=student.name.replace(' ', ''))
            except Student.DoesNotExist:
                messages.error(request, "Invalid user type")
                return redirect('home')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('home')

    return render(request, 'home.html')



def faculty(request):

    if request.method == 'POST':
        username = request.POST['faculty_username']
        email = request.POST['faculty_email'].lower()
        password = request.POST['faculty_password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            try:
                faculty = Faculty.objects.get(email=email, is_faculty=True)
                return redirect('facultyPage', faculty_name=faculty.name.replace(' ', ''))
            except Faculty.DoesNotExist:
                messages.error(request, "Invalid user type")
                return redirect('faculty')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('faculty')

    return render(request, 'faculty.html')


def facultyPage (request,faculty_name):

    try:
        faculty = Faculty.objects.get(name=faculty_name.replace(' ', ' '))
        username = faculty.username  # Get the username directly from the retrieved Student object

        # Check if the username from the URL matches the username of the logged-in user
        if request.user.is_authenticated and request.user.username != username:
            # Log out the current user
            logout(request)
            messages.info(request, "Authorized Timed Out, Please Log-in Again")
            return redirect('faculty')
        
        units = unit.objects.filter(instructor_fullName=faculty_name)

        return render(request, 'facultyPage.html', {'units': units, 'faculty': faculty})
    
    except Faculty.DoesNotExist:
        messages.error(request, "faculty does not exist")
        return redirect('faculty')



def logout_user(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')


def studentRegister(request,admin_username):

    if request.user.is_authenticated:
    
        if request.user.username != admin_username:
                # Log out the current user
                logout(request)
                messages.info(request, "Authorized Timed Out, Please Log-in Again")
                return redirect('adminLogin')
        
        else:
            if request.method == 'POST':
                form = StudentSignUpForm(request.POST)
                if form.is_valid():
                    # Create a new User instance and save it
                    user = form.save()

                    # Create a new Student instance and save it
                    student = Student(
                        firstName=form.cleaned_data['first_name'] ,
                        lastName=form.cleaned_data['last_name'],
                        name=form.cleaned_data['first_name'] + form.cleaned_data['last_name'],
                        username=form.cleaned_data['username'],
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password1'],
                        section = form.cleaned_data['section']
                    )
                    student.save()

                    messages.success(request, "Student Registered Successfully.")

                    return redirect(reverse('adminPage', kwargs={'admin_username': admin_username},))

            else:
                form = StudentSignUpForm()
        
            return render(request, 'studentRegister.html', {'form': form, 'admin_username': admin_username})
        
    return redirect('adminLogin')


def facultyRegister (request,admin_username):
    if request.user.is_authenticated:
    
        if request.user.username != admin_username:
                # Log out the current user
                logout(request)
                messages.info(request, "Authorized Timed Out, Please Log-in Again")
                return redirect('adminLogin')
        
        else:

            if request.method == 'POST':
                form = FacultySignUpForm(request.POST)
                if form.is_valid():

                    user = form.save()


                    faculty = Faculty(
                        firstName=form.cleaned_data['first_name'] ,
                        lastName=form.cleaned_data['last_name'],
                        name=form.cleaned_data['first_name'] + form.cleaned_data['last_name'],
                        username=form.cleaned_data['username'],
                        email=form.cleaned_data['email'],
                        password=form.cleaned_data['password1'],
                        is_faculty=form.cleaned_data['is_faculty']
                    )
                    faculty.save()


                    messages.success(request, "Faculty Registered Successfully.")

                    return redirect(reverse('adminPage', kwargs={'admin_username': admin_username}))

            else:
                form = FacultySignUpForm()
            
            return render(request, 'facultyRegister.html', {'form': form, 'admin_username': admin_username})
        
    return redirect('adminLogin')


def success_view(request):
    return render(request, 'success.html')

def student(request, student_name):
    try:
        student = Student.objects.get(name=student_name.replace(' ', ' '))
        username = student.username

        if request.user.is_authenticated and request.user.username != username:
            logout(request)
            messages.info(request, "Authorized Timed Out, Please Log-in Again")
            return redirect('home')

        # Use filter to get multiple instances of thirdYear
        subjects = thirdYear.objects.filter(student_fullName=student_name)

        return render(request, 'student.html', {'subjects': subjects, 'student': student})
    
    except Student.DoesNotExist:
        messages.error(request, "Student does not exist")
        return redirect('home')

def facultyUnit(request, faculty_name, subject, course):
    try:
        faculty = Faculty.objects.get(name=faculty_name.replace(' ', ' '))
        username = faculty.username
        faculty_name1=faculty_name

        if request.user.is_authenticated and request.user.username != username:
            # Log out the current user
            logout(request)
            messages.info(request, "Authorized Timed Out, Please Log-in Again")
            return redirect('faculty')

        # Filter thirdYear objects based on instructor_fullName, subject, and course
        subjects = thirdYear.objects.filter(instructor_fullName=faculty_name, subject=subject, course=course)
        subjectName = subject
        courseName = course

        # If you want to pass all matching objects to the template
        thirdyears = thirdYear.objects.filter(instructor_fullName=faculty_name, subject=subject, course=course)

        return render(request, 'facultyEncode.html', {'subjects': subjects, 'faculty': faculty, 'subjectName': subjectName, 'courseName': courseName, 'thirdyears': thirdyears,'faculty_name1':faculty_name1})

    except Faculty.DoesNotExist:
        messages.error(request, "Faculty does not exist")
        return redirect('faculty')

def edit_student(request, student_name,student_subject):

    student = thirdYear.objects.get(student_fullName=student_name,subject=student_subject)

    course = student.course
    student_firstName = student.student_firstName
    student_lastName = student.student_lastName
    student_fullName = f"{student_lastName}, {student_firstName}"

    if request.method == 'POST':
        form = ThirdYearForm(request.POST, instance=student)
        if form.is_valid():
            # Calculate writtenOutput as 30% of totalSW and 70% of totalQuiz
            written_output = 0.3 * form.cleaned_data['totalSW'] + 0.7 * form.cleaned_data['totalQuiz']

            # Calculate exam as 30% of prelim, 30% of midterm, and 40% of finals
            exam = 0.3 * form.cleaned_data['prelim'] + 0.3 * form.cleaned_data['midterm'] + 0.4 * form.cleaned_data['finals']

            # Calculate grade as 30% of writtenOutput, 30% of performanceTask, and 40% of exam
            grade = 0.3 * written_output + 0.3 * form.cleaned_data['performanceTask'] + 0.4 * exam

            # Save the calculated values to the form instance
            form.instance.writtenOutput = written_output
            form.instance.exam = exam
            form.instance.grade = grade

            # Save the form
            form.save()

            # Notify the student using WebSocket
            channel_layer = get_channel_layer()
            
            print("Before group_send")
            
            async_to_sync(channel_layer.group_send)(
                f"student_{student_name}",
                {
                    'type': 'notify.grade_change',
                    'student_name': student_name,
                    'new_grade': grade,
                }
            )
            
            print("After group_send")

            # Display success message
            messages.success(request, f"Successfully Encoded {student_fullName}")

            # Redirect to the 'unit' page
            return redirect('unit', faculty_name=student.instructor_fullName, subject=student.subject, course=course)
    else:
        form = ThirdYearForm(instance=student)

    faculty_name=student.instructor_fullName

    return render(request, 'facultyEdit.html', {'form': form, 'course': course, 'student_fullName': student_fullName,'faculty_name':faculty_name})

def adminLogin(request):
    if request.method == 'POST':
        admin_username = request.POST.get('admin_username')
        admin_password = request.POST.get('admin_password')

        user = authenticate(request, username=admin_username, password=admin_password)

        if user is not None:
            login(request, user)
            # Redirect to the adminPage with the correct admin_username
            return redirect('adminPage', admin_username=admin_username)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'adminLogin.html')

def adminPage(request, admin_username):
    try:
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the username from the URL matches the username of the logged-in user
            if request.user.username != admin_username:
                # Log out the current user
                logout(request)
                messages.info(request, "Authorized Timed Out, Please Log-in Again")
                return redirect('adminLogin')

            # If the user is authenticated and the usernames match, continue with rendering the adminPage
            return render(request, 'adminPage.html', {'admin_username': admin_username})
        else:
            # If the user is not authenticated, redirect to the login page
            return redirect('adminLogin')

    except User.DoesNotExist:
        messages.error(request, "Admin User does not exist")
        return redirect('adminLogin')


def assign(request,admin_username):
    if request.user.is_authenticated:
    
        if request.user.username != admin_username:
                # Log out the current user
                logout(request)
                messages.info(request, "Authorized Timed Out, Please Log-in Again")
                return redirect('adminLogin')
        
        else:

            if request.method == 'POST':
                form = ThirdYearFormAssign(request.POST)
                if form.is_valid():
                    # Concatenate instructor first name and last name to create full name
                    form.instance.instructor_fullName = form.cleaned_data['instructor_firstName'] + form.cleaned_data['instructor_lastName']
                    
                    # Concatenate student first name and last name to create full name
                    form.instance.student_fullName = form.cleaned_data['student_firstName'] + form.cleaned_data['student_lastName']
                    form.save()
                    messages.success(request, "Student-Instructor assigned successfully.")

                    return redirect(reverse('adminPage', kwargs={'admin_username': admin_username}))
            else:
                form = ThirdYearFormAssign()

            return render(request, 'assignRegister.html', {'form': form, 'admin_username': admin_username})
        
    return redirect('adminLogin')

def student_profile(request, student_name):
    try:
        student = Student.objects.get(name=student_name.replace(' ', ''))  # Assuming 'name' is the field in your Student model
        username = student.username

        if request.user.is_authenticated and request.user.username != username:
            logout(request)
            messages.info(request, "Authorized Timed Out, Please Log-in Again")
            return redirect('home')

        return render(request, 'student_profile.html', {'student': student})

    except Student.DoesNotExist:
        messages.error(request, "Student does not exist")
        return redirect('home')
    
def mail_message(request, student_name, instructor_name):
    try:
        student = Student.objects.get(name=student_name.replace(' ', ''))

        username = student.username

        if request.user.is_authenticated and request.user.username != username:
            logout(request)
            messages.info(request, "Authorized Timed Out, Please Log-in Again")
            return redirect('home')

        form = mailForms(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                # Set the values on the form instance before saving
                form.instance.instructor_fullName = instructor_name
                form.instance.student_fullName = student_name
                form.instance.to_prof = True
                form.instance.to_student= False
                form.save()
                messages.success(request, "Mail sent Successfully.")
                return redirect('student', student_name=student_name)

        return render(request, 'mail_message.html', {'form': form, 'student_name': student_name, 'instructor_name': instructor_name})

    except Student.DoesNotExist:
        messages.error(request, "Student does not exist")
        return redirect('home')


def mail_student(request, student_name):
    try:
        student = Student.objects.get(name=student_name.replace(' ', ''))

        username = student.username

        if request.user.is_authenticated and request.user.username != username:
            logout(request)
            messages.info(request, "Authorized Timed Out, Please Log-in Again")
            return redirect('home')

        mails_inbox = Mail.objects.filter(student_fullName=student_name, to_student=True, is_deleted=False)
        mails_sent = Mail.objects.filter(student_fullName=student_name, to_prof=True, is_deleted=False)

        return render(request, 'mail_student.html', {'mails_inbox': mails_inbox, 'mails_sent': mails_sent, 'student_name': student_name})

    except Student.DoesNotExist:
        messages.error(request, "Student does not exist")
        return redirect('home')

def delete_mail(request, mail_id):
    mail = get_object_or_404(Mail, id=mail_id)
    mail.is_deleted = True
    mail.save()
    messages.success(request, "Mail deleted successfully.")
    return redirect('mail_student', student_name=mail.student_fullName)


def mail_message_faculty(request, student_name, instructor_name):
    try:
        faculty = Faculty.objects.get(name=instructor_name.replace(' ', ''))

        username = faculty.username

        if request.user.is_authenticated and request.user.username != username:
            logout(request)
            messages.info(request, "Authorized Timed Out, Please Log-in Again")
            return redirect('home')

        form = mailForms(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                # Set the values on the form instance before saving
                form.instance.instructor_fullName = instructor_name
                form.instance.student_fullName = student_name
                form.instance.to_prof = False
                form.instance.to_student = True
                form.save()
                messages.success(request, "Mail sent Successfully.")
                return redirect('facultyPage', faculty_name=instructor_name)

        return render(request, 'mail_message_faculty.html', {'form': form, 'student_name': student_name, 'instructor_name': instructor_name})

    except Faculty.DoesNotExist:  # Fix the exception to use Faculty.DoesNotExist
        messages.error(request, "Faculty does not exist")  # Change the error message accordingly
        return redirect('home')

def faculty_profile(request, instructor_name):
    try:
        faculty = Faculty.objects.get(name=instructor_name.replace(' ', ''))  # Assuming 'name' is the field in your Student model
        username = faculty.username

        if request.user.is_authenticated and request.user.username != username:
            logout(request)
            messages.info(request, "Authorized Timed Out, Please Log-in Again")
            return redirect('home')

        return render(request, 'faculty_profile.html', {'faculty': faculty})

    except Student.DoesNotExist:
        messages.error(request, "Student does not exist")
        return redirect('home')
    
def mail_faculty(request, instructor_name):
    try:
        faculty = Faculty.objects.get(name=instructor_name.replace(' ', ''))

        username = faculty.username

        if request.user.is_authenticated and request.user.username != username:
            logout(request)
            messages.info(request, "Authorized Timed Out, Please Log-in Again")
            return redirect('home')

        # Filter thirdYear instances based on instructor_fullName
        thirdyear_instances = thirdYear.objects.filter(instructor_fullName=instructor_name)

        mails_inbox = Mail.objects.filter(instructor_fullName=instructor_name, to_student=True, is_deleted=False)
        mails_sent = Mail.objects.filter(instructor_fullName=instructor_name, to_prof=True, is_deleted=False)

        return render(request, 'mail_faculty.html', {'mails_inbox': mails_inbox, 'mails_sent': mails_sent, 'instructor_name': instructor_name, 'thirdyear_instances': thirdyear_instances})

    except Faculty.DoesNotExist:
        messages.error(request, "Faculty does not exist")
        return redirect('home')


def predict(request, admin_username):
    if request.user.is_authenticated:
        if request.user.username != admin_username:
            logout(request)
            messages.info(request, "Authorized Timed Out, Please Log-in Again")
            return redirect('adminLogin')
        else:
            try:
                # Use the correct query based on your Django model
                thirdyear_instances = thirdYear.objects.all()

                if thirdyear_instances.exists():
                    # Load data into DataFrame using the Django ORM
                    df = pd.DataFrame.from_records([instance.__dict__ for instance in thirdyear_instances])

                    # Check if the DataFrame is not empty and contains the expected columns
                    if not df.empty and all(col in df.columns for col in ['prelim', 'midterm', 'finals', 'grade']):
                        # Features and target variable
                        X = df[['prelim', 'midterm', 'finals']]
                        y = df['grade']

                        # Linear regression model
                        model = LinearRegression()
                        model.fit(X, y)

                        # Predictions
                        predicted = model.predict(X)

                        # Plotting
                        plt.figure(figsize=(10, 6))
                        plt.scatter(y, predicted, color='blue', edgecolor='black', s=20, label='Predicted Grades')
                        plt.scatter(y, y, color='red', edgecolor='black', s=20, label='Actual Grades')

                        plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
                        plt.xlabel('Actual Grades')
                        plt.ylabel('Predicted Grades')
                        plt.title('Actual vs Predicted Grades')
                        plt.legend()
                        plt.grid(True)
                        plt.show()

                        return render(request, 'adminPage.html', {'admin_username': admin_username,})
                    else:
                        # Handle the case where DataFrame is empty or doesn't have the expected columns
                        messages.error(request, "Error loading data from the database")
                        return redirect('adminLogin')
                else:
                    # Handle the case where there are no instances in the database
                    messages.error(request, "No data found in the database")
                    return redirect('adminLogin')

            except Exception as e:
                # Handle any other exceptions that might occur
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('adminLogin')

    return redirect('adminLogin')

def units(request,admin_username):
    if request.user.is_authenticated:
    
        if request.user.username != admin_username:
                # Log out the current user
                logout(request)
                messages.info(request, "Authorized Timed Out, Please Log-in Again")
                return redirect('adminLogin')
        
        else:

            if request.method == 'POST':
                form = unitForms(request.POST)
                if form.is_valid():
                    # Concatenate instructor first name and last name to create full name
                    form.instance.instructor_fullName = form.cleaned_data['instructor_firstName'] + form.cleaned_data['instructor_lastName']

                    form.save()
                    messages.success(request, "Unit assigned successfully.")

                    return redirect(reverse('adminPage', kwargs={'admin_username': admin_username}))
            else:
                form = unitForms()

            return render(request, 'adminUnits.html', {'form': form, 'admin_username': admin_username})
        
    return redirect('adminLogin')
