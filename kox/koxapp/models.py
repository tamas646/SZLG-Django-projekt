from django.db import models

# Create your models here.

class Felhasznalo(models.Model):
	felhasznalonev = models.CharField(max_length = 255, unique = True)
	jelszo = models.CharField(max_length = 255)
	szuldatum = models.DateField()
	magassag = models.IntegerField()
	suly_akt = models.IntegerField()
	suly_cel = models.IntegerField()
	ferfi = models.BooleanField()

	def __str__(self):
		return f"{self.felhasznalonev} [{self.id}]"

class Bevitel(models.Model):
	felhasznalo = models.ForeignKey(Felhasznalo, on_delete = models.CASCADE)
	datum = models.DateTimeField()
	kaloria = models.IntegerField()
	zsir = models.IntegerField()
	feherje = models.IntegerField()
	szenhidrat = models.IntegerField()

	@staticmethod
	def getStat(db_cursor, user_id, period):
		if period == 'daily':
			return db_cursor.execute('''
				SELECT (CASE WHEN SUM(`kaloria`) IS NOT NULL THEN SUM(`kaloria`) ELSE 0 END) AS `kaloria`, (CASE WHEN SUM(`zsir`) IS NOT NULL THEN SUM(`zsir`) ELSE 0 END) AS `zsir`, (CASE WHEN SUM(`feherje`) IS NOT NULL THEN SUM(`feherje`) ELSE 0 END) AS `feherje`, (CASE WHEN SUM(`szenhidrat`) IS NOT NULL THEN SUM(`szenhidrat`) ELSE 0 END) AS `szenhidrat` FROM `koxapp_bevitel`
				WHERE `felhasznalo_id` = ''' + str(user_id) + '''
				AND `datum` >= date('now', '-1 day')
			''').fetchone()
		elif period == 'weekly':
			return db_cursor.execute('''
				SELECT (CASE WHEN SUM(`kaloria`) IS NOT NULL THEN SUM(`kaloria`) ELSE 0 END) AS `kaloria`, (CASE WHEN SUM(`zsir`) IS NOT NULL THEN SUM(`zsir`) ELSE 0 END) AS `zsir`, (CASE WHEN SUM(`feherje`) IS NOT NULL THEN SUM(`feherje`) ELSE 0 END) AS `feherje`, (CASE WHEN SUM(`szenhidrat`) IS NOT NULL THEN SUM(`szenhidrat`) ELSE 0 END) AS `szenhidrat` FROM `koxapp_bevitel`
				WHERE `felhasznalo_id` = ''' + str(user_id) + '''
				AND `datum` >= date('now', '-7 day')
			''').fetchone()
		elif period == 'monthly':
			return db_cursor.execute('''
				SELECT (CASE WHEN SUM(`kaloria`) IS NOT NULL THEN SUM(`kaloria`) ELSE 0 END) AS `kaloria`, (CASE WHEN SUM(`zsir`) IS NOT NULL THEN SUM(`zsir`) ELSE 0 END) AS `zsir`, (CASE WHEN SUM(`feherje`) IS NOT NULL THEN SUM(`feherje`) ELSE 0 END) AS `feherje`, (CASE WHEN SUM(`szenhidrat`) IS NOT NULL THEN SUM(`szenhidrat`) ELSE 0 END) AS `szenhidrat` FROM `koxapp_bevitel`
				WHERE `felhasznalo_id` = ''' + str(user_id) + '''
				AND `datum` >= date('now', '-1 month')
			''').fetchone()
		else:
			raise Exception(f"Unknown period '{period}'")

	def __str__(self):
		return f"{self.felhasznalo.felhasznalonev} ({self.datum}) - kalória: {self.kaloria} ({self.zsir}, {self.feherje}, {self.szenhidrat}) [{self.id}]"

class MozgasTipus(models.Model):
	nev = models.CharField(max_length = 255)
	orankent = models.IntegerField()

	def __str__(self):
		return f"{self.nev} [{self.id}]"

class Mozgas(models.Model):
	felhasznalo = models.ForeignKey(Felhasznalo, on_delete = models.CASCADE)
	datum = models.DateTimeField()
	tipus = models.ForeignKey(MozgasTipus, on_delete = models.CASCADE)
	ido = models.IntegerField()

	@staticmethod
	def getStat(db_cursor, user_id, period):
		if period == 'daily':
			return db_cursor.execute('''
				SELECT `koxapp_mozgastipus`.`nev` AS `mozgas`, (CASE WHEN SUM(`koxapp_mozgas`.`ido`) IS NOT NULL THEN SUM(`koxapp_mozgas`.`ido`) ELSE 0 END) AS `ido` FROM `koxapp_mozgastipus`
				LEFT JOIN `koxapp_mozgas` ON `koxapp_mozgas`.`tipus_id` = `koxapp_mozgastipus`.`id`
					AND `koxapp_mozgas`.`felhasznalo_id` = ''' + str(user_id) + '''
					AND `koxapp_mozgas`.`datum` >= date('now', '-1 day')
				GROUP BY `koxapp_mozgas`.`tipus_id`, `koxapp_mozgastipus`.`nev`
			''').fetchall()
		elif period == 'weekly':
			return db_cursor.execute('''
				SELECT `koxapp_mozgastipus`.`nev` AS `mozgas`, (CASE WHEN SUM(`koxapp_mozgas`.`ido`) IS NOT NULL THEN SUM(`koxapp_mozgas`.`ido`) ELSE 0 END) AS `ido` FROM `koxapp_mozgastipus`
				LEFT JOIN `koxapp_mozgas` ON `koxapp_mozgas`.`tipus_id` = `koxapp_mozgastipus`.`id`
					AND `koxapp_mozgas`.`felhasznalo_id` = ''' + str(user_id) + '''
					AND `koxapp_mozgas`.`datum` >= date('now', '-7 day')
				GROUP BY `koxapp_mozgas`.`tipus_id`, `koxapp_mozgastipus`.`nev`
			''').fetchall()
		elif period == 'monthly':
			return db_cursor.execute('''
				SELECT `koxapp_mozgastipus`.`nev` AS `mozgas`, (CASE WHEN SUM(`koxapp_mozgas`.`ido`) IS NOT NULL THEN SUM(`koxapp_mozgas`.`ido`) ELSE 0 END) AS `ido` FROM `koxapp_mozgastipus`
				LEFT JOIN `koxapp_mozgas` ON `koxapp_mozgas`.`tipus_id` = `koxapp_mozgastipus`.`id`
					AND `koxapp_mozgas`.`felhasznalo_id` = ''' + str(user_id) + '''
					AND `koxapp_mozgas`.`datum` >= date('now', '-1 month')
				GROUP BY `koxapp_mozgas`.`tipus_id`, `koxapp_mozgastipus`.`nev`
			''').fetchall()
		else:
			raise Exception(f"Unknown period '{period}'")

	def __str__(self):
		return f"{self.felhasznalo.felhasznalonev} ({self.datum}) - típus: {self.tipus.nev} ({self.ido} perc) [{self.id}]"

class Etel(models.Model):
	nev = models.CharField(max_length = 255)
	zsir = models.IntegerField()
	feherje = models.IntegerField()
	szenhidrat = models.IntegerField()

	def __str__(self):
		return f"{self.nev} [{self.id}]"
