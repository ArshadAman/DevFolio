from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import searchProject, paginate
from .models import Project, Review
from .forms import ProjectForm, ReviewForm
# Create your views here.

# Global Variable

def projects(request):
    projects,search_query = searchProject(request)
    custom_range, projects = paginate(request, projects, 10)
    context = {'projects': projects, 'search_query': search_query,'custom_range':custom_range}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id = pk)

    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = projectObj
            review.owner = request.user.profile
            review.save()

            projectObj.getVotes
            
            messages.success(request, 'Your Review is successfully submitted!')

    tags = projectObj.tags.all()
    review = projectObj.review_set.all()
    return render(request, 'projects/singleProject.html', {'project': projectObj, 'tags': tags, 'reviews':review, 'form': form})

@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/projectForm.html', context)

@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id = pk)
    form = ProjectForm(instance = project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/projectForm.html', context)

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id = pk)
    context = {'object': project}
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    return render(request, 'delete_template.html', context)

# Handle Comments