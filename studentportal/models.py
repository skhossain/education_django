from django.db import models

class Education_Branch(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.branch_code)
