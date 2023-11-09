from rest_framework.exceptions import APIException


class MoreThanOneCommentNotAllowed(APIException):
    status_code = 400
    default_detail = 'Each user can write only one comment for an advertisement'
