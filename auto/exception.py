import json


class TestCaseNotException(Exception):
    pass


class ParameterBuildFailedException(Exception):
    pass


class ResponseErr(Exception):
    pass


class ReturnFormatException(Exception):
    pass


class CaseFailException(Exception):
    pass
