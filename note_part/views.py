from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required

from .models import Note

class CustomRegisterView(FormView):
    template_name = "register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("edit_note")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(CustomRegisterView, self).form_valid(form)

    # def get(self, request):
    #     if self.request.user.is_authenticated:
    #         return redirect("edit_note")
    #     # return super(CustomRegisterView, self.get(*args, **kwargs))

def home(request):
    return redirect("/notes")

def about(request):
    return render(request, "about.html")

class CustomLoginView(LoginView):
    template_name = "login.html"
    field = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("edit_note") 

@login_required
def edit_note(request):
    note_id = int(request.GET.get("note_id", default=0))
    notes = Note.objects.all().filter(user=request.user)
    # Get data when form is submitted
    if request.method == "POST":
        note_id = int(request.POST.get("note_id", default=0))
        note_user = request.user
        note_title = request.POST.get("title", default="New Note")
        note_body = request.POST.get("body", "")

        if note_id > 0:  # Edit note
            note = Note.objects.get(pk=note_id)
            note.title = note_title
            note.body = note_body
            note.save()
            return redirect("/notes/?note_id=%i" % note_id)
        else:  # Create new note
            note = Note.objects.create(user=note_user, title=note_title, body=note_body)
            return redirect("/notes/?note_id=%i" % note.id)

    if note_id > 0:  # If it isn't the default
        note = Note.objects.get(pk=note_id)
    else:
        note = ""

    note_dic = {"note_id": note_id, "notes": notes, "note": note}

    return render(request, "edit_note.html", note_dic)

@login_required
def trash_note(request, note_id):
    if note_id > 0:
        note = Note.objects.get(pk=note_id)
        note.is_trashed = True
        note.save()
        return redirect("/notes/?note_id=0")

@login_required
def untrash_note(request, note_id):
    if note_id > 0:
        note = Note.objects.get(pk=note_id)
        note.is_trashed = False
        note.save()
        return redirect("/trash")

@login_required
def archive_note(request, note_id):
    if note_id > 0:
        note = Note.objects.get(pk=note_id)
        note.is_archived = True
        note.save()
        return redirect("/notes/?note_id=0")

@login_required
def unarchive_note(request, note_id):
    if note_id > 0:
        note = Note.objects.get(pk=note_id)
        note.is_archived = False
        note.save()
        return redirect("/archive")

@login_required
def delete_note(request, note_id):
    if note_id > 0:
        note = Note.objects.get(pk=note_id)
        note.delete()
        return redirect("/trash")

@login_required
def view_trash(request):
    note_id = int(request.GET.get("note_id", default=0))
    notes = Note.objects.all().filter(user=request.user)

    if note_id > 0:  # If it isn't the default
        note = Note.objects.get(pk=note_id)
    else:
        note = ""

    note_dic = {"note_id": note_id, "notes": notes, "note": note}

    return render(request, "view_trash.html", note_dic)

@login_required
def view_archive(request):
    note_id = int(request.GET.get("note_id", default=0))
    notes = Note.objects.all().filter(user=request.user)

    if note_id > 0:  # If it isn't the default
        note = Note.objects.get(pk=note_id)
    else:
        note = ""

    note_dic = {"note_id": note_id, "notes": notes, "note": note}

    return render(request, "view_archive.html", note_dic)
