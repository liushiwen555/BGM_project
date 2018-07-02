from django.core.validators import RegexValidator

MAC_VALIDATOR = RegexValidator(regex=r'^([0-9A-F]{2}:){5}[0-9A-F]{2}$',
                                  message='Enter a valid MAC address, for example "12:AD:34:EC:4D:1B".')