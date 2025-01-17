from django.db import models
from django.contrib.auth.models import User

def upload_resource_path(instance, filename):
    return f"resources/agent_{instance.agent.name}_{instance.agent.creator}/{filename}"

# Create your models here.
class Agent(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agents')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('creator', 'name')

    def __str__(self):
        return f"Agent: {self.name}"

class Resource(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=upload_resource_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Interaction(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='interactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interactions', null=True, blank=True)
    query = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Interaction with {self.agent.name} at {self.timestamp}"

class Feedback(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')])
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Analytics(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='analytics')
    total_interactions = models.IntegerField(default=0)
    average_response_time = models.FloatField(default=0.0)
    last_interaction = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Analytics for {self.agent.name}"