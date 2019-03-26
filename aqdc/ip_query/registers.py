from django.urls import converters

'''
    ATTENTION:
        the chars like '^' or '$' cannot be used in regex!!!
'''


class IpConverter(converters.SlugConverter):
    """match Chinese, _, 0-9, a-Z, A-Z"""
    regex = r"(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})(\.(2(5[0-5]{1}|[0-4]\d{1})|[0-1]?\d{1,2})){3}"
