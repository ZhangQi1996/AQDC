from django.urls import converters

'''
    ATTENTION:
        the chars like '^' or '$' cannot be used in regex!!!
'''


class CommonConverter(converters.SlugConverter):
    """match Chinese, _, 0-9, a-Z, A-Z"""
    regex = r"[\u4e00-\u9fa5_a-zA-Z0-9]+"
