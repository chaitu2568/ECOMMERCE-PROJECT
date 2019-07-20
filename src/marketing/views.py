from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.views.generic import UpdateView
from django.shortcuts import render, redirect
from .forms import MarketingPreferenceForm
from .models import MarketingPreference
from django.conf import settings
from .utils import Mailchimp
from .mixins import CsrfExemptMixin
from django.views.generic import UpdateView, View

MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)

class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarketingPreferenceForm
    template_name = 'base/forms.html' # yeah create this
    success_url = '/settings/email/'
    success_message = 'Your Email Subscriptions have been updated. Thank you.'


    # If the user is not authenticated then it is redirected to login page
    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated():
            return redirect("/login/?next=/settings/email/") # HttpResponse("Not allowed", status=400)
        return super(MarketingPreferenceUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Email Preferences'
        return context

    def get_object(self):
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user) # get_absolute_url
        return obj

# Method:POST
# "root":
# "type": "subscribe"
# "fired_at": "2019-07-20 22:34:26"
# "data":
# "id": "97ec415b05"
# "email": "kbogaval@gmail.com"
# "email_type": "html"
# "ip_opt": "72.201.13.9"
# "web_id": "347480181"
# "merges":
# "EMAIL": "kbogaval@gmail.com"
# "FNAME": ""
# "LNAME": ""
# "ADDRESS": ""
# "PHONE": ""
# "BIRTHDAY": ""
# "list_id": "b5113c5eb4"
# host: en37vuw88zr6w.x.pipedream.net
# Content-Type: application/x-www-form-urlencoded
# User-Agent: MailChimp
# Content-Length: 418
# Connection: keep-alive

class MailchimpWebhookView(CsrfExemptMixin, View):
    # def get(self, request, *args, **kwargs):
    #     return HttpResponse("Thank you", status=200)
    def post(self, request, *args, **kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            hook_type = data.get("roottype]")
            email = data.get('data[email]')
            response_status, response = Mailchimp().check_subcription_status(email)
            sub_status  = response['status']
            is_subbed = None
            mailchimp_subbed = None
            if sub_status == "subscribed":
                is_subbed, mailchimp_subbed  = (True, True)
            elif sub_status == "unsubscribed":
                is_subbed, mailchimp_subbed  = (False, False)
            if is_subbed is not None and mailchimp_subbed is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(
                            subscribed=is_subbed,
                            mailchimp_subscribed=mailchimp_subbed,
                            mailchimp_msg=str(data))
        return HttpResponse("Thank you", status=200)


