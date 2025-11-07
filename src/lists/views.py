from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from lists.forms import ItemForm
from lists.models import Item, List


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html", {"form": ItemForm()})


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    our_list = List.objects.get(id=list_id)
    form = ItemForm()
    
    if request.method == "POST":
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=our_list)
            return redirect(our_list)
    return render(request, "list.html", {"list": our_list, "form": form})


def new_list(request: HttpRequest) -> HttpResponse:
    form = ItemForm(data=request.POST)
    if form.is_valid():
        nulist = List.objects.create()
        form.save(for_list=nulist)
        return redirect(nulist)
    else:
        return render(request, "home.html", {"form": form})
