from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import PostAddForm, CommentAddForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Post


@login_required
def add_post(request):
    if request.method == "POST":
        add_form = PostAddForm(data=request.POST, files=request.FILES)
        if add_form.is_valid():
            new_post = add_form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            # print(new_post)
    else:
        add_form = PostAddForm()
    return render(request, "posts/add_post.html", {"add_form": add_form})


@login_required
def delete_post(request, id):
    context = {}
    post = get_object_or_404(Post, id=id)

    if request.method == "POST":
        if post.user == request.user:
            post.delete()
            return redirect('home')
        else:
            return HttpResponse("You are not authorized to perform this action.")
    return render(request, "posts/delete_post.html", context)


@login_required
def liked_posts(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    if post.liked_by.filter(id=request.user.id).exists():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)
    return redirect('home')


# @login_required
# def add_comment(request):
#     comment_form = CommentAddForm()
#     if request.method == 'POST':
#         comment_form = CommentAddForm(data=request.POST)
#         new_comment = comment_form.save(commit=False)
#         post_id = request.POST.get('post_id')
#         post = get_object_or_404(Post, id=post_id)
#         new_comment.post = post
#         new_comment.save()
#         comment_form = CommentAddForm()  # reset the comment form after add new comment
#     else:
#         comment_form = CommentAddForm()
#     return render(request, 'users/index.html', {'comment_form': comment_form})
