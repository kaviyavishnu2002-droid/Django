from django.contrib.auth.models import Group,Permission
from django.db.models.signals import post_save, post_delete,pre_delete, pre_save
from django.dispatch import receiver
from .models import Vis_Members,Vis_Member_Created_Details
from datetime import datetime

def create_group_permissions(sender, **kwargs):
    try:
        readers_group, created = Group.objects.get_or_create(name = "Readers")
        authors_group, created = Group.objects.get_or_create(name = "Authors")
        editors_group, created = Group.objects.get_or_create(name = "Editors")

        readers_permissions = [
            Permission.objects.get(codename = 'view_movies')
        ]
        authors_permissions = [
            Permission.objects.get(codename = 'add_movies'),
            Permission.objects.get(codename = 'change_movies'),
            Permission.objects.get(codename = 'delete_movies'),
        ]
        can_publish, created = Permission.objects.get_or_create(codename = 'can_publish', content_type_id = 23, name = 'can_publish_movies')

        editors_permissions = [
            can_publish,
            Permission.objects.get(codename = 'add_movies'),
            Permission.objects.get(codename = 'change_movies'),
            Permission.objects.get(codename = 'delete_movies'),
        ]

        readers_group.permissions.set(readers_permissions)
        authors_group.permissions.set(authors_permissions)
        editors_group.permissions.set(editors_permissions)
    except Exception as e:
        print(f"An error occured {e}")

@receiver(post_save, sender=Vis_Members)
def Vis_Members_Post_Save(sender, instance, created, **kwargs):
    print("signal trigered")
    if created:
        action = 'created'
    else:
        action = 'updated'

    print("action:",action)
    print("instance:", instance)
    Vis_Member_Created_Details.objects.create(
        name = instance.name,
        about_creation = f"{action} to {instance.name} {instance.updated_at}"
    )

@receiver(post_delete, sender=Vis_Members)
def Vis_Members_Post_Delete(sender, instance, **kwargs):
    print("signal trigered")
    action = 'deleted'
    print("action:",action)
    print("instance:", instance)
    Vis_Member_Created_Details.objects.create(
        name = instance.name,
        about_creation = f"{action} to {instance.name} at {datetime.now()}"
    )

@receiver(pre_delete, sender=Vis_Members)
def Vis_Members_Pre_Delete(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)
