from django.shortcuts import render, redirect, get_object_or_404
from app.models import * 
from app.forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.db.models import Count
from django.core.paginator import Paginator


# Create your views here.

def index(request):
    subscribe_form = SubsribeForm()
    subscribed = ''
    if request.method == 'POST':
        subscribe_form = SubsribeForm(request.POST)
        if subscribe_form.is_valid:
            subscribe_form.save()
            request.session['subscribed'] == True
            subscribe_form = SubsribeForm()
            messages.success(request, 'YOu have successiful subscribed to our channel...')
            return redirect('index')

    website_info = None
    if MetaWebsite.objects.all().exists():
        website_info = MetaWebsite.objects.all()[0]

    featured_blog = Post.objects.filter(is_featured=True)
    if featured_blog:
        featured_blog = featured_blog[0]

    post = Post.objects.all()
    top_post = Post.objects.all().order_by('-view_count')[0:3]
    recent_post = Post.objects.all().order_by('-last_updated')[0:3]
    context = {
        'posts':post,
        'recent_post':recent_post,
        'top_post':top_post,
        'form':subscribe_form,
        'featured_blog':featured_blog,
        'website_info':website_info
    }
    return render(request, 'app/index.html', context=context)

def post_page(request, slug):
    post = Post.objects.get(slug=slug)

    #######getting the author of the post ######
    author_profile = Profile.objects.get(user=post.author)


    form = CommentForm()
    comments = Comment.objects.filter(post=post, parent=None)

    if request.method == "POST":
        form_comment = CommentForm(request.POST)
        if form_comment.is_valid:
            if request.POST.get('parent'):
                reply_comment = form_comment.save(commit=False)
                post_id = request.POST['post_id']
                post = Post.objects.get(id=post_id)
                comment_id = request.POST.get('parent')
                comment = Comment.objects.get(id=comment_id)
                reply_comment.post = post
                reply_comment.parent = comment
                reply_comment.name = request.user.username
                reply_comment.save()
                print('reply was saved')
                return redirect('post_page', slug)
            else:
                comment = form_comment.save(commit=False)
                postId = request.POST['post_id']
                post = Post.objects.get(id=postId)
                comment.post = post
                comment.name = request.user.username
                comment.save()
                print('Comment was saved')
                return redirect('post_page', slug)

        ########### THIS IS BOOKMARK LOGIC ###########
    bookmarked = False
    if post.bookmarks.filter(id=request.user.id).exists():
        bookmarked = True

        ########### THIS IS LIKE LOGIC ###########
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True

        ########### THIS IS LIKE LOGIC ###########
    number_of_likes = post.like_number()



    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count += 1
    post.save()

        ########### THE LOGIC FOR SIDE BAR ############
    recent_post = Post.objects.exclude(id = post.id).order_by('-last_updated')[0:3]
    top_authors = User.objects.annotate(number = Count('post')).order_by('-number')
    related_post = Post.objects.exclude(id = post.id).filter(author = post.author)[0:3]
    tags = Tag.objects.all()


    context = {
        'post':post,
        'form':form,
        'comments':comments,
        'bookmarked':bookmarked,
        'liked':liked,
        'number_of_likes':number_of_likes,
        'author_profile':author_profile,
        'recent_post':recent_post,
        'top_authors':top_authors,
        'related_post':related_post,
        'tags':tags

    }
    return  render(request, 'app/post.html', context=context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
          ##########      REMAIMDER TO LOOK FOR      #############
    top_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-last_updated')[0:3]
          ##########      REMAIMDER TO LOOK FOR      #############
    tags = Tag.objects.all()
    context = {
        'tag':tag,
        'top_post':top_posts,
        'recent_posts':recent_posts,
        'tags':tags
    }
    return render(request, 'app/tag.html', context=context)

def author_page(request, slug):
    profile = Profile.objects.get(slug=slug)
    
    top_posts = Post.objects.filter(author=profile.user).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(author=profile.user).order_by('-last_updated')[0:3]
    top_authors = User.objects.annotate(number=Count('post')).order_by('-number')

    context = {
        'profile':profile,
        'recent_posts':recent_posts,
        'top_posts':top_posts,
        'top_authors':top_authors
    }
    return render(request, 'app/author.html', context=context)


def search_page(request):
    posts = Post.objects.all()
    iterms = ''
    if request.method == 'GET':  
        if request.GET.get('search'):   
            iterms = request.GET.get('search')
            posts = Post.objects.filter(title__icontains = iterms)
    
    context = {
        'posts':posts,
        'iterms':iterms
    }
    return render(request, 'app/search.html', context=context)

def about_page(request):
    website_info = None
    if MetaWebsite.objects.all().exists():
        website_info = MetaWebsite.objects.all()[0]   
    context = {
        'about':website_info 
    }
    return render(request, 'app/about.html', context=context)


def register_page(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    context = {
        'form':form
    }
    return render(request, 'registration/registration.html', context=context)


def logout_page(request):
    logout(request)
    return render(request, 'app/logged_out.html')

def bookmarks_page(request, slug):
    id = request.POST.get('post_id')
    print('This is id am looking for....', id)
    post = get_object_or_404(Post, id=id)
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)

    return redirect('post_page', slug)


def like_page(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('like_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('post_page', slug)


def all_bookmark_page(request):
    bookmarked = Post.objects.filter(bookmarks=request.user)
    context = {
        'bookmarked':bookmarked
    }
    return render(request, 'app/all_bookmark_page.html', context=context)

def all_posts(request):
    all_posts = Post.objects.all()
    pagination = Paginator(all_posts, 2)
    page = request.GET.get('page')
    try:
        posts = pagination.get_page(page)
    except:
        posts = pagination.get_page(1)

    context = {
        'posts':posts
    }
    return render(request, 'app/all_posts.html', context=context)

def my_likes_page(request):
    likes = Post.objects.filter(likes=request.user)
    context = {
        'likes':likes
    }
    return render(request, 'app/my_likes.html', context=context)


def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.author:
        post.delete()
    return redirect('index')


def new_post(request):
    form = Create_Post()
    if request.method == 'POST':
        form = Create_Post(request.POST, request.FILES) 
        if form.is_valid():
            post = form.save(commit=False) 
            post.save()   
            request.user.post.add(post)
            
            return redirect('index')  
    context = {
        'form': form
    }
    return render(request, 'app/new_post.html', context=context)


from django.shortcuts import get_object_or_404

def edit_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    form = editProfile(instance=profile)

    if request.method == 'POST':
        form = editProfile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile.save()
            return redirect('index')

    context = {
        'form': form
    }
    return render(request, 'app/edit_profile.html', context=context)


def create_profile(request):
    form = editProfile()

    if request.method == 'POST':
        current_user = request.user
        form = editProfile(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
            return redirect('index')

    context = {
        'form': form
    }
    return render(request, 'app/create_profile.html', context=context)

