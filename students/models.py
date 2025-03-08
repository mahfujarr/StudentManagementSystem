from django.db import models
from django.utils import timezone
import os
import re

#Functions
def student_image_path(instance, filename):
    ext = filename.split('.')[-1]
    # Use a safe filename based on student ID
    safe_id = re.sub(r'[^a-zA-Z0-9]', '_', str(instance.student_id))
    filename = f"{safe_id}.{ext}"
    return os.path.join('student_img', filename)

# Create your models here.
class Student(models.Model):
    f_name = models.CharField(max_length=255, verbose_name="First Name")
    l_name = models.CharField(max_length=255, verbose_name="Last Name")
    student_id = models.CharField(max_length=20, verbose_name="Student ID", unique=True)
    gender = models.CharField(max_length=10, choices=[('Male','Male'), ('Female', 'Female'), ('Others', 'Others') ])
    dob = models.DateField(verbose_name="Date of Birth")
    current_year = timezone.now().year
    year = int(str(current_year)[-2:])  # Convert to int
    month = timezone.now().month
    student_session = models.CharField(
        max_length=10, 
        choices=[
            (f"{year - 1}-JUL", f"{year - 1}-JUL"), 
            (f"{year}-JAN", f"{year}-JAN"), 
            (f"{year}-JUL", f"{year}-JUL"), 
            (f"{year + 1}-JAN", f"{year + 1}-JAN")
        ], verbose_name="Session",default = f"{year}-JAN" if month <= 6 else f"{year}-JUL")
    religion = models.CharField(max_length=10)
    joining_date = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=64)
    image = models.ImageField(upload_to=student_image_path, blank=True, null=True)
    father_name = models.CharField(max_length=255, verbose_name="Father's Name")
    father_occupation = models.CharField(max_length=50, verbose_name="Father's Occupation")
    father_phone = models.CharField(max_length=15, verbose_name="Father's Phone")

    mother_name = models.CharField(max_length=255, verbose_name="Mother's Name")
    mother_occupation = models.CharField(max_length=50, verbose_name="Mother's Occupation")
    mother_phone = models.CharField(max_length=15, verbose_name="Mother's Phone")

    present_address = models.CharField(max_length=255)
    permanent_address = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_image = Student.objects.get(pk=self.pk).image
                if old_image and old_image.name != self.image.name:
                    old_image.delete(save=False)
            except Student.DoesNotExist:
                pass
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.f_name} {self.l_name}"
    
class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="fees")
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    # due_date = models.DateField()
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(default=timezone.now, blank=True, null=True)
    # transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        status = "Paid" if self.paid else "Due"
        return f"{self.student.f_name} {self.student.l_name} - {status}"
