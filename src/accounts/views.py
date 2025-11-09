from django.contrib import auth, messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse

from django.conf import settings

from accounts.models import Token, User


def send_login_email(request):
    email = request.POST["email"]
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse("login") + "?token=" + str(token.uid)
    )
    send_mail(
        "Your login link for Superlists",
        f"Use this link to log in:\n\n{url}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in.",
    )
    return redirect("/")


def login(request):
    if user := auth.authenticate(uid=request.GET["token"]):
        auth.login(request, user)
    else:
        messages.error(request, "Invalid login link, please request a new one")
    return redirect("/")
