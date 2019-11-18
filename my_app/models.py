from django.db import models

class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    #Admin will conver Search to Searchs so need to modify the 
    #the Meta to correct the correct spelling
    class Meta:
        verbose_name_plural = 'Searches'

    def __str__(self):
        return f'{self.search}'
