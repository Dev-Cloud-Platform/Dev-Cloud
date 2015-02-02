# -*- coding: utf-8 -*-
# @COPYRIGHT_begin
#
# Copyright [2015] Michał Szczygieł, M4GiK Software
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @COPYRIGHT_end

from smtplib import SMTPRecipientsRefused

from django.core.mail import get_connection
from django.core.mail.message import EmailMultiAlternatives
from django.template import loader, Context
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from core.common import log
from core.settings import common
from core.utils.exception import DevCloudException
from database.models import Users


def email_error(f):
    """
    Decorator for catching exception with sending emails' error.

    @par Decorated function's declaration
    @code
    @email_error
    function (request, *args, **kw)
    @endcode

    @par Decorated function's call
    @code
    function (request, *arg, **kw)
    @endcode
    """

    def wrap(request, *args, **kwds):
        try:
            return f(request, *args, **kwds)
        except SMTPRecipientsRefused, e:
            error = "%s %s" % (f.__name__, str(e))
            log.error(0, error)
            raise

    return wrap


@email_error
def send(to_address, html_content, subject):
    """
    @parameter{to_address,string} addressee of the email
    @parameter{msg_text,string} contents of the email
    @parameter{subject,string} subject of the email

    Sends email via STMP server.
    """
    from_address = common.EMAIL
    log.debug(0, '%s%s%s%s%s%s%s' % (
        "send_email(from='", from_address, "', to='", to_address, "', subject='", subject, "')"))

    txt_content = strip_tags(html_content)

    connection = get_connection(use_tls=common.EMAIL_USE_TLS,
                                host=common.EMAIL_HOST,
                                port=common.EMAIL_PORT,
                                username=common.EMAIL_HOST_USER,
                                password=common.EMAIL_HOST_PASSWORD,
                                backend=common.EMAIL_BACKEND,
                                fail_silently=common.EMAIL_FAIL_SILENTLY)

    message = EmailMultiAlternatives(subject, txt_content, from_address, [to_address], connection=connection)
    message.attach_alternative(html_content, "text/html")
    message.send()


def send_activation_email(activation_key, user, dev_cloud_data):
    """
    @parameter{activation_key,string} activation key to be sent
    @parameter{user,string} username of the user to activate
    @parameter{dev_cloud_data}

    Sends email with activation key to registred user.
    """
    dev_cloud_dict = {'activation_key': activation_key,
                      'site': dev_cloud_data['site_domain'],
                      'site_name': dev_cloud_data['site_name']}

    subject = render_from_template_to_string('registration_msg/activation_email_subject', dev_cloud_dict)
    subject = ''.join(subject.splitlines())
    message = render_from_template_to_string('registration_msg/activation_email', dev_cloud_dict)

    send(user.email, message, subject)


def send_activation_confirmation_email(user, dev_cloud_data):
    """
    @parameter{user,string} username of the user to activate
    @parameter{dev_cloud_data,dict}, \n fields:
    @dictkey{site_domain,string}
    @dictkey{site_name,string}

    Sends confirmation email to user as admin confirms user's activation.
    """
    dev_cloud_dict = {'site': dev_cloud_data['site_domain'],
                      'site_name': dev_cloud_data['site_name']}
    subject = render_from_template_to_string('registration_msg/admin_activation_email_subject', dev_cloud_dict)
    subject = ''.join(subject.splitlines())
    message = render_from_template_to_string('registration_msg/admin_activation_email', dev_cloud_dict)

    send(user.email, message, subject)


def send_admin_registration_notification(user, dev_cloud_data):
    """
    @parameter{user}
    @parameter{dev_cloud_data,dict}, \n fields:
    @dictkey{site_name,string}

    Sends notification to admin about a newly registered user.
    """
    dev_cloud_dict = {'site_name': dev_cloud_data['site_name']}
    subject = render_from_template_to_string('registration_msg/admin_notify_email_subject', dev_cloud_dict)
    subject = ''.join(subject.splitlines())
    message = render_from_template_to_string('registration_msg/admin_notify_email', user)

    for admin in Users.objects.filter(is_superuser=True):
        send(admin.email, message, subject)

    send(common.EMAIL, message, subject)


def send_reset_password_mail(user, token, dev_cloud_data):
    """
    @parameter{user,string} username of the user to reset password
    @parameter{token,string}
    @parameter{dev_cloud_data,dict}, \n fields:
    @dictkey{site_domain,string}
    @dictkey{site_name,string}

    Sends mail for password reset.
    """
    dev_cloud_dict = {'site_name': dev_cloud_data['site_name'],
                      'domain': dev_cloud_data['site_domain'],
                      'username': user.login,
                      'token': token}
    message = render_from_template_to_string('account_msg/password_reset_email', dev_cloud_dict)

    send(user.email, message, _("Password reset on %s") % dev_cloud_data['site_name'])


def send_block_email(user, block, dev_cloud_data):
    """
    @parameter{user,string} username of the user to reset password
    @parameter{block,boolean} whether to block or unblock.
    @parameter{dev_cloud_data,dict}, \n fields:
    @dictkey{site_name,string}
    """
    dev_cloud_dict = {}
    if block:
        send(user.email,
             render_from_template_to_string('account_msg/block_email', dev_cloud_dict),
             _("User account blocked on %s") % dev_cloud_data['site_name'])
    else:
        send(user.email,
             render_from_template_to_string('account_msg/unblock_email', dev_cloud_dict),
             _("User account unblocked on %s") % dev_cloud_data['site_name'])


def send_contact_message(subject, msg):
    """
    Method sends message with content.
    @param subject:
    @param msg:
    @return:
    """
    message_dict = {'subject': subject, 'content': msg}
    message = render_from_template_to_string('contact/contact_message', message_dict)
    send(common.EMAIL, message, subject)


def render_from_template_to_string(template_filename, dev_cloud_dict={}):
    """
    @parameter{template_filename,string} path to template of the email
    @parameter{ctx_dict,dict} params to be filled in the email

    Renders strings which can be sent as email contents (basing on template and
    data to be filled in).

    @raises{clm_template_create,CLMException}
    """

    try:
        template = loader.get_template(template_filename)
    except Exception, e:
        log.error(0, "Cannot load template. Error: %s" % str(e))
        raise DevCloudException('template_create')

    return template.render(Context(dev_cloud_dict))
