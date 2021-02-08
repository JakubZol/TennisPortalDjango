from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class PlayerManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, gender, weight, height, ntrp, plays, backhand, birthdate, password=None):
        if not email:
            raise ValueError("Field email is missing!")
        if not username:
            raise ValueError("Field username is missing!")
        if not first_name:
            raise ValueError("Field first_name is missing!")
        if not last_name:
            raise ValueError("Field last_name is missing!")
        if not gender:
            raise ValueError("Field gender is missing!")
        if not height:
            raise ValueError("Field height is missing!")
        if not weight:
            raise ValueError("Field weight is missing!")
        if not ntrp:
            raise ValueError("Field ntrp is missing!")
        if not plays:
            raise ValueError("Field plays is missing!")
        if not backhand:
            raise ValueError("Field backhand is missing!")
        if not birthdate:
            raise ValueError("Field birthdate is missing!")

        player = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            weight=weight,
            height=height,
            ntrp=ntrp,
            plays=plays,
            backhand=backhand,
            birthdate=birthdate
        )
        player.set_password(password)
        player.save(using=self._db)

        return player

    def create_superuser(self, email, username, first_name, last_name, gender, weight, height, ntrp, plays, backhand, birthdate, password):
        superuser = self.create_user(
            email=email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            weight=weight,
            height=height,
            ntrp=ntrp,
            plays=plays,
            backhand=backhand,
            birthdate=birthdate
        )
        superuser.is_admin = True
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save(using=self._db)

        return superuser


class Player(AbstractBaseUser):
    # required fields
    email = models.EmailField(verbose_name='email', unique=True, max_length=60)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    # custom fields
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    ntrp = models.FloatField(
        choices=[
            (1.0, '1'),
            (1.5, '1.5'),
            (2.0, '2'),
            (2.5, '2.5'),
            (3.0, '3'),
            (3.5, '3.5'),
            (4.0, '4'),
            (4.5, '4.5'),
            (5.0, '5'),
            (5.5, '5.5'),
            (6.0, '6'),
            (6.5, '6.5'),
            (7.0, '7'),
        ]
    )
    plays = models.CharField(
        max_length=1,
        choices=[
            ('L', 'Left-handed'),
            ('R', 'Right-handed'),
        ]
    )
    gender = models.CharField(
        max_length=1,
        choices=[
            ('M', 'Man'),
            ('W', 'Woman'),
        ]
    )
    height = models.IntegerField()
    weight = models.IntegerField()

    class Backhand(models.IntegerChoices):
        ONE_HANDED = 1
        TWO_HANDED = 2

    backhand = models.IntegerField(choices=Backhand.choices)
    birthdate = models.DateField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'gender', 'weight', 'height', 'ntrp', 'plays', 'backhand', 'birthdate']

    objects = PlayerManager()

    def __str__(self):
        return 'Player ' + str(self.username) + ': ' + self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

