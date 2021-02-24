from django.shortcuts import redirect, render

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
	return render(request, 'bejelentkezes.html')

def regisztracio(request, *args, **kwargs):
	if isLoggedIn(request):
		return redirect('/')
	return render(request, 'regisztracio.html')

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
	context: {
		'termekek': [],
		'mozgasok': [],
	}
	for termek in Etel.objects:
		context['termekek'].append({ 'id': termek.id, 'nev': termek.nev })
	for mozgas in MozgasTipus.objects:
		context['termekek'].append({ 'id': mozgas.id, 'nev': mozgas.nev })
	return render(request, 'beviteli-mezo.html')

def grafikonok(request, *args, **kwargs):
	if not isLoggedIn(request):
		return redirect('/')
	context = {
		'bevitel': {},
		'mozgas': {},
	}
	# result = map(lambda a: { 'kaloria':  }, Bevitel.objects.filter(a => a.felhasznalo.id == request.session['user']['id'])
	context['bevitel']['napi'] = Bevitel.objects.raw('''
		SELECT SUM(`kaloria`) AS `kaloria`, SUM(`zsir`) AS `zsir`, SUM(`feherje`) AS `feherje`, SUM(`szenhidrat`) AS `szenhidrat` FROM `koxapp_bevitel`
		WHERE `felhasznalo_id` = ''' + request.session['user']['id'] + '''
		AND `datum` >= date('now', '-1 day')
	''')[0]
	context['bevitel']['heti'] = Bevitel.objects.raw('''
		SELECT SUM(`kaloria`) AS `kaloria`, SUM(`zsir`) AS `zsir`, SUM(`feherje`) AS `feherje`, SUM(`szenhidrat`) AS `szenhidrat` FROM `koxapp_bevitel`
		WHERE `felhasznalo_id` = ''' + request.session['user']['id'] + '''
		AND `datum` >= date('now', '-7 day')
	''')[0]
	context['bevitel']['havi'] = Bevitel.objects.raw('''
		SELECT SUM(`kaloria`) AS `kaloria`, SUM(`zsir`) AS `zsir`, SUM(`feherje`) AS `feherje`, SUM(`szenhidrat`) AS `szenhidrat` FROM `koxapp_bevitel`
		WHERE `felhasznalo_id` = ''' + request.session['user']['id'] + '''
		AND `datum` >= date('now', '-1 month')
	''')[0]
	context['mozgas']['napi'] = Mozgas.objects.raw('''
		SELECT `koxapp_mozgastipus`.`nev` AS `mozgas`, SUM(`koxapp_mozgas`.`ido`) AS `ido` FROM `koxapp_mozgastipus`
		LEFT JOIN `koxapp_mozgas` ON `koxapp_mozgas`.`tipus_id` = `koxapp_mozgastipus`.`id`
			AND `koxapp_mozgas`.`felhasznalo_id` = ''' + request.session['user']['id'] + '''
			AND `koxapp_mozgas`.`datum` >= date('now', '-1 day')
		GROUP BY `koxapp_mozgas`.`tipus_id`, `koxapp_mozgastipus`.`nev`
	''')
	context['mozgas']['heti'] = Mozgas.objects.raw('''
		SELECT `koxapp_mozgastipus`.`nev` AS `mozgas`, SUM(`koxapp_mozgas`.`ido`) AS `ido` FROM `koxapp_mozgastipus`
		LEFT JOIN `koxapp_mozgas` ON `koxapp_mozgas`.`tipus_id` = `koxapp_mozgastipus`.`id`
			AND `koxapp_mozgas`.`felhasznalo_id` = ''' + request.session['user']['id'] + '''
			AND `koxapp_mozgas`.`datum` >= date('now', '-7 day')
		GROUP BY `koxapp_mozgas`.`tipus_id`, `koxapp_mozgastipus`.`nev`
	''')
	context['mozgas']['havi'] = Mozgas.objects.raw('''
		SELECT `koxapp_mozgastipus`.`nev` AS `mozgas`, SUM(`koxapp_mozgas`.`ido`) AS `ido` FROM `koxapp_mozgastipus`
		LEFT JOIN `koxapp_mozgas` ON `koxapp_mozgas`.`tipus_id` = `koxapp_mozgastipus`.`id`
			AND `koxapp_mozgas`.`felhasznalo_id` = ''' + request.session['user']['id'] + '''
			AND `koxapp_mozgas`.`datum` >= date('now', '-1 month')
		GROUP BY `koxapp_mozgas`.`tipus_id`, `koxapp_mozgastipus`.`nev`
	''')
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
	return render(request, 'grafikonok.html')

# Backend views

def backend_login(request, *args, **kwargs):
	if not isLoggedIn(request.session) and request.method == 'POST' and hasattr(request.POST, 'felhasznalonev') and hasattr(request.POST, 'jelszo'):
		result = Felhasznalo.objects.filter(felhasznalonev = request.POST['felhasznalonev'], jelszo = request.POST['jelszo'])
		if len(result) == 1:
			request.session['user'] = {
				'id': result.id,
				'felhasznalonev': result.felhasznalonev,
				'jelszo': result.jelszo,
			}
			return redirect('/')
		request.session['login_error'] = 'Hibás felhasználónév vagy jelszó'
	return redirect('/bejelentkezes')

def backend_registration(request, *args, **kwargs):
	if not isLoggedIn(request.session) and request.method == 'POST' and hasattr(request.POST, 'felhasznalonev') and hasattr(request.POST, 'jelszo') and hasattr(request.POST, 'szuldatum') and hasattr(request.POST, 'magassag') and hasattr(request.POST, 'suly_akt') and hasattr(request.POST, 'suly_cel') and hasattr(request.POST, 'ferfi'):
		user = Felhasznalo(
			felhasznalonev = request.POST['felhasznalonev'],
			jelszo = request.POST['jelszo'],
			szuldatum = request.POST['szuldatum'],
			magassag = request.POST['magassag'],
			suly_akt = request.POST['suly_akt'],
			suly_cel = request.POST['suly_cel'],
			ferfi = request.POST['ferfi']
		)
		user.save()
		request.session['login_regist'] = True
		return redirect('/bejelentkezes')
	return redirect('/regisztracio')

def backend_logout(request, *args, **kwargs):
	if isLoggedIn(request.session):
		del request.session['user']
	return redirect('/bejelentkezes')

def backend_get_food_details(request, *args, **kwargs):
	pass

def backend_save_intake(request, *args, **kwargs):
	pass

def backend_save_sport(request, *args, **kwargs):
	pass
