# from account.models import EmailAddress

# from geowatchutil.base import GeoWatchError

from django.conf import settings
# from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template import Context


from geonode.contrib.geowatch.broker.base import GeoNodeBroker


class GeoNodeBrokerMetadata(GeoNodeBroker):
    """
    GeoNodeBrokerMetatdata is a bot that checks new layers for missing metdata.
    If the new layer is missing metadata, the broker will send notifications.
    """

    def _pre(self):
        pass

    # def _send_email(self, to_email=None, site_name=None, text_content=None, html_content=None):
    def _send_email(self, **kwargs):
        print kwargs
        site_name = kwargs.get('site_name', None)
        to_email = kwargs.get('to_email', None)
        text_content = kwargs.get('text_content', None)
        html_content = kwargs.get('html_content', None)
        return
        subject = site_name+": Missing metadata on Layer"
        from_email = settings.DEFAULT_FROM_EMAIL
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def _post(self, messages=None):
        for m in messages:
            # print "Message: ", m
            data = m[u'data']
            site_name = data[u'site_name']
            owner = self._get_owner(data)
            instance = self._get_instance(data)
            to_email = self._get_email(owner)
            print "Instance: ", instance
            if instance and to_email:
                fields = []

                if not instance.regions.all():
                    fields.append("regions")

                if not instance.keywords.all():
                    fields.append("keywords")

                if fields:
                    context = Context({
                        'username': data[u'owner_name'],
                        'fields': fields,
                        'site_name': site_name,
                        'baseurl': data[u'baseurl'],
                        'typename': data[u'service_typename'],
                        'url_detail': data[u'url_detail']
                    })
                    text_content = self._render_template(context=context, template="geowatch/email_metadata.txt")
                    html_content = self._render_template(context=context, template="geowatch/email_metadata.html")
                    print "Email HTML Content:"
                    print html_content
                    self._send_email(
                        site_name=site_name,
                        to_email=to_email,
                        text_content=text_content,
                        html_content=html_content)

    def __init__(self, name, description, consumers=None, filter_metadata=None, producers=None, stores_out=None, sleep_period=5, count=1, timeout=5, deduplicate=False, verbose=False):  # noqa
        super(GeoNodeBrokerMetadata, self).__init__(
            name,
            description,
            consumers=consumers,
            producers=producers,
            stores_out=stores_out,
            count=count,
            threads=1,
            sleep_period=sleep_period,
            timeout=timeout,
            deduplicate=deduplicate,
            filter_metadata=filter_metadata,
            verbose=verbose)
