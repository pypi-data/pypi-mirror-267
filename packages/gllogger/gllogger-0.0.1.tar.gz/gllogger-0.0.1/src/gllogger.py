import asyncio
import datetime
import inspect
import logging
import threading
import time
import os


class GlobalLogger(logging.Logger):
    class FunctionHandler(logging.Handler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def emit(self, record):  # logging.LogRecord
            record.asyncTaskName = GlobalLogger.get_asyncio_current_task_name()
            GlobalLogger.FunctionHandler.func(self.format(record))

        @staticmethod
        def func(msg):
            print(msg)

    class StreamHandler(logging.StreamHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def emit(self, record):
            record.asyncTaskName = GlobalLogger.get_asyncio_current_task_name()
            return super().emit(record)

    @staticmethod
    def get_asyncio_current_task():
        try:
            _asyncio_current_task = asyncio.current_task()
        except Exception:
            _asyncio_current_task = None
        return _asyncio_current_task

    @staticmethod
    def get_asyncio_current_task_name():
        _asyncio_current_task = GlobalLogger.get_asyncio_current_task()
        return " " + _asyncio_current_task.get_name() if _asyncio_current_task else ""

    @staticmethod
    def get_class_name(caller_frame):
        _args = caller_frame.f_code.co_varnames
        _class_name = ""
        if len(_args) > 0:
            _args1 = _args[0]
            if _args1 in ("cls", "self",):
                _class = caller_frame.f_locals.get(_args1, None)
                if _class:
                    if isinstance(_class, type):
                        _class_name = _class.__name__ + "::"
                    else:
                        _class_name = type(_class).__name__ + "::"
        return _class_name

    _instance = None
    _instance_init = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, )
        return cls._instance

    def __init__(self, *args, **kwargs):
        if GlobalLogger._instance_init: return
        GlobalLogger._instance_init = True
        super().__init__(*args, **kwargs)
        self.setLevel(logging.DEBUG)
        self.log_dir_path = os.path.join(os.path.dirname(__file__), "log", )
        self.output = "debug"
        self.log_format = None
        self.log_start_time = None
        self.log_file_path = None
        self.log_file_fp = None
        self.log_handler = None

    def init(self, output):
        '''
        :param output: ("debug", "function", "logging",)
        :return: None
        '''
        if output in ("debug", "function", "logging",):
            self.output = output
        self.log_start_time = time.time()
        self.log_file_path = os.path.join(self.log_dir_path, time.strftime("%Y-%m-%d_%H-%M-%S.log", self.utc8()))
        if self.output == "debug":
            self.log_handler = GlobalLogger.StreamHandler(None)
        elif self.output == "function":
            self.log_handler = GlobalLogger.FunctionHandler()
        elif self.output == "logging":
            os.makedirs(self.log_dir_path, exist_ok=True)
            self.log_file_fp = open(self.log_file_path, "a", encoding="utf8", buffering=1)
            self.log_handler = GlobalLogger.StreamHandler(self.log_file_fp)

        if self.output in ("debug", "function",):
            _fmt = "[%(levelname)s %(asctime)s %(fullModule)s[%(lineno)d].%(className)s%(funcName)s%(threadNameMe)s%(asyncTaskName)s] %(message)s"
            _datefmt = "%H:%M:%S"
        else:
            # %(name)s pid:%(process)d %(filename)s %(module)s %(pathname)s %(thread)d %(threadName)s
            _fmt = "[%(levelname)s %(asctime)s %(fullModule)s[%(lineno)d].%(className)s%(funcName)s%(threadNameMe)s%(asyncTaskName)s] %(message)s"
            _datefmt = "%m-%d %H:%M:%S"  # %Y-
        self.log_format = logging.Formatter(_fmt, _datefmt)
        self.log_format.converter = self.utc8  # time.gmtime
        self.log_handler.setFormatter(self.log_format)

        self.addHandler(self.log_handler)
        return self

    @staticmethod
    def utc8(*args, **kwargs):
        return (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).timetuple()

    def switch(self, ):
        if self.output != "logging": return
        self.infos(f"""切换日志文件。""")
        os.makedirs(self.log_dir_path, exist_ok=True)
        self.removeHandler(self.log_handler)
        self.log_handler.stream.close()
        self.log_start_time = time.time()
        self.log_file_path = os.path.join(self.log_dir_path, time.strftime("%Y-%m-%d_%H-%M-%S.log", self.utc8()))
        self.log_file_fp = open(self.log_file_path, "a", encoding="utf8", buffering=1)
        self.log_handler = GlobalLogger.StreamHandler(self.log_file_fp)
        self.log_handler.setFormatter(self.log_format)
        self.addHandler(self.log_handler)

    @staticmethod
    def check_switch():
        if GlobalLogger._instance.output != "logging": return
        if time.time() - GlobalLogger._instance.log_start_time >= 60 * 60 * 12:
            GlobalLogger._instance.switch()

    @staticmethod
    def infos(*args, sep=" "):
        caller_frame = inspect.currentframe().f_back
        _fullModule = inspect.getmodule(caller_frame).__name__
        GlobalLogger._instance.info(sep.join((str(i) for i in args)), stacklevel=2, extra={
            "fullModule": "main" if _fullModule == "__main__" else _fullModule,
            "className": GlobalLogger.get_class_name(caller_frame),
            "threadNameMe": "" if threading.currentThread() == threading.main_thread() else " " + threading.current_thread().getName(),
        })
        GlobalLogger._instance.log_handler.flush()

    @staticmethod
    def warns(*args, sep=" "):
        caller_frame = inspect.currentframe().f_back
        _fullModule = inspect.getmodule(caller_frame).__name__
        GlobalLogger._instance.warning(sep.join((str(i) for i in args)), stacklevel=2, extra={
            "fullModule": "main" if _fullModule == "__main__" else _fullModule,
            "className": GlobalLogger.get_class_name(caller_frame),
            "threadNameMe": "" if threading.currentThread() == threading.main_thread() else " " + threading.current_thread().getName(),
        })
        GlobalLogger._instance.log_handler.flush()
