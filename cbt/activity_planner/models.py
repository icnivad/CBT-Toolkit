from django.db import models

# Create your models here.

class Mood(models.Model):
	feeling=models.CharField(blank=True, max_length=100)
	mood=models.IntegerField(blank=True, null=True)
	user=models.ForeignKey(User)
	datetime=models.DateTimeField('time')
	def save(self):
		if not self.datetime:
			self.datetime=datetime.datetime.now()
		super(Mood, self).save()
		
	def __unicode__(self):
		return str(self.mood)
	
#	def pretty_date(self):
#		return datetime_helper.pretty_date(self.datetime)

def MoodTest(models.Model):
	situation=models.TextField()
	created_by=models.ForeignKey(User)
	avg_mood_true=models.FloatField()
	avg_mood_false=models.FloatField()

def MoodTestCase(models.Model):
	mood=models.ForeignKey(Mood)
	created_by=models.ForeignKey(User)
	test=models.ForeignKey(MoodTest)
	comments=models.TextField(blank=True, null=True)
	
	#what did you decide to do?
	choice=models.BooleanField()