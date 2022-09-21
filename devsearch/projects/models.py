from django.db import models
from users.models import Profile
import uuid

# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    desc = models.TextField(null= True, blank=True)
    featured_image = models.ImageField(null=True, blank = True, default = "default.jpg")
    demo_link = models.CharField(max_length=2000, blank=True, null=True)
    source_link = models.CharField(max_length=2000, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']

    @property
    def reviewers(self):
        query_set = self.review_set.all().values_list('owner__id', flat=True)
        return query_set

    @property
    def getVotes(self):
        reviews = self.review_set.all()
        upVote = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVote/totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner =models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete= models.CASCADE)
    body = models.TextField(null = True, blank=True)
    value = models.CharField(max_length=200, choices= VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'project']] #No instance of the review of can have the same owner and the same project.

    def __str__(self) -> str:
        return self.value

class Tag(models.Model):

    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.name


# ForeignKey establishes one to many relationships 
# For quering child in one to many RelatedField we use name_set: project.review_set.all()
# While quering many to many we use name only: project.tags.all()