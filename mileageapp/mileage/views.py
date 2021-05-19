from django.shortcuts import render
from .models import Driver, Mileage
from django.db.models import Sum
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, timedelta
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#To avoid the float error. return zero
from django.db.models.functions import Coalesce
# Create your views here.

#Login, Logout, Register Views

#The Custom Login and Logout Views
def login_view(request):
    next = request.GET.get('next') #/premium/
    form = UserLoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            auth_user = authenticate(username=username, password=password)
            login(request, auth_user)
            messages.info(request, 'Succesfully Logged in.')
            if next:
                return redirect(next)
            return redirect('index')
    context = {
        'form': form
    }
    return render(request, "mileage/login.html", context)

def logout(request):
    return render(request, 'mileage/logout.html')

def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            auth_user = authenticate(username=user.username, password=password)
            login(request, auth_user)
            messages.info(request, 'Succesfully registered')
            if next:
                return redirect(next)
            return redirect('index')
    context = {
        'form': form
    }
    return render(request, 'mileage/signup.html', context)


@login_required(login_url='login/')
def index(request):
    driver = Driver.objects.filter(name=request.user)
    users_mileage = Mileage.objects.filter(user_name=request.user).aggregate(Sum('miles'))
    
    mileage_total = (users_mileage['miles__sum'])
    newest_miles = Mileage.objects.filter(user_name=request.user, timestamp__gte=datetime.now()-timedelta(hours=3))
  
    context = {
        'driver': driver,
        'mileage_total': mileage_total,
        'newest_miles': newest_miles
    }
    return render(request, 'mileage/index.html', context)

class MileageCreateView(CreateView):
    model = Mileage
    fields = ['miles']
    template_name = 'mileage/mileage_form.html'
    success_url = reverse_lazy('index')
    #How to make sure User that posts his miles always posts with his own user name 
    def form_valid(self, form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)

#view showing djangos get object function

from django.shortcuts import get_object_or_404

def my_view(request):
    first = get_object_or_404(Mileage, pk=1)
    context = {
        'first': first

    }
    return render(request, 'mileage/my_view.html', context)

def other(request):
    try:

        second = Mileage.objects.all()
    except Mileage.DoesNotExist:
        raise Http404("No Mileage matches the given query")
    context = {
        'second': second
    }
    return render(request, 'mileage/other.html', context)