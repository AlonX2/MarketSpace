class MicroserviceClientException(Exception):
    """A generic exception for `MicroserviceClient`.
    """
    pass

class MicroserviceClientFailedRabbitConnection(MicroserviceClientException):
    """Raised in case the connection to the RabbitMQ server fails.
    """
    pass

class MicroserviceFailed(MicroserviceClientException):
    """Raised in the case the called microservice internally fails with the data provided to it.
    """
    pass