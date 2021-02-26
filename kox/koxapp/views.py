import datetime
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.db import connection
from koxapp.models import Felhasznalo, Bevitel, MozgasTipus, Mozgas, Etel

# Create your views here.

def isLoggedIn(request):
	if 'user' in request.session:
		result = Felhasznalo.objects.filter(id = request.session['user']['id'], felhasznalonev = request.session['user']['felhasznalonev'], jelszo = request.session['user']['jelszo'])
		if len(result) == 1:
			return True
		else:
			del request.session['user']
	return False

# Frontend views

def root(request, *args, **kwargs):
	if isLoggedIn(request):
		return redirect('/beviteli-mezo')
	return redirect('/bejelentkezes')

def bejelentkezes(request, *args, **kwargs):
	if isLoggedIn(request):
		return redirect('/')
	login_error = False
	login_regist = False
	if 'login_error' in request.session:
		login_error = True
		del request.session['login_error']
	if 'login_regist' in request.session:
		login_regist = True
		del request.session['login_regist']
	return render(request, 'bejelentkezes.html', { 'login_error': login_error, 'login_regist': login_regist })

def regisztracio(request, *args, **kwargs):
	if isLoggedIn(request):
		return redirect('/')
	regist_error = False
	if 'regist_error' in request.session:
		regist_error = True
		del request.session['regist_error']
	return render(request, 'regisztracio.html', { 'regist_error': regist_error })

def adatok(request, *args, **kwargs):
	if not isLoggedIn(request):
		return redirect('/')
	result = Felhasznalo.objects.filter(id = request.session['user']['id'])[0]
	context = {
		'felhasznalonev': result.felhasznalonev,
		'szuldatum': result.szuldatum,
		'magassag': result.magassag,
		'suly_akt': result.suly_akt,
		'suly_cel': result.suly_cel,
	}
	return render(request, 'adatok.html', context)

def beviteli_mezo(request, *args, **kwargs):
	if not isLoggedIn(request):
		return redirect('/')
	context = {
		'termekek': [],
		'mozgasok': [],
	}
	for termek in Etel.objects.all():
		context['termekek'].append({ 'id': termek.id, 'nev': termek.nev })
	for mozgas in MozgasTipus.objects.all():
		context['mozgasok'].append({ 'id': mozgas.id, 'nev': mozgas.nev })
	return render(request, 'beviteli-mezo.html', context)

def grafikonok(request, *args, **kwargs):
	if not isLoggedIn(request):
		return redirect('/')
	context = {
		'bevitel': {},
		'mozgas': {},
	}
	# result = map(lambda a: { 'kaloria':  }, Bevitel.objects.filter(a => a.felhasznalo.id == request.session['user']['id'])
	cursor = connection.cursor()
	context['bevitel']['napi'] = Bevitel.getStat(cursor, request.session['user']['id'], 'daily')
	context['bevitel']['heti'] = Bevitel.getStat(cursor, request.session['user']['id'], 'weekly')
	context['bevitel']['havi'] = Bevitel.getStat(cursor, request.session['user']['id'], 'monthly')
	context['mozgas']['napi'] = Mozgas.getStat(cursor, request.session['user']['id'], 'daily')
	context['mozgas']['heti'] = Mozgas.getStat(cursor, request.session['user']['id'], 'weekly')
	context['mozgas']['havi'] = Mozgas.getStat(cursor, request.session['user']['id'], 'monthly')
	# elmúlt 24 óra
	# napi bevitel:
	#	- Kcal
	#	- Zsír
	#	- Fehérje
	#	- Szénhidrát
	# heti bevitel:
	#	- Kcal
	#	- Zsír
	#	- Fehérje
	#	- Szénhidrát
	# havi bevitel:
	#	- Kcal
	#	- Zsír
	#	- Fehérje
	#	- Szénhidrát
	# napi mozgás:
	#	- gyaloglás
	#	- futás
	#	- úszás
	#	- kerékpározás
	# heti mozgás:
	#	- gyaloglás
	#	- futás
	#	- úszás
	#	- kerékpározás
	# havi mozgás:
	#	- gyaloglás
	#	- futás
	#	- úszás
	#	- kerékpározás
	return render(request, 'grafikonok.html', context)

# Backend views

def backend_login(request, *args, **kwargs):
	if not isLoggedIn(request) and request.method == 'POST':
		result = Felhasznalo.objects.filter(felhasznalonev = request.POST['felhasznalonev'], jelszo = request.POST['jelszo'])
		if len(result) == 1:
			request.session['user'] = {
				'id': result[0].id,
				'felhasznalonev': result[0].felhasznalonev,
				'jelszo': result[0].jelszo,
			}
			return redirect('/')
		request.session['login_error'] = True
	return redirect('/bejelentkezes')

def backend_registration(request, *args, **kwargs):
	if not isLoggedIn(request) and request.method == 'POST':
		result = Felhasznalo.objects.filter(felhasznalonev = request.POST['felhasznalonev'])
		if len(result) != 0:
			request.session['regist_error'] = True
			return redirect('/regisztracio')
		user = Felhasznalo(
			felhasznalonev = request.POST['felhasznalonev'],
			jelszo = request.POST['jelszo'],
			szuldatum = request.POST['szuldatum'],
			magassag = request.POST['magassag'],
			suly_akt = request.POST['suly_akt'],
			suly_cel = request.POST['suly_cel'],
			ferfi = 'ferfi' in request.POST
		)
		user.save()
		request.session['login_regist'] = True
		return redirect('/bejelentkezes')
	return redirect('/regisztracio')

def backend_logout(request, *args, **kwargs):
	if isLoggedIn(request):
		del request.session['user']
	return redirect('/bejelentkezes')

def backend_get_food_details(request, *args, **kwargs):
	if not isLoggedIn(request):
		return JsonResponse({'success': False, 'message': 'Nincs bejelentkezve'})
	if request.method != 'POST':
		return JsonResponse({'success': False, 'message': 'Hibás kérés'})
	result = Etel.objects.filter(id = request.POST['id'])
	if len(result) == 0:
		return JsonResponse({'success': False, 'message': 'A kért termék nem található'})
	response_data = {
		'success': True,
		'data': {
			'zsir': result[0].zsir,
			'feherje': result[0].feherje,
			'szenhidrat': result[0].szenhidrat,
		}
	}
	return JsonResponse(response_data)

def backend_save_intake(request, *args, **kwargs):
	if not isLoggedIn(request):
		return redirect('/')
	if request.method != 'POST':
		return redirect('/beviteli-mezo')
	mennyiseg = int(request.POST['mennyiseg'])
	kaloria = int(request.POST['kaloria']) * mennyiseg / 100
	zsir = int(request.POST['zsir']) * mennyiseg / 100
	feherje = int(request.POST['feherje']) * mennyiseg / 100
	szenhidrat = int(request.POST['szenhidrat']) * mennyiseg / 100
	intake = Bevitel(
		felhasznalo = Felhasznalo.objects.filter(id = request.session['user']['id'])[0],
		datum = datetime.datetime.now(),
		kaloria = kaloria,
		zsir = zsir,
		feherje = feherje,
		szenhidrat = szenhidrat
	)
	intake.save()
	return redirect('/beviteli-mezo')

def backend_save_sport(request, *args, **kwargs):
	if not isLoggedIn(request):
		return redirect('/')
	if request.method != 'POST':
		return redirect('/beviteli-mezo')
	sport = Mozgas(
		felhasznalo = Felhasznalo.objects.filter(id = request.session['user']['id'])[0],
		datum = datetime.datetime.now(),
		tipus = MozgasTipus.objects.filter(id = int(request.POST['tipus_id']))[0],
		ido = int(request.POST['ido'])
	)
	sport.save()
	return redirect('/beviteli-mezo')

def backend_change_userdata(request, *args, **kwargs):
	if not isLoggedIn(request):
		return redirect('/')
	if request.method != 'POST':
		return redirect('/adatok')
	Felhasznalo.objects.filter(id = request.session['user']['id']).update(magassag = 0 if request.POST['magassag'] == '' else request.POST['magassag'], suly_akt = 0 if request.POST['suly_akt'] == '' else request.POST['suly_akt'], suly_cel = 0 if request.POST['suly_cel'] == '' else request.POST['suly_cel'])
	if 'jelszo' in request.POST and request.POST['jelszo'] != '':
		Felhasznalo.objects.filter(id = request.session['user']['id']).update(jelszo = request.POST['jelszo'])
	return redirect('/adatok')
