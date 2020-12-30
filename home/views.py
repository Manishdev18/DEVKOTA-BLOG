from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,HttpResponseRedirect
from datetime import datetime
from home.models import contact,Post, BlogComment
from django.urls import reverse
from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home.froms import UserRegisterForm, UserUpdateForm,ProfileUpdateForm ,NewCommentForm
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.
def register(request):
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f'Account created has been created {username}')
            return redirect('/login')
    else:
        form = UserRegisterForm()
    return render(request,'register.html',{'form':form})
    


# Create your views here.






def index(request):
    context={
        'posts': Post.objects.all()
        
        
    }
    return render(request,"index.html",context)

@login_required
def bloglike(request,pk):
    post = get_object_or_404(Post, id=request.POST.get('blogpost_id'))
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
    else:
        post.like.add(request.user)

    return HttpResponseRedirect(reverse("post_detail", args=[str(pk)]))
   ## return HttpResponseRedirect(reverse("home"))

  



class PostListView(ListView):
    model = Post
    
    #model.number_of_likes
    # template_name = MainApp/BlogPost_detail.html
    # context_object_name = 'object'

   
    template_name = "index.html"
    
    context_object_name= "posts"
    ordering = ['-like']
    paginate_by =3

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['lposts'] = Post.objects.order_by('-date_posted')[:5]
        return context
    
class UserListView(ListView):
    model = Post
    template_name = "user_post.html"
    context_object_name= "posts"
    paginate_by = 3
   

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class SearchListView(ListView):
    
    model = Post
    template_name = "search.html"
    context_object_name = 'object_list'
   
    paginate_by = 2
    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return Post.objects.filter(title__contains=query)
        return Post.objects.all()
        #print(name)
        #object_list=[]
        #if name:
         ##   object_list = model.objects.filter(title__contains=name)
        #if not name:
         ##   print('chutiya')
        
        #return object_list
   

    
     


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args,**kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if likes_connected.like.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        comments_connected = BlogComment.objects.filter(
            blogpost_connected=self.get_object()).order_by('-date_posted')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = NewCommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = BlogComment(content=request.POST.get('content'),
                                  author=self.request.user,
                                  blogpost_connected=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)

    
    

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title', 'discription','postimage','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        else:
            return False
    

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title', 'discription','postimage','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    
    
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post 
    success_url='/'
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        else:
            return False

def about(request):
    return render(request,"about.html")

def travel(request):
    if request.method=="POST":  
        print("this is Post")
        name=request.POST["name"]
        email=request.POST["email"]
        phone=request.POST["phone"]
        print(name,email,phone)
        ins=contact(name=name,email=email,phone=phone,date=datetime.today())
        ins.save()
        print("we done it")
    return render(request,"travel.html")
def food(request):
    return render(request,"food.html")
 #user = user.object.get(username=username)
class LikeRedirect(RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        id_= self.kwargs.get("pk")
        print(id_)
        obj = get_object_or_404(Post, id=self.kwargs['pk'])
        url_= obj.get_absolute_url()
        user=self.request.user
        if user.is_authenticated:
            if user in obj.like.all():
                obj.like.remove(user)
            else:
                obj.like.add(user)
        return url_

@login_required
def profile(request):
    if request.method=="POST":  
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                       request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account Update!')
            return redirect('/profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
      
        


    context={
        'u_form':u_form,
        'p_form': p_form
    }
    return render(request,"profile.html",context)

