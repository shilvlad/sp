from django.shortcuts import render

# Create your views here.
def start(request):
    return render(request, 'portal/index.html', {})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print ("Invalid login details:")

            return HttpResponse("Invalid login details supplied.")

def user_logout(request):
    logout(request)
    return render(request, 'portal/index.html',{})