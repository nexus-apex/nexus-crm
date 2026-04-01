from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Contact, Deal, Activity
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusCRM with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexuscrm.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Contact.objects.count() == 0:
            for i in range(10):
                Contact.objects.create(
                    name=["Rajesh Kumar","Priya Sharma","Amit Patel","Deepa Nair","Vikram Singh","Ananya Reddy","Suresh Iyer","Meera Joshi","Karthik Rao","Fatima Khan"][i],
                    company=["TechVision Pvt Ltd","Global Solutions","Pinnacle Systems","Nova Enterprises","CloudNine Solutions","MetaForge Inc","DataPulse Analytics","QuantumLeap Tech","SkyBridge Corp","Zenith Innovations"][i],
                    email=f"demo{i+1}@example.com",
                    phone=f"+91-98765{43210+i}",
                    status=random.choice(["lead", "customer", "prospect", "churned"]),
                    source=random.choice(["website", "referral", "social", "direct"]),
                    value=round(random.uniform(1000, 50000), 2),
                    notes=f"Sample notes for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Contact records created'))

        if Deal.objects.count() == 0:
            for i in range(10):
                Deal.objects.create(
                    title=f"Sample Deal {i+1}",
                    company=["TechVision Pvt Ltd","Global Solutions","Pinnacle Systems","Nova Enterprises","CloudNine Solutions","MetaForge Inc","DataPulse Analytics","QuantumLeap Tech","SkyBridge Corp","Zenith Innovations"][i],
                    value=round(random.uniform(1000, 50000), 2),
                    stage=random.choice(["qualification", "proposal", "negotiation", "won", "lost"]),
                    probability=random.randint(1, 100),
                    expected_close=date.today() - timedelta(days=random.randint(0, 90)),
                    notes=f"Sample notes for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Deal records created'))

        if Activity.objects.count() == 0:
            for i in range(10):
                Activity.objects.create(
                    subject=f"Sample Activity {i+1}",
                    related_to=f"Sample {i+1}",
                    activity_type=random.choice(["call", "email", "meeting", "task", "note"]),
                    scheduled=date.today() - timedelta(days=random.randint(0, 90)),
                    done=random.choice([True, False]),
                    notes=f"Sample notes for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 Activity records created'))
