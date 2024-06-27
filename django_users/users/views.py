from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, DetailView, ListView

from .forms import CreationForm, ProfileForm

User = get_user_model()


def send_activation_email(user, current_site):
    """Отправка активационного email пользователю."""

    subject = "Activate Your Account"
    message = render_to_string(
        "activation_email.html",
        {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
        },
    )
    user.email_user(subject, message)


def activate(request, uidb64, token):
    """Активация пользователя по ссылке."""

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
        user = None
    except User.DoesNotExist:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("login")
    else:
        return render(request, "activation_invalid.html")


class SignUp(CreateView):
    """Класс для регистрации пользователей."""

    form_class = CreationForm
    success_url = reverse_lazy("users:profile")
    template_name = "users/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        current_site = get_current_site(self.request)
        send_activation_email(user, current_site)
        return response


@login_required
def profile(request):
    """Класс демонстрации и изменения профиля пользователя."""

    if request.method == "POST":
        user_form = ProfileForm(request.POST, instance=request.user)
        if user_form.is_valid():
            new_email = user_form.cleaned_data.pop("new_email")
            if new_email:
                user = user_form.instance
                user.is_active = False
                user.email = new_email
                current_site = get_current_site(request)
                send_activation_email(user, current_site)
                user.save()
            user_form.save()
            return redirect("users:profile")
    else:
        user_form = ProfileForm(instance=request.user)
    context = {"user_form": user_form}
    return render(request, "profile.html", context)


class UserListView(ListView):
    """Страница с пользователями."""

    model = User
    template_name = "user_list.html"
    context_object_name = "users"
    paginate_by = 10


class UserProfileView(DetailView):
    """Страница пользователя."""

    model = User
    template_name = "user_detail.html"
