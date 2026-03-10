from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FeedbackForm
from django.core.mail import send_mail


def home(request):
    return HttpResponse("Welcome to my Fantasy Basketball Site!")


def leaderboard(request):
    return render(request, "main/leaderboard.html")


def about_feedback(request):

    if request.method == "POST":
        form = FeedbackForm(request.POST)

        if form.is_valid():
            feedback = form.save()

            send_mail(
                subject="New Crusher Fantasy Feedback",
                message=f"""
Name: {feedback.name}
Email: {feedback.email}

Message:
{feedback.message}
""",
                from_email=None,
                recipient_list=["crusherfantasy@outlook.com"],
                fail_silently=False,
            )

            return redirect("about_feedback")

    else:
        form = FeedbackForm()

    return render(request, "about_feedback.html", {"form": form})