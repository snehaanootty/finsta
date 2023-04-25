from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views.generic import CreateView,View,TemplateView,UpdateView,ListView,DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout


from myapp.forms import SignUpForm,SignInForm,ProfileEditForm,PostForm,CoverPicChangeForm,ProfilePicChangeForm
from myapp.models import UserProfile,Posts,Comments

class SignUpView(CreateView):
    model=User
    template_name="register.html"
    form_class=SignUpForm
    success_url=reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request,"account created succcessfullyy")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"account creation failed")
        return super().form_invalid(form)
    
class SignInView(View):
    model=User
    template_name="login.html"
    form_class=SignInForm

    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{"form":form})
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login succeessfull")
                return redirect("index")
        messages.error(request,"login failed")
        return render(request,self.template_name,{"form":form})
    

class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    model=Posts
    context_object_name="posts"
    success_url=reverse_lazy("index")
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
def add_like_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    post_obj=Posts.objects.get(id=id)
    post_obj.liked_by.add(request.user)
    return redirect("index")

def add_comment_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    post_obj=Posts.objects.get(id=id)
    comment=request.POST.get("comment")
    user=request.user
    Comments.objects.create(user=request.user,post=post_obj,comment_text=comment)
    return redirect("index")

def comment_remove_View(request,*args,**kwargs):
    id=kwargs.get("pk")
    comment_obj=Comments.objects.get(id=id)
    if request.user==comment_obj.user:
        comment_obj.delete()
        return redirect("index")
    else:
        messages.error(request,"you are unable to do this!! please contact admin")
        return redirect("signin")

class Profile_detail_View(DetailView):
    model=UserProfile
    template_name="profile.html"
    context_object_name="profile"
    
            
class ProfileEditView(UpdateView):
    model=UserProfile
    form_class=ProfileEditForm
    template_name="profileedit.html"
    success_url=reverse_lazy("index")




def Update_Coverpic_View(request,*args,**kwargs):
    id=kwargs.get("pk")
    pro_obj=UserProfile.objects.get(id=id)
    form=CoverPicChangeForm(instance=pro_obj,data=request.POST,files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("profiledetail",pk=id)
    return redirect("profiledetail",pk=id)



def Update_profilepic_view(request,*args,**kwargs):
    id=kwargs.get("pk")
    pro_obj=UserProfile.objects.get(id=id)
    form=ProfilePicChangeForm(instance=pro_obj,data=request.POST,files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("profiledetail",pk=id)
    return redirect("profiledetail",pk=id)
    

class ProfileListView(ListView):
    model=UserProfile
    template_name="profile-list.html"
    context_object_name="profiles"

    def get_queryset(self):
        return UserProfile.objects.exclude(user=self.request.user)
    
    def post(self,request,*args,**kwargs):
        pname=request.POST.get("username")
        qs=UserProfile.objects.filter(Q(user__username__icontains=pname)|Q(user__first_name__icontains=pname)|Q(user__last_name__icontains=pname))
        messages.error(request,"result not found")
        return render(request,self.template_name,{"profiles":qs})

   
    
def followView(request,*args,**kwargs):
    id=kwargs.get("pk")
    profile_obj=UserProfile.objects.get(id=id)
    user_obj=request.user.profile
    user_obj.following.add(profile_obj)
    user_obj.save()
    return redirect("profile-list")

def unfollowView(request,*args,**kwargs):
    id=kwargs.get("pk")
    profile_obj=UserProfile.objects.get(id=id)
    user_obj=request.user.profile
    user_obj.following.remove(profile_obj)
    user_obj.save()
    return redirect("profile-list")



  


def SignOutView(request,*args,**kwargs):
    logout(request)
    messages.success(request,"logouted successfully")
    return redirect("signin")
    

    


