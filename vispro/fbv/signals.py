from django.db.models.signals import post_save, pre_save, post_delete, pre_delete, m2m_changed
from django.dispatch import receiver
from .models import Detail, All_detail
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        All_detail.objects.create(
            detail = f"New user created(post save method): {instance.username}", 
            detail_time = timezone.now()
        )

@receiver(pre_save, sender=User)
def create_profile(sender, instance, **kwargs):
    All_detail.objects.create(
        detail = f"New user created(pre save method): {instance.username}", 
        detail_time = timezone.now()
    )

@receiver(pre_save, sender=Detail)
def set_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = instance.name.lower().replace(" ", "-")
        All_detail.objects.create(
            detail = f"create slug and Detail created(pre save method): {instance.name}", 
            detail_time = timezone.now()
        )
        return
    All_detail.objects.create(
        detail = f"New detail created(pre save method): {instance.name}", 
        detail_time = timezone.now()
    )

@receiver(post_delete, sender=Detail)
def delete_product_files(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
'''
@receiver(m2m_changed, sender=Detail.tags.through)
def tags_changed(sender, instance, action, **kwargs):
    if action == "post_add":
        print(f"Tags added to {instance.name}")'''
'''
@receiver(post_save, sender=User, dispatch_uid="create_user_profile")
def create_profile(sender, instance, created, **kwargs):'''