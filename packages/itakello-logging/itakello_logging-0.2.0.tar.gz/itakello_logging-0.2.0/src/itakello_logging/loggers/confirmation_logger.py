import logging


class ConfirmationLogger(logging.Logger):
    CONFIRMATION_LEVEL = 25

    def __init__(self, name, level=logging.NOTSET) -> None:
        super().__init__(name, level)
        logging.addLevelName(self.CONFIRMATION_LEVEL, "CONFIRMATION")

    def confirmation(self, message, *args, **kwargs) -> None:
        if self.isEnabledFor(self.CONFIRMATION_LEVEL):
            self._log(self.CONFIRMATION_LEVEL, message, args, **kwargs)
