from django.db import models

# Create your models here.

class Felhasznalo(models.Model):
	felhasznalonev = models.CharField(max_length = 255)
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

	def __str__(self):
		return f"{self.felhasznalo.felhasznalonev} ({self.datum}) - típus: {self.tipus.nev} ({self.ido} perc) [{self.id}]"
