from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from urllib.parse import urlencode
from utils import mailing
import uuid
import datetime
import pytz


class Profile(models.Model):
    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE)
    uuid = models.UUIDField(null=False, blank=False)
    registered = models.DateField(verbose_name='registration_date', auto_now=True) # дата регистрации, не меняется
    last_update = models.DateField(verbose_name='last_update', auto_now_add=True)
    #email = models.EmailField(max_length=254)
    verified = models.BooleanField(default=False)

    # TODO: Добавить возможность смены мейла
    # TODO: Решить вопросы с таймзоной

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        while not self.uuid:
            uid = str(uuid.uuid4())
            _user = Profile.objects.filter(uuid=uid)
            if not _user.exists():
                self.uuid = uid


    class Meta:
        unique_together = ('user', 'uuid')
        verbose_name = ('user account')
        verbose_name_plural = ('user accounts')

class EmailConfirmation(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    email_adress = models.EmailField(max_length=200, unique=True, primary_key=True)
    key_ref = models.CharField(max_length=64, unique=True)
    sent = models.DateTimeField(blank=True)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.sent:
            self.key_ref = mailing.generate_ref()
            self.send()


    def key_expired(self):
        utc = pytz.UTC
        expiration_date = self.sent + datetime.timedelta(days = 1)
        return expiration_date < utc.localize(datetime.datetime.now())

    def confirm(self):
        if not self.key_expired() and not self.user.verified:
            self.user.verified = True
            self.delete() # СУЕЦЫД - объект удаляется

    def send(self, **kwargs):
        current_site = "127.0.0.1:8000" # пока так
        #current_site = kwargs["site"] if "site" in kwargs else Site.objects.get_current()
        # protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        protocol = "http"
        #code = urlencode({"code": self.key_ref})
        code = self.key_ref
        signup_url = f"{protocol}://{current_site}/confirm/{code}"
        #signup_url = f"{protocol}://{current_site.domain}confirm?{code}"
        ctx = {'url': signup_url}
        mailing.send_confirmation_email(self.email_adress, ctx)
        self.sent = timezone.now()
        self.save()