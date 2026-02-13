from django.db import models
from django.contrib.auth.hashers import make_password , identify_hasher
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    # regex=r'^\d{10}$',
    regex=r'^[6-9]\d{9}$',
    message="Phone number must be a valid 10-digit Indian mobile number."
)

class Team(models.Model):
    TEAM_TYPE_CHOICES = (
        ('solo', 'Solo'),
        ('duo', 'Duo'),
    )

    team_id = models.CharField(max_length=50, unique=True)
    team_type = models.CharField(max_length=10, choices=TEAM_TYPE_CHOICES)
    password = models.CharField(max_length=128)
    
    payment_order_id = models.CharField(max_length=100, blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.BooleanField(default=False)
    
    email_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        try:
            identify_hasher(self.password)
        except Exception:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.team_id


class Player(models.Model):
    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    )
    
    BRANCH_CHOICES = [
        ("CSE", "CSE"),
        ("ECE", "ECE"),
        ("IT", "IT"),
        ("EEE", "EEE"),
        ("ME", "ME"),
        ("CE", "CE"),
        ("CSIT", "CSIT"),
        ("AIML", "AIML"),
        ("OTHERS", "OTHERS"),
    ]


    team = models.ForeignKey(Team, related_name="players", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, validators=[phone_validator])
    student_no = models.CharField(max_length=20, unique=True)
    roll_no = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    year = models.CharField(max_length=1, choices=[('1', '1st'), ('2', '2nd')])
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES)

    def __str__(self):
        return self.name
