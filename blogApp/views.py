from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import Post
from .forms import *
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request,'index.html')


def post_list(request,tag_slug=None):
    posts_list=Post.published.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        posts_list=posts_list.filter(tags__in=[tag])
    paginator=Paginator(posts_list,10)
    page_number=request.GET.get('page',1)
    try:
        posts=paginator.page(page_number)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts=paginator.page(1)

    print(posts)
    return render(request,'allBlogs.html',{"posts":posts,'tag':tag})




def post_details(request,year,month,day,post):
    print("hi")
    try:
       
        # post=get_object_or_404(Post,id=id,status=Post.Status.PUBLISHED)
        post=get_object_or_404(Post,status=Post.Status.PUBLISHED,slug=post,publish__year=year,publish__month=month,publish__day=day)
        comments=post.comments.filter(active=True)
        form=CommentForm()
        print(post)

        post_tags_id=post.tags.values_list('id',flat=True)
        similar_posts=Post.published.filter(tags__in=post_tags_id).exclude(id=post.id)
        similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

        return render(request,'postDetail.html',{'post':post,'comments':comments,'form':form,'similar_posts':similar_posts})
    except:
        print("An exception occurred")
        return render(request,'postDetail.html')
    return render(request,'postDetail.html')

@require_POST
def post_comment(request,post_id):
    post=get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    comment = None
    form= CommentForm(data=request.POST)
    if form.is_valid():
        comment=form.save(commit=False)
        comment.post=post
        comment.save()
        return render(request,'comment.html',{'post':post,'comment':comment})


def post_share(request,post_id):
    post=get_object_or_404(Post,id=post_id, status=Post.Status.PUBLISHED)
    sent=False
    # return render(request,'share.html')
    if request.method == 'POST':
        form=EmailPostForm(request.POST)
        print(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject=f"{request.user} recommends  you read " f"{post.title}"
            message=f"Read {post.title} at {post_url} \n\n"f"{request.user}\'s comments : {cd['comments']}"
            send_mail(subject,message,'shubhamvr33@gmail.com',[cd['to']])
            sent=True
            print(subject)
            return render(request,'share.html',{'post':post,'form':form,'sent':sent})

    else:
        form=EmailPostForm()
        return render(request,'share.html',{'post':post,'form':form,'sent':sent})


def search(request):
#    return render(request,'allBlogs.html')
    if request.method == 'POST': # this will be GET now      
        searchtext =  request.POST.get('search') # do some research what it does       
        print(searchtext)
        try:
            status = Post.objects.filter(title__icontains=searchtext) # filter returns a list so you might consider skip except part
            print(status)
        except Post.DoesNotExist:
            status = None
           
        return render(request,"allBlogs.html",{"posts":status})
    else:
        return render(request,"allBlogs.html",{})
    

class RegistrationView(View):
    def get(self,request):
        if not request.user.is_authenticated:
            form =RegistrationForm()
            # print(form)
            return render(request, 'account/register.html', {'form': form})
        else:
              return HttpResponseRedirect('/accounts/profile/') 
    def post(self,request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(
                request, "Congratulations! Registration Successful!")
            form.save()
        else:
            messages.warning(request,'some error occure')
        
        return render(request, 'account/register.html', {'form': form})
    
# class UserLoginView(View):
    # def get(self,request):
    #     fm= LoginForm()
    #     return render(request,'account/login.html',{'form':fm})
    
    # def post(self,request):
        
    #     fm =LoginForm(request.POST)
    #     print(fm)
    #     if fm.is_valid():
    #         uname=fm.cleaned_data(['username'])
    #         upass=fm.cleaned_data(['password'])
    #         user=authenticate(username=uname,password=upass)
    #         print(user)
    #         if user is not None:
    #             login(request,user)
    #             return HttpResponseRedirect('/profile/')

def UserLogin(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            fm=LoginForm(request=request,data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data["username"]
                upass=fm.cleaned_data["password"]
                user=authenticate(username=uname,password=upass)
                print(user)
                if user is not None:
                    login(request,user)
                    messages.success(request,"Congratulation! login succesfully ")
                    return HttpResponseRedirect('/accounts/profile/')
            else:
                messages.error(request,"Invallid Credientials")
                return HttpResponseRedirect('/accounts/login/')
        else:
            fm=LoginForm()
            return render(request,'account/login.html',{'form':fm})
    else:
        return HttpResponseRedirect('/accounts/profile/')
    


def UserLogout(request):
    logout(request) 
    return HttpResponseRedirect('/accounts/login') 


class UserProfileView(View):
    def get(self,request):
        if request.user.is_authenticated:
            publishPost= Post.objects.filter(Q(author=request.user.id) & Q(status='PB'))
            draftPost= Post.objects.filter(Q(author=request.user.id) & Q(status='DF'))
            print(publishPost)
            context={
                "username":request.user,
                "publishPost":publishPost
            }
            return render(request,'account/profile.html',{'publishPost':publishPost,'draftPost':draftPost,'username':request.user})
        else:
            return HttpResponseRedirect('/accounts/login/')
        

# create blog

# class AddBlogView(View):
#     def get(self,request):
#         fm=AddBlogForm()
#         return render(request,'addBlog.html',{'form':fm})
    
#     def post(self,request):
#         fm=AddBlogForm(request.POST)
#         # print(fm)
#         post =None
#         title=request.POST.get('title')        
#         tags=request.POST.get('tags')
#         body=request.POST.get('body')
#         image = request.FILES['image']
#         print(image)
#         print(request.POST)
#         author=request.user.id
#         # print(fm)
#         try:
#             if fm.is_valid():
#                 content=fm.cleaned_data(["body"])
#                 print(content)
#                 obj=fm.save(commit=False)
#                 obj.author=request.user
#                 obj.save()
#                 let=fm.save_m2m()
#                 print(let)
#         except Exception as e:
#             print(e)
#         print(title,tags,body,author)
#         return render(request,'addBlog.html',{"form":fm})


def addBlog(request):
    context={'form':AddBlogForm}
    try:
        if request.method=='POST':
            form=AddBlogForm(request.POST)
            image=request.FILES['image']
            title=request.POST.get('title')
            body=request.POST.get('body')
            # clean_body=form.cleaned_data['body']
            print(title,body,image)
            
            try:
                if form.is_valid():
                    # content=form.cleaned_data['body']
                    body=form.cleaned_data['body']
                    obj=form.save(commit=False)
                    obj.author=request.user
                    obj.image=image
                    obj.save()
                    form.save_m2m()
                    
                    print("created")
                else:
                    print(form.errors)
            except Exception as e:
               
                print(e)
            return HttpResponseRedirect('/blog/addblog/')
        else:
            return render(request,'addBlog.html',context)
    except Exception as e:
        print(e) 
        print("some eeror accour")   
    return render(request,'addBlog.html',context)