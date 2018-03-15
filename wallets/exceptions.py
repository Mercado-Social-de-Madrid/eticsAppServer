# coding=utf-8
import json

from django.core.exceptions import PermissionDenied
from tastypie.http import HttpUnauthorized


class WrongPinCode(PermissionDenied):
    """ Exception when the user enters an incorrect pincode """
    def __init__(self, wallet=None):

        response = {
            'error': 'wrong_pincode',
            'message': 'El código pin introducido no es correcto'
        }

        self.response = HttpUnauthorized(content=json.dumps(response), content_type='application/json')


class NotEnoughBalance(Exception):
    """ Exception when a transaction is being made but the wallet doesnt have enough cash """
    def __init__(self, wallet=None):

        response = {
            'error': 'not_enough_balance',
            'message': 'El monedero no tiene suficiente saldo disponible para realizar la operación'
        }

        self.response = HttpUnauthorized(content=json.dumps(response), content_type='application/json')



