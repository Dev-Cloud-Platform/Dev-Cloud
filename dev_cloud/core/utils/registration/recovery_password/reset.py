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
from core.settings import common
from core.utils.exception import DevCloudException
from core.utils.registration import mail
from database.models import Users
from core.utils.registration.recovery_password.token_generator import default_token_generator as token_generator


def reset_password_mail(email, dev_cloud_data):
    """
    Sends mail for reseting password
    @clmview_guest
    @parameter{email,string} whom send mail for resetting password to
    @parameter{wi_data,dict} fields:
    @dictkey{site_domain}
    @dictkey{site_name}
    """
    if common.MAILER_ACTIVE:
        user = Users.objects.get(email=email)
        token = token_generator.make_token(user)
        try:
            mail.send_reset_password_mail(user, token, dev_cloud_data)
            return True
        except SMTPRecipientsRefused:
            raise DevCloudException('reset_password_smtp_error')
    raise DevCloudException('reset_password_error')