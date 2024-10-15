from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Post, Profile
from .forms import PostForm

# Index View
def home(request):
    # Paginate post list
    paginator = Paginator(Post.objects.all(), 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    # Post form
    if request.user.is_authenticated:
        if request.method == "POST":            
            post_form = PostForm(data=request.POST)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('home')
                
        post_form = PostForm()
        return render(request, 'social/index.html', {"posts":posts,"post_form":post_form,})
        
    else:
        post_form = PostForm()
        return render(request, 'social/index.html', {"posts":posts,"post_form":post_form,})



# Edit Post Veiw    
def edit_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)        
        if request.user.username == post.user.username:

            post_form = PostForm(request.POST or None, instance=post) 

            if request.method == "POST":
                if post_form.is_valid():
                    post = post_form.save(commit=False)
                    post.user = request.user
                    post.save()

                    return redirect('home')
            else:
                return render(request, "social/edit_post.html", {'post_form':post_form, 'post':post})


# Delete Post Veiw    
def delete_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        if request.user.username == post.user.username:
            
            post.delete()
            return redirect(request.META.get("HTTP_REFERER"))

        else:
            
            return redirect('home')
                      


# Profile List View
def profile_list(request):
    if request.user.is_authenticated:

        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'social/profile_list.html', {"profiles":profiles})

    else:
        # ONCE CREATAED, REDIRECT USER TO LOGIN PAGE
        return redirect('home')


# Profile Page View
def profile_page(request, pk):
    if request.user.is_authenticated:

        profile_posts = Post.objects.filter(user_id=pk).order_by("-created_on")
        profile_page = Profile.objects.get(user_id=pk)

        # Follow/ Unfollow form request
        if request.method == "POST":
            user_profile = request.user.profile
            action = request.POST["follow"]
            if action == "unfollow":
                user_profile.follows.remove(profile_page)
            else:
                user_profile.follows.add(profile_page)
            user_profile.save()


        return render(request, 'social/profile_page.html', {
            "profile_page":profile_page,
            "profile_posts":profile_posts,
        })

    else:
        # ONCE CREATAED, REDIRECT USER TO LOGIN PAGE
        return redirect('home')
