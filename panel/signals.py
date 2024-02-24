# -*- encoding: utf-8 -*-
from django.dispatch import receiver
from django.db.models.signals import post_save

from panel.models import Teacher


@receiver(post_save, sender=Teacher)
def company_balance_change(sender, instance, created, raw, *args, **kwargs):
    """we can add this in this way or simply write in other file but in this case we should modify apps.py"""
    print('2. method post save')
    return None