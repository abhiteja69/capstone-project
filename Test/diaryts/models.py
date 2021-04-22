from django.db import models

from django.urls import reverse
from Test import settings
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from django.contrib.auth.models import User
User = get_user_model()

class Diaryt(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
   # seen_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='supervisor', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)
   # category = models.IntegerField(choices=CRIME_CATEGORY, default=1)
    description = models.TextField(max_length=200)
    #emotion = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)
    #status = models.CharField(max_length=100)
    def emotion(self):
       emo=self.description
       authenticator = IAMAuthenticator('VDDyBH9uCNhaX13ZNTh6KHg3DGVPW6XJpPyjl3XkE0QV')
       tone_analyzer = ToneAnalyzerV3(version={'2017-09-21'},authenticator=authenticator)
       tone_analyzer.set_service_url('https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/ec037f03-517d-4c25-acc5-b02033dc8ece')
       tone_analysis = tone_analyzer.tone(emo,content_type='text/plain').get_result()
       return(tone_analysis['document_tone']['tones'][0]['tone_name'])
    def get_absolute_url(self):
        return reverse('accounts:dashboard')

    def __str__(self):
        return self.title