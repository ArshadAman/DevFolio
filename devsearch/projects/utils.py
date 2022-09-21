from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Project, Tag
from django.db.models import Q
from users.models import Profile


def searchProject(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    tags = Tag.objects.filter(name__iexact=search_query)
    owner = Profile.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(Q(title__icontains=search_query) | Q(tags__in = tags) | Q(owner__in = owner))
    return projects, search_query

def paginate(request, query_set, results):
        # Paginator
    page = request.GET.get('page')
    paginator = Paginator(query_set, results)

    try:
        query_set = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        query_set = paginator.page(page)

    except EmptyPage:
        page = paginator.num_pages
        query_set = paginator.page(page)

    leftRange = int(page) - 4
    if leftRange < 1:
        leftRange = 1
    
    rightRange = int(page)+5
    if rightRange > paginator.num_pages:
        rightRange = paginator.num_pages+1
    
    custom_range = range(leftRange, rightRange)
    return custom_range, query_set