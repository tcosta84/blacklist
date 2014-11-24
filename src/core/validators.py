from django.core.exceptions import ValidationError


def validate_msisdn(msisdn):
    msisdn = str(msisdn)

    if len(msisdn) < 12:
        raise ValidationError('MSISDN must have 12 or 13 digits')

    if len(msisdn) > 13:
        raise ValidationError('MSISDN must have 12 or 13 digits. Given: %s' % (len(msisdn), ))

    if msisdn[0:2] != '55':
        raise ValidationError('MSISDN must start with 55')
