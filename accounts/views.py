from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .models import CustomUser
from django.views.generic import CreateView,DetailView,UpdateView,DeleteView
from .forms import CustomUserCreationForm,UserUpdateForm
from django.urls import reverse
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView


class UserCreateAndLoginView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("tasks:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        correo_electronico = form.cleaned_data.get("correo_electronico")
        #username = form.cleaned_data.get("nombre_usario")
        raw_pw = form.cleaned_data.get("password1")
        user = authenticate(username=correo_electronico, password=raw_pw)
        if user is not None:
            login(self.request, user)
        return response
    
class UserDetail(DetailView):
    model = CustomUser
    template_name = 'accounts/user_detail.html'
    
#User=get_user_model
class UserUpdate(UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'accounts/templates_nameuser_edit.html'

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.kwargs['pk']})
 
class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'accounts/user_detail.html'
    
class PasswordChange(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    
class UserDelete(DeleteView):
    model = CustomUser
    template_name = 'accounts/user_delete.html'
    success_url = reverse_lazy('login')

# Create your views here.
