from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AddSkillsForm, CustomUserCreationForms, EditSkillsForm, MessageForm, ProfileForm
from .models import Profile
from .utils import searchUser
from projects.utils import paginate

# Create your views here.
def profiles(request):
    profiles, search_query = searchUser(request)
    custom_range, profiles = paginate(request, profiles, 10)
    context = {'profiles': profiles, 'search_query': search_query, 'custom_range':custom_range}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id = pk)
    if request.user.is_authenticated:
        if request.user.profile == profile:
            return userAccount(request)
    topSkills = profile.skill_set.exclude(description__exact ="")
    otherSkills = profile.skill_set.filter(description__exact ="")
    context = {'profile': profile, 'topSK': topSkills, 'otherSk': otherSkills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    project = profile.project_set.all()
    context = {'profile': profile, 'skills': skills, 'project': project}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)

# Handling Authentication
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')


    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username doesn't exits")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, "Incorrect Password..... Try to remember otherwise fuck off....")
    
    return render(request, 'users/login_register.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.info(request, "User is successfully logged out...")
    return redirect('login')

def regiaterUser(request):
    page = 'register'
    form = CustomUserCreationForms()

    if request.method == "POST":
        form = CustomUserCreationForms(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account is created...')
            
            login(request, user)
            return redirect('edit-account')
        # else:
        #     messages.error(request, 'An error has occured during registration...')

    context = {"page": page, 'form': form}
    return render(request, 'users/login_register.html', context)


# Skills CRUD Operatons
@login_required(login_url='login')
def addSkills(request):
    profile = request.user.profile
    form = AddSkillsForm()
    todo = 'add'
    if request.method == 'POST':
        form = AddSkillsForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect('account')
    context = {'todo': todo,'form': form}
    return render(request, 'users/skills.html', context)

@login_required(login_url='login')
def editSkills(request, pk):
    todo = 'edit'
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = EditSkillsForm(instance=skill)
    if request.method == 'POST':
        form = EditSkillsForm(request.POST, instance = skill)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'todo': todo,"form": form}
    return render(request, 'users/skills.html', context)

@login_required(login_url='login')
def deleteSkills(request, pk):
    current_user = request.user.profile
    skill = current_user.skill_set.get(id = pk)
    context = {'object': skill}
    if request.method == 'POST':
        skill.delete()
        return redirect('account')
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unReadCount = messageRequests.filter(is_read = False).count()
    context = {'messageRequest': messageRequests, 'unReadCount': unReadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)

def sendMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit= False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, 'Your message has been sent')

            return redirect('user-profile', recipient.id)
    context = {'form':form, 'reciepient': recipient}
    return render(request, 'users/messageForm.html', context)
