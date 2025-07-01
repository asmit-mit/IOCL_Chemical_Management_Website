from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render


# Create your views here.
def user_login(request):
    try:
        if request.POST:
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login Successful!")
                return redirect("entryform")
            else:
                messages.success(request, "Incorrect Login Credentials.")
                redirect("user_login")
    except Exception as e:
        messages.success(request, f"Error: {e}. Please login again.")
        redirect("user_login")

    return render(request, "login_page.html")
