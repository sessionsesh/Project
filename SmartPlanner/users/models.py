from django.db import models
from django.contrib.auth.models import User
import uuid


class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if (postData['login'].isalpha()) == False:
            if len(postData['first_name']) < 2:
                errors['first_name'] = "First name can not be shorter than 2 characters"

        if len(postData['email']) == 0:
            errors['email'] = "You must enter an email"

        if len(postData['password']) < 8:
            errors['password'] = "Password is too short!"

        return errors

class Profile(models.Model):
    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE)
    uuid = models.UUIDField(null=False, blank=False)
    registered = models.DateField(verbose_name='registration_date', auto_now=True) # дата регистрации, не меняется
    last_update = models.DateField(verbose_name='last_update', auto_now_add=True)
    email = models.EmailField(max_length=254)

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