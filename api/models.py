# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "Customer"
        AGENT = "AGENT", "Agent"

    base_role = Role.CUSTOMER

    role = models.CharField(max_length=50, choices=Role.choices, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.is_superuser:
                self.role = self.Role.ADMIN
            else:
                self.role = self.base_role
        return super().save(*args, **kwargs)


class CustomerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CUSTOMER)


class Customer(User):
    base_role = User.Role.CUSTOMER

    customer = CustomerManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for customers"


class CustomerProfile(models.Model):
    phone_number = models.CharField("phone number", max_length=15, blank=True, null=True)
    location = models.IntegerField(default=None, blank=True, null=True)

    customer = models.OneToOneField(Customer,
                                on_delete=models.CASCADE)

    @receiver(post_save, sender=Customer)
    def create_user_profile(sender, instance, created, **kwargs):
        if created and instance.role == User.Role.CUSTOMER:
            CustomerProfile.objects.get_or_create(user=instance)


class AgentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.AGENT)


class Agent(User):
    base_role = User.Role.AGENT

    agent = AgentManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Agents"


class AgentProfile(models.Model):
    name = models.CharField("name", max_length=150, blank=True, null=True)
    phone_number = models.CharField("phone number", max_length=15, blank=True, null=True)
    location = models.IntegerField(default=None, blank=True, null=True)
    availability = models.BooleanField("availability", blank=True, default=True)

    agent = models.OneToOneField(Agent,
                                on_delete=models.CASCADE)

    # class Meta:
    #     ordering = ('created',)

    @receiver(post_save, sender=Agent)
    def create_user_profile(sender, instance, created, **kwargs):
        if created and instance.role == User.Role.AGENT:
            AgentProfile.objects.get_or_create(user=instance)

    @receiver(post_save, sender=Agent)
    def save_user_profile(sender, instance, **kwargs):
        instance.agentprofile.save()
