import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import LoginForm, RegisterForm
from recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGE = os.environ.get('PER_PAGE')


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', context={
        'form': form,
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'User registered with sucess!, Please Log In.') # noqa E501
        del (request.session['register_form_data'])
        return redirect('authors:login_view')

    return redirect('authors:register_view')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login_view.html', context={
        'form': form,
        'form_action': reverse('authors:login_create'),
    })


def login_create(request):
    if not request.POST:
        raise Http404
    form = LoginForm(request.POST)
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password'),
        )
        if authenticated_user is not None:
            messages.success(request, 'You are Logged In')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Invalid username or password')

    return redirect('authors:dashboard')


@login_required(login_url='authors:login_view', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout')
        return redirect(reverse('authors:login_view'))  

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect(reverse('authors:login_view'))  

    messages.success(request, 'Logged out successfully')
    logout(request)
    return redirect(reverse('authors:login_view'))


@login_required(login_url='authors:login_view', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False, author=request.user
    ).order_by('-id')
    paje_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGE,
        )

    return render(request, 'authors/pages/dashboard.html', context={
        'recipes': paje_obj,
        'pagination_range': pagination_range,
    })
