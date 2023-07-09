from django.db import models
from django.contrib.auth.models import User

class Track(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tracks")
    prompt = models.CharField(max_length=255, null=False)
    track = models.FileField(upload_to='tracks/%Y-%m-%d', null=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.created_on}] {self.prompt} - {self.track} by {self.owner.username}"
    

    def serialize(self):
        return {
            "id": self.id,
            "owner": self.owner.username,
            "prompt": self.prompt,
            "track": str(self.track.url),
            "created_on": self.created_on.strftime("%b %d %Y, %I:%M %p")
        }
