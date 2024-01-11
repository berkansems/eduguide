# Eduguide

In order to access admin panel please make a django superuser or simply log in with the following info:
<br>
username: berkan
<br>
password: 123

<hr>


    def sync_order(self, order, _async=True):
        """
        Send order to service
        :param order: object
        :param _async: bool
        :return:
        """
        exception_text_template = """{} //
[ Dopigo Sipariş ID: %(order_id)s (%(service_value)s) ]
[ Gönderilen JSON'ı görmek için sipariş satırındaki butona tıklayın. ]
[ INVEON CEVABI ] %(seperator)s
{}""" % ({'order_id': order.id, 'service_value': order.service_value, 'seperator': "-" * 45})
        # Going to post json object as data argument instead of using self.logger_requests_session.post with json argument,
        # because of the order dictionary has django objects, and needs to serialize with DjangoJSONEncoder
        company = order.owner.company.name
        json_response = 'İstek tamamlanamadı.'
        send_cancel_data = order.owner.company.settings.send_cancel_data
        if not self.configuration.extra_data.get('sync_empty_country', True):
            if not order.shipping_address.country or not order.billing_address.country:
                raise ValueError("Order shipping_address veys billing_address içinde country bilgisi bulunmuyor!")
        if order.status in [order.OS_UNDEFINED, order.OS_PENDING]:
            error_text = "{} Numaralı sipariş gönderilmeye hazır değil".format(order.service_value)
            exception_text = exception_text_template.format(error_text, json_response)
            self.log.exception(exception_text)
            send_error_mail_to_inveon(exception_text, company=company, service_value=order.service_value)
            raise SyncFailed(error_text)
        if order.status == order.OS_CANCELLED and not send_cancel_data:
            raise SyncFailed("Sipariş İPTAL Edilmiş. GÖNDERİLMEYECEK!")
        if not order.intercessor_id and order.status == order.OS_CANCELLED:
            raise SyncFailed("Sipariş Inveon'a iletilmeden önce İPTAL edilmiş. GÖNDERİLMEYECEK!")
        if not order.intercessor_id and order.status == order.OS_SHIPPED:
            raise SyncFailed("Sipariş TY üzerinden iptal edilmiş. Gönderilmeyecek.")
        if not order.intercessor_id and order.status == order.OS_CLAIMED:
            raise SyncFailed("Sipariş iade durumuna dönmüş, Gönderilmeyecek!")

        lock_id = "{}-{}".format(order.owner_id, order.id)
        with advisory_lock(lock_id, wait=False) as acquired:
            if not acquired and _async:
                raise SyncRequiresRetry("Şu an sipariş için bir istek atılıyor, sonra tekrar denenecek", 10)
            order.refresh_from_db()
            request_method = self.logger_requests_session.post
            if order.intercessor_id is not None:
                self.ORDER_END_POINT = '/api/Order/UpdateOrder'
                self.ORDER_URL = "{}{}".format(self.API_AP, self.ORDER_END_POINT)
                request_method = self.logger_requests_session.put

            if self.order_sync_date_limit is not None and order.service_created:
                if order.service_created < self.order_sync_date_limit:
                    error_text = "Sipariş tarihi {} tarihinden geride".format(self.order_sync_date_limit)
                    exception_text = exception_text_template.format(error_text, json_response)
                    self.log.exception(exception_text)
                    send_error_mail_to_inveon(exception_text, company=company, service_value=order.service_value)
                    raise SyncFailed(error_text)
            try:
                headers = {'Content-Type': 'application/json', }
                order_json = json.dumps(self.build_order_dict(order), cls=DjangoJSONEncoder)
                json_response = request_method(
                    self.ORDER_URL,
                    data=order_json,
                    headers=headers,
                    verify=False,
                    timeout=20
                )
                response = json_response.json()
            except AttributeError as aee:
                error_text = aee
                exception_text = exception_text_template.format(error_text, json_response)
                self.log.exception(exception_text)
                send_error_mail_to_inveon(exception_text, company=company, service_value=order.service_value)
                return
            except ValueError as vee:
                error_text = vee
                exception_text = exception_text_template.format(error_text, json_response)
                self.log.exception(exception_text)
                raise SyncFailed(exception_text)
            except SyncFailed as sf:
                raise sf
            except Exception as uee:
                error_text = uee
                exception_text = exception_text_template.format(error_text, json_response)
                self.log.exception(exception_text)
                # if _async:
                #     send_error_mail_to_inveon(exception_text, company=company, service_value=order.service_value)
                #     raise SyncRequiresRetry(exception_text, 360)
                # else:
                raise SyncFailed(exception_text)

            self.send_kibana_message(order.owner,
                                     message=f'iso intercessor_id: {order.intercessor_id}, order_id: {order.id}',
                                     response_text=json_response.text, func_name='sync_order')
            try:
                exception_text = ""
                error_text = ""
                if json_response is not None and json_response.status_code < 300:
                    if response['hasErrors']:
                        response_err = response.get('errors', [])
                        for re_err in response_err:
                            error_text += " | {}".format(re_err)
                            message = (f'iso intercessor_id: {order.intercessor_id},'
                                       f' re_err: {re_err}, order_id: {order.id}')
                            self.send_kibana_message(order.owner, message=message, response_text=json_response.text,
                                                     func_name='sync_order')

                            if re_err.startswith("OrderId-Sipariş daha önce") and \
                                    re_err.endswith("sipariş numarası ile kayıt edilmiştir."):
                                intercessor_id = re_err.replace("OrderId-Sipariş daha önce", "")
                                intercessor_id = intercessor_id.replace("sipariş numarası ile kayıt edilmiştir.", "")
                                intercessor_id = intercessor_id.strip()
                                order.intercessor_id = intercessor_id
                                order.dont_sync = True
                                order.save()
                                default_logger.exception(error_text + " " + self.ORDER_URL)
                                if _async:
                                    raise SyncFailed(error_text + " " + self.ORDER_URL)
                                    # raise SyncRequiresRetry(error_text + " " + self.ORDER_URL, 300)
                                else:
                                    return True
                            elif "Ürün Stokta Yok!" in re_err or "Ürün yayınlanmamaktadır!" in re_err or \
                                    "Ürün sistemden kaldırılmıştır!" in re_err or "sending to Erp now" in re_err:
                                exception_text = f'bu error için tekrar deneme yapılacak: {re_err}'
                                if self.specific_retry_value:
                                    retry_time = 60 * 5

                                else:
                                    try_count = 0
                                    retry_time = 30
                                    ob_up = order.object_updates.last()
                                    if ob_up is not None:
                                        up_sy = ob_up.update_sync.last()
                                        if up_sy is not None:
                                            try_count = up_sy.try_count
                                    if try_count > 5:
                                        retry_time = 60 * int(self.sync_repeat_time)
                                        if "sending to Erp now" in re_err:
                                            if try_count == 6:
                                                retry_time = 30
                                            elif try_count == 7:
                                                retry_time = 45
                                            elif try_count == 8:
                                                retry_time = 60
                                            else:
                                                retry_time = 120

                                raise SyncRequiresRetry(message=exception_text, delay=retry_time)
                            else:
                                exception_text = exception_text_template.format(error_text, response)
                        else:
                            if len(response_err) > 0:
                                error_text = response_err[0]
                            else:
                                error_text = "INVEON'dan bilinmeyen bir hata geldi."
                            exception_text = exception_text_template.format(error_text, response)
                        self.log.exception("INVEON'dan GELEN HATA | " + exception_text)
                        # if _async:
                        #     send_error_mail_to_inveon(exception_text, company=company, service_value=order.service_value)
                        #     raise SyncRequiresRetry(exception_text, 360)
                        # else:
                        raise SyncFailed(exception_text)
                    elif response['result'] is None and response['message']:
                        error_text = response['message']
                        exception_text = exception_text_template.format(error_text, response)
                        self.log.exception(exception_text)
                        # if _async:
                        #     send_error_mail_to_inveon(exception_text, company=company, service_value=order.service_value)
                        #     raise SyncRequiresRetry(exception_text, 360)
                        # else:
                        raise SyncFailed(exception_text)

                    order.dont_sync = True
                    inveon_order_id = response['result']['orderId']

                    if inveon_order_id:
                        order.intercessor_id = inveon_order_id
                    order.save()
                    return True
                else:
                    error_text = "{} |".format(json_response.status_code) + " ".join(
                        (json_response.status_code, response.get('title', ''), 'Trace ID:', response.get('traceId', ''))
                    )
                    exception_text = exception_text_template.format(error_text, json_response)
                    self.log.exception(exception_text)
                    # send_error_mail_to_inveon(exception_text, company=company, service_value=order.service_value)
                    # raise SyncRequiresRetry(error_text, 360)
                    # if _async:
                    #     send_error_mail_to_inveon(exception_text, company=company, service_value=order.service_value)
                    #     raise SyncRequiresRetry(error_text, 360)
                    # else:
                    raise SyncRequiresRetry(error_text, 360)
            except SyncFailed as sf:
                raise sf
            # except SyncRequiresRetry as srr:
            #     self.log.exception(srr.message, exc_info=True)
            #     raise srr
            except Exception as uee:

                try:
                    error_message = response.get('message')
                    error_message += "\\"
                except Exception:
                    error_message = "INVEON'dan GELEN HATA | "
                error_text = " ".join(
                    (error_message + repr(response), 'Trace ID:', response.get('traceId', ''), str(uee))
                )
                exception_text = exception_text_template.format(error_text, repr(json_response))
                self.log.exception(exception_text, exc_info=True)
                # send_error_mail_to_inveon(exception_text, company=company, service_value=order.service_value)
                # raise SyncRequiresRetry(error_text, 360)
                # if _async:
                #     send_error_mail_to_inveon(exception_text, company=company, service_value=order.service_value)
                #     raise SyncRequiresRetry(error_text, 360)
                # else:
                raise SyncFailed(exception_text)
