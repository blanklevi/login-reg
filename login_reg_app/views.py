from django.shortcuts import render, redirect
from .models import User, UserManager, Message, Comment
import bcrypt
from django.contrib import messages
from time import strftime, gmtime


def index(request):
    all_users = User.objects.all()
    print(all_users)
    return render(request, "index.html")


def registration(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        if request.method == "POST":
            fn = request.POST['first_name']
            ln = request.POST['last_name']
            email = request.POST['email']
            pw = request.POST['password']
            confirm_pw = request.POST['confirm_pw']
            pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
            # confirm password stuff here
            if bcrypt.checkpw(confirm_pw.encode(), pw_hash.encode()) == True:
                User.objects.create(first_name=fn, last_name=ln,
                                    email=email, password=pw_hash)
                request.session['email'] = email
                request.session['password'] = pw_hash
                request.session['first_name'] = fn
                request.session['last_name'] = ln
            else:
                errors['pwconfirm'] = "Lol pw didnt match, noob"
                if len(errors) > 0:
                    for key, value in errors.items():
                        messages.error(request, value)
                    return redirect('/')
    return redirect("/wall")


def log_in(request):
    if request.method == "POST":
        log_email = request.POST['log_email']
        login_pw = request.POST['login_pw']
        if User.objects.filter(email=log_email):
            request.session['log_email'] = log_email
            request.session['login_pw'] = login_pw
            return redirect('/wall')


def success_log_in(request):
    if 'message' not in request.session:
        request.session['message'] = []
    logged_user = User.objects.filter(email=request.session['log_email'])
    logged_user_fn = logged_user[0].first_name
    logged_user_ln = logged_user[0].last_name
    user_id = logged_user[0].id
    messages = Message.objects.all()
    comments = Comment.objects.all()
    request.session['id'] = user_id
    context = {
        "first_name": logged_user_fn,
        "last_name": logged_user_ln,
        "session_messages": request.session['message'],
        "time": strftime("%m-%d-%y"),
        "user_id": user_id,
        "messages": messages,
        "comments": comments,
        "session_id": request.session['id']
    }
    return render(request, "wall.html", context)


def success(request):
    logged_user = User.objects.filter(email=request.session['email'])
    logged_user_fn = logged_user[0].first_name
    print(logged_user_fn)
    context = {
        "first_name": logged_user_fn,
    }
    return render(request, "loggedin.html", context)


def log_out(request):
    request.session['log_email'] = []
    request.session['email'] = []
    return redirect('/')


def wall_page(request):
    user_id = request.POST['user_id']
    user = User.objects.get(id=user_id)
    current_user = User.objects.get(id=user_id)
    posted_message = request.POST['message']
    new_message = Message.objects.create(user=user, message=posted_message)
    return redirect('/wall')


def comment(request):
    userid = request.POST['userid']
    user = User.objects.get(id=userid)
    message_id = request.POST['message_id']
    message = Message.objects.get(id=message_id)
    posted_comment = request.POST['comment']
    new_comment = Comment.objects.create(
        user=user, message=message, comment=posted_comment)
    return redirect('/wall')
