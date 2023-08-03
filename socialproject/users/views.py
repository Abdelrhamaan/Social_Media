from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import UserEditForm, ProfieEditForm
from posts.models import Post
from posts.forms import CommentAddForm


@login_required
def index(request):
    if request.method == 'POST':
        comment_form = CommentAddForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            new_comment.post = post
            new_comment.user = request.user  # set the logged-in user as the comment's user
            new_comment.save()
            comment_form = CommentAddForm()  # reset the comment form after add new comment
            '''
             to prvent when logged in and refresh page not dublicate all comments for logged in user
             due to  browser caching
            '''
            return redirect('home')
    else:
        comment_form = CommentAddForm()
    curr_user = request.user
    get_all_posts = Post.objects.all()
    get_profile = Profile.objects.filter(user=curr_user).first()
    return render(request, 'users/index.html', {'get_all_posts': get_all_posts,
                                                'get_profile': get_profile,
                                                'curr_user': curr_user,
                                                'comment_form': comment_form})


@login_required
def profile(request):
    if request.method == 'POST':
        comment_form = CommentAddForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            new_comment.post = post
            new_comment.user = request.user  # set the logged-in user as the comment's user
            new_comment.save()
            comment_form = CommentAddForm()  # reset the comment form after add new comment
            '''
             to prvent when logged in and refresh page not dublicate all comments for logged in user
             due to  browser caching
            '''
            return redirect('home')
    else:
        comment_form = CommentAddForm()
    curr_user = request.user
    get_user_posts = Post.objects.filter(user=curr_user)
    get_profile = Profile.objects.filter(user=curr_user).first()
    # user_profile_photo = Profile.objects.filter(user=curr_user).first()
    return render(request, 'users/Profile.html', {'get_all_posts': get_user_posts,
                                                  'get_profile': get_profile,
                                                  'curr_user': curr_user,
                                                  'comment_form': comment_form
                                                  })


def user_login(request):
    ''' to check if user logged in return him to home page
        redirect take the name of url not the url '''
    if request.user.is_authenticated:
        return redirect('home')
    if (request.method == "POST"):
        form = LoginForm(request.POST)
        if form.is_valid():
            # to store form data form.cleaned_data
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return index(request)
            else:
                return HttpResponse("Invalid credentials")
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # commit saving data to database
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, "users/register_done.html")
    else:
        user_form = UserRegistrationForm()
    return render(request, "users/register.html", {'user_form': user_form})


@login_required
def edit_user_profile(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        # files=request.FILES to accept files from request (images)
        profile_form = ProfieEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
        else:
            print("User form errors:", user_form.errors)
            print("Profile form errors:", profile_form.errors)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfieEditForm(instance=request.user.profile)
    return render(request, "users/edit.html", {"user_form": user_form, "profile_form": profile_form})
