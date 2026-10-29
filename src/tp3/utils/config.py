import logging
import sys

import src.config  # noqa: F401  (configure le logging racine)

logger = logging.getLogger("TP3")


class _StdoutHandler(logging.Handler):
    def emit(self, record):
        sys.stdout.write(self.format(record) + "\n")


output_logger = logging.getLogger("TP3.output")
output_logger.propagate = False
_handler = _StdoutHandler()
_handler.setFormatter(logging.Formatter("%(message)s"))
output_logger.addHandler(_handler)
output_logger.setLevel(logging.INFO)
