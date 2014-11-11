from django.core.exceptions import ValidationError


def validate_msisdn(msisdn):
    if len(str(msisdn)) < 10:
        raise ValidationError('MSISDN must have 10 or 11 digits. Expected format: DDD + Number')
