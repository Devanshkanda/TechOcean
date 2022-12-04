from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from blog.models import Post

# html pages
def home(request):
     allPosts= Post.objects.all()
     context={'allPosts': allPosts}
     return render(request, "home/home.html", context)
    

def about(request):
    return render(request,'home/about.html')

def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        issue =request.POST['issue']
        phone = request.POST['phone']
        if len(name)<2 :
            messages.warning(request, "Please Enter correct Name")
        if len(email)<5 :
            messages.warning(request, "Please Enter correct Email")
        if len(issue)<50 :
            messages.warning(request, "Please Write atleast 50 words")
        if len(phone)<10 or len(phone)>10:
            messages.warning(request, "Please Enter correct Phone Number")
        else:
            contact=Contact(name=name, email=email, issue=issue,phone=phone)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    return render(request,'home/contact.html')

def search(request):
    query=request.GET.get('query')
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle= Post.objects.filter(title__icontains=query)
        allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)

#authentication api's

def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        if len(username)<10:
            messages.warning(request, " Your user name must not be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.warning(request, " User name should only contain letters and numbers")
            return redirect('home')
        if (pass1!= pass2):
             messages.warning(request, " Passwords do not match")
             return redirect('home')
        
        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, " Your Account has been successfully created")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")

def handeLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.warning(request, "Invalid credentials! Please try again")
            return redirect("home")

    return HttpResponse("404- Not found")
   

    return HttpResponse("login")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')

