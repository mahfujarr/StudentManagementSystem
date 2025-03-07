from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def list(request):
    return render(request, 'student-list.html')

def add(request):
    return render(request, 'student-add.html')

def edit(request):
    return render(request, 'student-edit.html')

def details(request):
    return render(request, 'student-details.html')

def fees_collections(request):
    return render(request, 'fees-collections.html')

def add_fees_collection(request):
    return render(request, 'add-fees-collection.html')
