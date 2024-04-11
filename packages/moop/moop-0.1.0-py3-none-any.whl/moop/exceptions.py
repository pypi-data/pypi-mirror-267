"""exception module for moop."""

class MoopException(Exception):
    """Base notifier exception. Catch this to catch all of :mod:`notifiers` errors"""

    def __init__(self, *args, **kwargs):
        """
        Looks for ``provider``, ``message`` and ``data`` in kwargs
        :param args: Exception arguments
        :param kwargs: Exception kwargs
        """
        self.provider = kwargs.get('provider')
        self.response = kwargs.get('response')

        self.message = kwargs.get('message')
        self.data = kwargs.get('data')

        super().__init__(self.message)

    def __repr__(self):
        return f'<MoopError: {self.message}>'


class MoopValidationException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
