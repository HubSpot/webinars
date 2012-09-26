from django.db import models
from sanetime.dj import SaneTimeField
#from webex.webex import WebEx
#from webex.event_controller import WebExEventController


class AccountType(models.Model):
    class Meta:
        app_label = 'webinars'

    name = models.CharField(max_length=64)
    username_label = models.CharField(max_length=64) # webex => hostId
    extra_username_label = models.CharField(max_length=64) # webex => siteId or siteName
    listing_priority = models.IntegerField()
    can_api_create_event = models.BooleanField()
    can_api_load_event = models.BooleanField()
    can_api_register_user = models.BooleanField()
    can_api_report_views = models.BooleanField()

    updated_at = SaneTimeField(auto_now=True)
    created_at = SaneTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    @property
    def image_name(self):
        return 'webex' if self.id in (1,6) else self.name.lower()

    @classmethod
    def account_id_to_name(cls, self):
        cls._account_id_to_name = getattr(cls, '_account_id_to_name', cls.generate_id_to_name())

    @classmethod
    def generate_id_to_name(cls, self):
        return dict([(account_type.id, account_type.name) for account_type in AccountType.objects.all()])

    def is_available(self, hub):
        if self.id==1: 
            return True
        elif self.id==2:
            return True
        return False




