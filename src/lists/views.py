from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


from lists.forms import ExistingListItemForm, ItemForm, ShareForm
from lists.models import List


User = get_user_model()


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html", {"form": ItemForm()})


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    our_list = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=our_list)

    if request.method == "POST":
        form = ExistingListItemForm(for_list=our_list, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(our_list)
    share_form = ShareForm()
    return render(
        request, "list.html", {"list": our_list, "form": form, "share_form": share_form}
    )


def new_list(request: HttpRequest) -> HttpResponse:
    form = ItemForm(data=request.POST)
    if form.is_valid():
        nulist = List.objects.create()
        if request.user.is_authenticated:
            nulist.owner = request.user
            nulist.save()
        form.save(for_list=nulist)
        return redirect(nulist)
    else:
        return render(request, "home.html", {"form": form})


def my_lists(request: HttpRequest, email: str) -> HttpResponse:
    owner = User.objects.get(email=email)
    return render(request, "my_lists.html", {"owner": owner})


def share_list(request: HttpRequest, list_id: int) -> HttpResponse:
    list_ = List.objects.get(id=list_id)
    form = ShareForm(data=request.POST)
    if form.is_valid():
        sharee_email = form.cleaned_data["sharee"]
        sharee, _ = User.objects.get_or_create(email=sharee_email)
        list_.shared_with.add(sharee)
        return redirect(list_)
    return render(
        request,
        "list.html",
        {
            "list": list_,
            "form": ExistingListItemForm(for_list=list_),
            "share_form": form,
        },
    )
