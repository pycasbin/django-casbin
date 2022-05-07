from django.shortcuts import render
from django.shortcuts import redirect
from . import models, forms
import hashlib


def hash_code(s, salt='sad122sad'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def login(request):
    if request.session.get("is_login", None):
        return redirect('/index/')
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "please check your input!"
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(name=username)
            except:
                message = "user not exist!"
                return render(request, 'login.html', locals())
            print(user.password, "password:", password)
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = "password is wrong!"
                return render(request, 'login.html', locals())

            return redirect('/index/')
        else:
            return render(request, 'login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login.html', locals())


def index(request):
    username = request.session.get('user_name', None)
    return render(request, 'index.html', locals())


def register(request):
    if request.session.get("is_login", None):
        return redirect('/index/')
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "please check your input!"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')

            if password1 != password2:
                message = 'password is not same!'
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = 'user already exist!'
                    return render(request, 'register.html', locals())
                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.save()
                return redirect('/login/')
        else:
            return render(request, 'register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    request.session.flush()
    return redirect('/login/')
