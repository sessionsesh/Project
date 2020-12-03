from django.core.mail import send_mail
#from django.template.loader import render_to_string
from django.template import Context, Template
from SmartPlanner import settings
import hashlib
import random
import os

def render_to_string(path, ctx):
    path = os.path.join(settings.BASE_DIR, path)
    with open(path, "r") as file:
        text = file.readlines()
        text = ''.join(text)
    template = Template(text)
    context = Context(ctx)
    return template.render(context)

def generate_ref(hash_func=hashlib.sha256):
    bits = str(random.SystemRandom().getrandbits(512)) # тут очень большое рандомное число
    return hash_func(bits.encode("utf-8")).hexdigest()

def generate_context(key_ref, type):
    current_site = "127.0.0.1:8000"  # пока так
    # current_site = kwargs["site"] if "site" in kwargs else Site.objects.get_current()
    # protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
    protocol = "http"
    # code = urlencode({"code": self.key_ref})
    code = key_ref
    signup_url = f"{protocol}://{current_site}/{type}/{code}"
    # signup_url = f"{protocol}://{current_site.domain}confirm?{code}"
    context = {'url': signup_url}
    return context

def send_confirmation_email(to, ctx):
    if not isinstance(to, list):
        to = [to]
    subject = render_to_string(r"templates\utils\email_confirmation_subject.txt", ctx) # Вставляем контекстные слова в шаблон
    subject = "".join(subject.splitlines())
    message = render_to_string(r"templates\utils\email_confirmation_message.txt", ctx) # Вставляем контекстные слова в шаблон
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)


def send_password_change_email(to, ctx):
    if not isinstance(to, list):
        to = [to]
    subject = render_to_string(r"templates\utils\password_change_subject.txt", ctx)
    subject = "".join(subject.splitlines())
    message = render_to_string(r"templates\utils\password_change_message.txt", ctx)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, to)
