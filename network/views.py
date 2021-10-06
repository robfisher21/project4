from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.utils import ConnectionRouter
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.http import JsonResponse
import json
from django.core.paginator import EmptyPage, Paginator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone, formats



from .models import User, Posts, Profile


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# New Post Form: describes a new post form:
class PostForm (forms.Form):
    Post = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':70, 'autofocus' : 'True','id':'form-post'}), label=False )


def following (request):
    request_user = User.objects.get(username = request.user)
    UsersFollowers= Profile.objects.get(user=request_user).following.all()
    FollowersPosts = Posts.objects.filter(user__in = UsersFollowers).order_by('datetime').reverse()

    posts = getpagination (request, FollowersPosts)[0]
    pagination = getpagination (request, FollowersPosts)[1]
   # allposts = Posts.objects.filter().order_by('datetime').reverse()
    #Posts.objects.all().values('id', 'user_id__username', 'post', 'datetime').order_by('datetime').reverse()
    # WORKING data= User.objects.get(username = request.user).followerlist.all()
    # WORKING data= User.objects.get(username = request.user).user.all()
    # WORKING data= User.objects.get(username = request.user).user.values('post')

    return render(request, "network/following.html", {
        "posts" : posts,
        "pagination" : pagination,
   })

  

def all_posts(request):
 #   posts = nopagination(request)
    allposts = Posts.objects.filter().order_by('datetime').reverse()

    posts = getpagination (request, allposts)[0]
    pagination = getpagination (request, allposts)[1]

    return render(request, "network/index.html", {
        "PostForm" : PostForm,
        "posts" : posts,
        "pagination" : pagination,
    })


def update_post (request, post_id):
    Post = Posts.objects.get(id = post_id)
    data = json.loads(request.body)


    if  data.get("postbody") is not None:
        Post.post = data["postbody"]
        Post.datetime = timezone.now() 
        Post.save()
        Post = Posts.objects.get(id = post_id)
        postbody = Post.post
        datetime = formats.date_format(Post.datetime, 'N j, Y, P')

        return JsonResponse({"postbody": postbody, "datetime": datetime}, status=201) 
    
    else:
        return JsonResponse({"message": "No updates made"}, status=201) 


def create_post (request):
    allposts = Posts.objects.filter().order_by('datetime').reverse()

    posts = getpagination (request, allposts)[0]
    pagination = getpagination (request, allposts)[1]

    if request.method =="POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.cleaned_data['Post']
            p = Posts(user=request.user, post=post)
            p.save()

            return HttpResponseRedirect(reverse("allposts")) 

        else:
            return render(request, "network/index.html", {
            "PostForm" : form,
            "posts" : posts,
            "pagination" : pagination
            })

def GetFollowStatus (request, UserToFollow):
    try:
        # Check user is authenticated:
        UserFollowing = User.objects.get(username = request.user)
        

        if UserToFollow.id != UserFollowing.id:
            EligibleToFollow = True

        else:
            EligibleToFollow = False

        # Check Following status:
        try:
            Profile.objects.get(user=UserToFollow.id).followers.get(id=UserFollowing.id)
            followstatus= "true"
            followaction = "Unfollow"
        except:
            followstatus= "false"
            followaction = "Follow"

    except:
            followstatus = "User Not Signed-in"
            followaction = "User Not Signed-in"
            EligibleToFollow = False
            UserFollowing = "User Not Signed-in"
            

    return  followstatus, followaction, EligibleToFollow, UserFollowing

@csrf_exempt
def updatefollowers (request, profile):
        UserToFollow = User.objects.get(username=profile)
        UserFollowing = GetFollowStatus (request, UserToFollow)[3]
        followstatus = GetFollowStatus (request, UserToFollow)[0]
    
    # Change Follow Status

        if followstatus == "true": 
            # Remove UserFollowing as a Followers
            Profile.objects.get(user=UserToFollow).followers.remove(UserFollowing)
            # Remove UserToFollow from Following list
            Profile.objects.get(user=UserFollowing).following.remove(UserToFollow)

            followaction = "Follow"
            followstatus= "false"
        else:
            # Add UserFollowing as a Followers
            Profile.objects.get(user=UserToFollow).followers.add(UserFollowing)
            # Add UserToFollow from Following list
            Profile.objects.get(user=UserFollowing).following.add(UserToFollow)

            followaction = "Unfollow"
            followstatus= "true"
            
        FollowerCount = Profile.objects.get(user=UserToFollow.id).followers.all().count()
        
        return JsonResponse({"followaction": followaction, "followstatus": followstatus, "followers": FollowerCount}, status=201, safe=False) 


def profile (request, profile):
    UserToFollow = User.objects.get(username=profile)
    UserToFollowPosts = Posts.objects.filter(user=UserToFollow.id).order_by('datetime').reverse()
    UserToFollowPostsCount = UserToFollowPosts.all().count()
    followaction = GetFollowStatus (request, UserToFollow)[1]
    followstatus = GetFollowStatus (request, UserToFollow)[0]
    EligibleToFollow = GetFollowStatus (request, UserToFollow)[2]
    FollowerCount = Profile.objects.get(user=UserToFollow.id).followers.all().count()
    
    posts = getpagination (request, UserToFollowPosts)[0]
    pagination = getpagination (request, UserToFollowPosts)[1]

    return render(request, "network/profile.html", {
        "profile" : UserToFollow,
        "posts" : posts,
        "pagination" : pagination,
        "followaction" : followaction,
        "followercount" : FollowerCount,
        "followstatus" : followstatus,
        "postcount" : UserToFollowPostsCount,
        "EligibleToFollow" : EligibleToFollow,
        "PostForm" : PostForm
  

    })

@csrf_exempt
def like (request, post_id):
    try:
        user = User.objects.get(username=request.user)
        
        if request.method == "POST":
            data = json.loads(request.body)
            likestatus = data.get("likestatus", "")
            

            if likestatus == "True":
                Posts.objects.get(id=post_id).likes.remove(user)
            
            else:
                Posts.objects.get(id=post_id).likes.add(user)
            
            userlikes = Posts.objects.filter(id=post_id).filter(likes=user)
        
            if user is not None and userlikes:
                    newlikestatus = "True"
            else: newlikestatus = "False"

            likecount = Posts.objects.get(id=post_id).likes.all().count()

            p=Posts.objects.get(id=post_id)
            p.likecount=likecount
            p.save()
        else:
            userlikes = Posts.objects.filter(id=post_id).filter(likes=user)
        
            if user is not None and userlikes:
                    newlikestatus = "True"
            else: newlikestatus = "False"

            likecount = Posts.objects.get(id=post_id).likes.all().count()

            p=Posts.objects.get(id=post_id)
            p.likecount=likecount
            p.save()

        return JsonResponse({"message": newlikestatus, "likecount": likecount, "post": post_id}, status=201, safe=False) 
    
    except:
        return JsonResponse({"message": "Sign-in to like", "likecount": "Sign-in to like", "post": post_id}, status=201, safe=False) 


def getpagination (request, data):
    resultsperpage = 5
    pagination = []
  
    for i in Paginator(data,resultsperpage).page_range:
        pagination.append(i)

        try: 
            page_number = request.GET.get('page')
            posts = Paginator(data, resultsperpage).page(page_number)

        except: 
            posts = Paginator(data, resultsperpage).page(1)

    return [posts, pagination]



#
#
#
# Old code
#
#
#
#












def post_sort_order (request, *args):
    pagination = []
    user_id = None

    #If user profile present in argument:
    for arg in args:
            user_id = arg
    
    if user_id:
        try:
            user_posts = Posts.objects.filter(user=user_id).order_by('datetime').reverse()

            for i in Paginator(user_posts,5).page_range:
                pagination.append(i)

                try: 
                    page_number = request.GET.get('page')
                    posts = Paginator(user_posts, 5).page(page_number)

                except: 
                    posts = Paginator(user_posts, 5).page(1)

        except:
            posts = None  
         
    else:
        try:
            allposts = Posts.objects.filter().order_by('datetime').reverse()
          #  allposts = nopagination(request)

            for i in Paginator(allposts,5).page_range:
                pagination.append(i)

            try: 
                page_number = request.GET.get('page')
                posts = Paginator(allposts, 5).page(page_number)

            except: 
                posts = Paginator(allposts, 5).page(1)

        except:
            posts = None

    return [posts, pagination] 




    #def nopagination (request):
#    posts = Posts.objects.all().values('id', 'user_id__username', 'post', 'datetime').order_by('datetime').reverse()
#    postswithlikes = []
 #   try: 
 #       user_id = User.objects.get(username=request.user)
 #   except:
 #       user_id = None

 #   for i in range (len(posts)):
  #      post_id = posts[i]['id']
      #  likecount = Posts.objects.get(id=post_id).likes.all().count()
   #     userlikes = Posts.objects.filter(id=post_id).filter(likes=user_id)
   #     if user_id is not None and userlikes:
  #          likestatus = True
    #    else: likestatus = False

  #      postswithlikes.append ({
  #          "id" : posts[i]['id'],
   #         "user" : posts[i]['user_id__username'],
   #         "post" : posts[i]['post'],
   #         "datetime" : posts[i]['datetime'],
   #         "likecount" : "",
   #         "likestatus" : ""  
   #     })
   # return postswithlikes

#2.9
# 1.7 - no count
# 0.3 - no count, no like status  