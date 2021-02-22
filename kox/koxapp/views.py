from django.shortcuts import redirect, render

# Create your views here.

def isLoggedIn(request):
	if 'user' in request.session:
		result = User.objects.filter(id = request.session['user']['id'], felhasznalonev = request.session['user']['felhasznalonev'], jelszo = request.session['user']['jelszo'])
		if len(result) == 1:
			return True
		else:
			del request.session['user']
	return False

def root(request, *args, **kwargs):
	if isLoggedIn(request):
		return redirect('/beviteli-mezo')
	return redirect('/bejelentkezes')

def bejelentkezes(request, *args, **kwargs):
	if isLoggedIn(request):
		return redirect('/')
	return render(request, 'bejelentkezes.html')

def regisztracio(request, *args, **kwargs):
	if isLoggedIn(request):
		return redirect('/')
	return render(request, 'regisztracio.html')

def adatok(request, *args, **kwargs):
	if not isLoggedIn(request):
		return redirect('/')
	return render(request, 'adatok.html')

def beviteli_mezo(request, *args, **kwargs):
	if not isLoggedIn(request):
		return redirect('/')
	return render(request, 'beviteli-mezo.html')

def grafikonok(request, *args, **kwargs):
	if not isLoggedIn(request):
		return redirect('/')
	return render(request, 'grafikonok.html')
