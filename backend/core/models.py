from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=50, choices=[("lead", "Lead"), ("customer", "Customer"), ("prospect", "Prospect"), ("churned", "Churned")], default="lead")
    source = models.CharField(max_length=50, choices=[("website", "Website"), ("referral", "Referral"), ("social", "Social"), ("direct", "Direct")], default="website")
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Deal(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, default="")
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stage = models.CharField(max_length=50, choices=[("qualification", "Qualification"), ("proposal", "Proposal"), ("negotiation", "Negotiation"), ("won", "Won"), ("lost", "Lost")], default="qualification")
    probability = models.IntegerField(default=0)
    expected_close = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Activity(models.Model):
    subject = models.CharField(max_length=255)
    related_to = models.CharField(max_length=255, blank=True, default="")
    activity_type = models.CharField(max_length=50, choices=[("call", "Call"), ("email", "Email"), ("meeting", "Meeting"), ("task", "Task"), ("note", "Note")], default="call")
    scheduled = models.DateField(null=True, blank=True)
    done = models.BooleanField(default=False)
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.subject
