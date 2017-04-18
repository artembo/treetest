from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from tree.models import Referat
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

@receiver(post_delete, sender=Referat)
@receiver(post_save, sender=Referat)
def clear_cache(sender, **kwargs):
	key = make_template_fragment_key('branches', Referat.objects.values('pk'))
	cache.delete(key)