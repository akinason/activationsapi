from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField

from contrib.utils import generate_random_numbers, generate_random_strings
from storage_backend import PreviewImageStorage

CURRENCY_LIST = ['USD']
LICENSE_TYPE_LIST = ['Monthly', 'Annual']

CURRENCY_CHOICE_LIST = (('USD', 'USD'),)
LICENSE_TYPE_CHOICE_LIST = (('Monthly', 'Monthly'), ('Annual', 'Annual'))


class User(AbstractUser):
    email = models.EmailField(_('email'), blank=False, null=False, unique=True)
    website = models.URLField(_('website'), blank=True)
    mobile = models.CharField(_('mobile'), max_length=20, blank=True)
    access_key = models.CharField(_('access key'), max_length=255, blank=True)
    access_secret = models.CharField(_('access secret'), max_length=255, blank=True)
    rave_public_key = models.CharField(
        _("Flutterwave Public Key"), max_length=255, blank=True,
        help_text=_("Plublic key obtained from https://bit.ly/3aHzeFJ. NB: This link contains a referral id.")
    )
    rave_secret_key = models.CharField(
        _("Flutterwave Secret Key"), max_length=255, blank=True,
        help_text=_("Optional: If provided, we will verify payments before marking them as verified otherwise, we simply mark as verified..")
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', "username"]


class Software(models.Model):
    name = models.CharField("name", max_length=50)
    short_description = models.CharField("short description", max_length=70)
    version = models.CharField("version", max_length=10)
    preview_image = models.FileField(_('preview image'), blank=True, storage=PreviewImageStorage())
    documentation_link = models.URLField(_('documentation link'), blank=True, null=True)
    download_link = models.URLField(_('download link'), blank=True, null=True)
    video_link = models.URLField(_('video link'), blank=True, help_text=_("Provide the link of a playlist or single video."))
    is_active = models.BooleanField(_('is active'), default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='softwares')
    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now_add=True)

    def __str__(self):
        return self.name


class Description(models.Model):
    software = models.ForeignKey(Software, on_delete=models.CASCADE, related_name='descriptions')
    title = models.CharField(_('title'), max_length=50, help_text=_("Maximum Characters 50"))
    content = models.TextField(_('content'))
    index = models.IntegerField(_('index'), help_text=_('indicates the order of the software descriptions'))
    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now_add=True)

    class Meta:
        ordering = ['index', 'id']


class License(models.Model):
    software = models.ForeignKey(Software, on_delete=models.CASCADE, related_name='licenses')
    duration = models.IntegerField(_('duration'), help_text=_('duration in days.'))
    price = models.DecimalField(_('price'), decimal_places=2, help_text=_('precision 2'), max_digits=10)
    currency = models.CharField(_('currency'), max_length=3, choices=CURRENCY_CHOICE_LIST)
    type = models.CharField(_('License Type'), choices=LICENSE_TYPE_CHOICE_LIST, max_length=10)
    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now_add=True)

    def __str__(self):
        return f"{self.type} ({self.price} {self.currency})"

    class Meta:
        unique_together = (('software', 'type'), )


class Order(models.Model):
    license = models.ForeignKey(License, on_delete=models.CASCADE, related_name='orders')
    software = models.ForeignKey(Software, on_delete=models.CASCADE, related_name='orders')
    reference = models.CharField(_("reference"), max_length=50)
    license_key = models.CharField(_("License Key"), max_length=50, blank=True)
    is_used = models.BooleanField(_('is used'), default=False)
    is_paid = models.BooleanField(_('is paid'), default=False)
    is_verified = models.BooleanField(_('is verified'), default=False, help_text=_("indicates if payment is verified."))
    amount = models.DecimalField(_('amount'), decimal_places=4, max_digits=10)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICE_LIST)
    name = models.CharField(_("client name"), max_length=100)
    email = models.EmailField(_("client email"))
    address = models.CharField(_("client address"), max_length=255)
    country = models.CharField(_("client country"), max_length=2)
    mobile = models.CharField(_('mobile'), max_length=20, blank=True)
    payment_response = JSONField(_('payment response'), blank=True, null=True)
    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now_add=True)

    def set_reference(self, length=7):
        if not self.reference:
            reference = generate_random_numbers(length)
            while Order.objects.filter(reference=reference).exists():
                reference = generate_random_numbers(length)
            self.reference = reference

    def set_license_key(self, length=12):
        if not self.license_key:
            self.license_key = generate_random_strings(length)

    @staticmethod
    def format_license_key(license_key):
        lk = license_key
        return ' '.join([lk[i:i + 3] for i in range(0, len(lk), 3)])

    @staticmethod
    def get_order_using_email_and_license_key(email, license_key):
        lk = str(license_key).replace(" ", "")
        try:
            order = Order.objects.filter(email=email, license_key=lk)[:1].get()
            return order
        except Order.DoesNotExist:
            return None

    @staticmethod
    def get_order_using_reference_and_license_key(reference, license_key):
        lk = str(license_key).replace(" ", "")
        try:
            order = Order.objects.filter(reference=reference, license_key=lk).get()
            return order
        except Order.DoesNotExist:
            return None


    @staticmethod
    def get_order_using_reference(reference):
        try:
            order = Order.objects.filter(reference=reference).get()
            return order
        except Order.DoesNotExist:
            return None
