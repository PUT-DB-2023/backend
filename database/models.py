from email.policy import default
from enum import unique
from polymorphic.models import PolymorphicModel
from django.db import models
from django.db.models import CheckConstraint, Q, F
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

import smtplib, ssl
from email.message import EmailMessage


class CustomUserManager(UserManager):

    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        email = self.remove_accents_from_email(email)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        # email_subject = 'Konto w systemie'
        # email_content = f'Witaj {user.first_name} {user.last_name}! Twoje konto w systemie zostało utworzone. Twoje hasło to: {password}.'
        # user.send_email_gmail(user.email, email_subject, email_content)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)
    
    def remove_accents_from_email(self, email):
        accents = 'ŮôῡΒძěἊἦëĐᾇόἶἧзвŅῑἼźἓŉἐÿἈΌἢὶЁϋυŕŽŎŃğûλВὦėἜŤŨîᾪĝžἙâᾣÚκὔჯᾏᾢĠфĞὝŲŊŁČῐЙῤŌὭŏყἀхῦЧĎὍОуνἱῺèᾒῘᾘὨШūლἚύсÁóĒἍŷöὄЗὤἥბĔõὅῥŋБщἝξĢюᾫაπჟῸდΓÕűřἅгἰშΨńģὌΥÒᾬÏἴქὀῖὣᾙῶŠὟὁἵÖἕΕῨčᾈķЭτἻůᾕἫжΩᾶŇᾁἣჩαἄἹΖеУŹἃἠᾞåᾄГΠКíōĪὮϊὂᾱიżŦИὙἮὖÛĮἳφᾖἋΎΰῩŚἷРῈĲἁéὃσňİΙῠΚĸὛΪᾝᾯψÄᾭêὠÀღЫĩĈμΆᾌἨÑἑïოĵÃŒŸζჭᾼőΣŻçųøΤΑËņĭῙŘАдὗპŰἤცᾓήἯΐÎეὊὼΘЖᾜὢĚἩħĂыῳὧďТΗἺĬὰὡὬὫÇЩᾧñῢĻᾅÆßшδòÂчῌᾃΉᾑΦÍīМƒÜἒĴἿťᾴĶÊΊȘῃΟúχΔὋŴćŔῴῆЦЮΝΛῪŢὯнῬũãáἽĕᾗნᾳἆᾥйᾡὒსᾎĆрĀüСὕÅýფᾺῲšŵкἎἇὑЛვёἂΏθĘэᾋΧĉᾐĤὐὴιăąäὺÈФĺῇἘſგŜæῼῄĊἏØÉПяწДĿᾮἭĜХῂᾦωთĦлðὩზკίᾂᾆἪпἸиᾠώᾀŪāоÙἉἾρаđἌΞļÔβĖÝᾔĨНŀęᾤÓцЕĽŞὈÞუтΈέıàᾍἛśìŶŬȚĳῧῊᾟάεŖᾨᾉςΡმᾊᾸįᾚὥηᾛġÐὓłγľмþᾹἲἔбċῗჰხοἬŗŐἡὲῷῚΫŭᾩὸùᾷĹēრЯĄὉὪῒᾲΜᾰÌœĥტ'
        ascii_replacements = 'UoyBdeAieDaoiiZVNiIzeneyAOiiEyyrZONgulVoeETUiOgzEaoUkyjAoGFGYUNLCiIrOOoqaKyCDOOUniOeiIIOSulEySAoEAyooZoibEoornBSEkGYOapzOdGOuraGisPngOYOOIikoioIoSYoiOeEYcAkEtIuiIZOaNaicaaIZEUZaiIaaGPKioIOioaizTIYIyUIifiAYyYSiREIaeosnIIyKkYIIOpAOeoAgYiCmAAINeiojAOYzcAoSZcuoTAEniIRADypUitiiIiIeOoTZIoEIhAYoodTIIIaoOOCSonyKaAsSdoACIaIiFIiMfUeJItaKEISiOuxDOWcRoiTYNLYTONRuaaIeinaaoIoysACRAuSyAypAoswKAayLvEaOtEEAXciHyiiaaayEFliEsgSaOiCAOEPYtDKOIGKiootHLdOzkiaaIPIIooaUaOUAIrAdAKlObEYiINleoOTEKSOTuTEeiaAEsiYUTiyIIaeROAsRmAAiIoiIgDylglMtAieBcihkoIrOieoIYuOouaKerYAOOiaMaIoht'
        translator = str.maketrans(accents, ascii_replacements)
        return email.translate(translator)


class User(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def _validate_email(self, email):
        try:
            validate_email(email)
        except ValidationError:
            return False
        return True
    
    def send_email_gmail(self, receiver, subject, message):
        msg = EmailMessage()
        msg.set_content(f'{message}')

        msg['Subject'] = subject
        msg['From'] = "" "FILL WITH SENDER EMAIL"
        sender_password = "" # FILL WITH SENDER PASSWORD
        msg['To'] = receiver

        # Send the message via our own SMTP server.
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(msg['From'], sender_password)
        server.send_message(msg)
        server.quit()

    def send_email_zimbra(self, receiver, subject, message):

        port = 587  # For starttls
        smtp_server = "poczta.student.put.poznan.pl"
        sender_email = "" # FILL WITH EMAIL SENDER
        receiver_email = receiver
        password = "" # FILL WITH PASSWORD
        message = f'Subject: {subject}\n\n{message}'

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.encode('utf-8'))

    


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')

    student_id = models.CharField(max_length=6, unique=True)
    major = models.ForeignKey('Major', on_delete=models.SET_NULL, blank=True, null=True, related_name='students')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Major(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=50, unique=True)
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, blank=True, null=True, related_name='courses')
    description = models.CharField(max_length=255, blank=True, default='')
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        print(f"Saving course {self.name}")
        # check if self.editions.all() is empty
        if self.editions.all():
            print(f"Editions: {self.editions.all()}")
            for edition in self.editions.all():
                if edition.semester.active:
                    print(f"Found an active semester: {edition.semester}")
                    self.active = True
                    break
                else:
                    print(f"Found an inactive semester: {edition.semester}")
                    self.active = False
        else:
            print(f"No editions found for course: {self}")
            self.active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Semester(models.Model):
    start_year = models.IntegerField()
    winter = models.BooleanField(default=True)
    active = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['start_year', 'winter'], name='unique_semester'),
            models.CheckConstraint(check=Q(start_year__gte=2000) & Q(start_year__lte=3000), name='start_year_between_2020_and_3000'),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for course in Course.objects.all():
            print(f"Checking course: {course}")
            course.save()
    
    # override update method to check if it can be activated
    # def update(self, *args, **kwargs):
    #     print(f"Updating semester: {self}, {self.active}")
    #     if Semester.objects.filter(active=True).count() == 0:
    #         print(f"No active semester found, activating semester: {self}")
    #         self.active = True

    #     super().update(*args, **kwargs)
    
    # override delete method to disallow deletion of an active semester
    def delete(self, *args, **kwargs):
        print("self.active: ", self.active)
        if self.active:
            print(f"Cannot delete active semester: {self}")
            raise Exception("Cannot delete an active semester")
        else:
            print(f"Deleting semester: {self}")
            super().delete(*args, **kwargs)
        for course in Course.objects.all():
            print(f"Checking course: {course}")
            course.save()
    
    def __str__(self):
        # return year and winter if self.winter=True, else return year and summer
        return f"{self.start_year}/{self.start_year + 1} - {'zima' if self.winter else 'lato'}"

class Edition(models.Model):
    description = models.CharField(max_length=255, blank=True, default='')
    date_opened = models.DateField(blank=True, null=True)
    date_closed = models.DateField(blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='editions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='editions')
    teachers = models.ManyToManyField(Teacher, through='TeacherEdition', blank=True, related_name='editions')
    # servers = models.ManyToManyField('Server', through='EditionServer', blank=True, related_name='editions')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'semester'], name='unique_edition'),
        ]

    def save(self, *args, **kwargs):
        print(f"Before save:\nCourse: {self.course}, Course active: {self.course.active}, semester active: {self.semester.active}")
        super().save(*args, **kwargs)
        self.course.save()
        print(f"After save:\nCourse: {self.course}, Course active: {self.course.active}, semester active: {self.semester.active}")

    # override delete method to check if the course is active
    def delete(self, *args, **kwargs):
        print(f"Deleting edition: {self}")
        super().delete(*args, **kwargs)
        print("Saving course")
        self.course.save()

    def __str__(self):
        return f"{self.course} - {self.semester}"


class TeacherEdition(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['teacher', 'edition'], name='unique_teacher_edition'),
        ]
    
    def __str__(self):
        return f"{self.teacher} - {self.edition}"


class Group(models.Model):
    name = models.CharField(max_length=50)
    day = models.CharField(max_length=30, blank=True, default='')
    hour = models.CharField(max_length=30, blank=True, default='')
    room = models.CharField(max_length=30, blank=True, default='')
    teacherEdition = models.ForeignKey(TeacherEdition, on_delete=models.CASCADE, related_name='groups')
    students = models.ManyToManyField(Student, blank=True, related_name='groups')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['teacherEdition', 'name'], name='unique_group'),
        ]
    
    def __str__(self):
        return self.name


class DBMS(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return self.name


class Server(models.Model):
    name = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    port = models.CharField(max_length=255)
    # provider = models.CharField(max_length=30)
    dbms = models.ForeignKey(DBMS, on_delete=models.CASCADE, related_name='servers')
    user = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    database = models.CharField(max_length=255)
    date_created = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    editions = models.ManyToManyField(Edition, through='EditionServer', related_name='servers')

    create_user_template = models.CharField(max_length=1023, blank=True, default='')
    modify_user_template = models.CharField(max_length=1023, blank=True, default='')
    delete_user_template = models.CharField(max_length=1023, blank=True, default='')
    custom_command_template = models.CharField(max_length=1023, blank=True, default='')

    username_template = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.name} - {self.dbms.name}"


class EditionServer(models.Model):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    additional_info = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f"{self.edition} - {self.server}"


class DBAccount(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    additional_info = models.CharField(max_length=255, blank=True, default='')
    is_moved = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name='db_accounts')
    editionServer = models.ForeignKey(EditionServer, on_delete=models.CASCADE, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username', 'editionServer'], name='unique_username_editionserver'),
        ]
    
    def __str__(self):
        return self.username
