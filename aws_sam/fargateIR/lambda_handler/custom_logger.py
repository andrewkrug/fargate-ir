from pythonjsonlogger import jsonlogger
import datetime


class JsonFormatter(jsonlogger.JsonFormatter, object):
    def __init__(
        self,
        fmt="%(asctime) %(name) %(processName) %(filename) \
        %(funcName) %(levelname) %(lineno) %(module) %(threadName) %(message)",
        datefmt="%Y-%m-%dT%H:%M:%SZ%z",
        style="%",
        extra={},
        *args,
        **kwargs
    ):
        self._extra = extra
        jsonlogger.JsonFormatter.__init__(
            self, fmt=fmt, datefmt=datefmt, *args, **kwargs
        )

    def process_log_record(self, log_record):
        if "asctime" in log_record:
            log_record["timestamp"] = log_record["asctime"]
        else:
            log_record["timestamp"] = datetime.datetime.utcnow().strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ%z"
            )

        if self._extra is not None:
            for key, value in self._extra.items():
                log_record[key] = value
        return super(JsonFormatter, self).process_log_record(log_record)
