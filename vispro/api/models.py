from django.db import models
from django.utils.text import slugify
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class Api_Members(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    grade = models.CharField(max_length=1)
    slug = models.SlugField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_archived = models.BooleanField(null=True, blank=True, default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            content = 1
            while Api_Members.objects.filter(slug = slug).exists():
                slug = f"{base_slug}-{content}"
                content += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ArchivedOrder(models.Model):
    action = models.CharField(max_length=50)
    data = models.JSONField()
    archived_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.action