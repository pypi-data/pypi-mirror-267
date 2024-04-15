"""
from gllogger import gL

gL.getLogger(__name__)
gL.setGlobalLevel(logging.DEBUG)

gL.init(gL.OT_console)

def gL_function(text):
    print(text)
gL.setFunction(gL_function)
gL.init(gL.OT_function)

gL.setLogDir(os.path.join(os.getcwd(), "log", ))
gL.init(gL.OT_logging)

gL.debugs("a", 1, True, )
gL.infos()
gL.warns()
gL.errors()

# pip install better_exceptions==0.3.3
gL.warns(gL(Exception))

"""

__all__ = ["gL", ]

import logging


class GlobalLogger(logging.Logger):
    OT_console = 0
    OT_function = 1
    OT_logging = 2

    level_map = {
        # 'WARNING': 'WARN',
        # 'WARNING': 'W',
        # 'ERROR': 'E',
        # 'INFO': 'I',
        # 'DEBUG': 'D',
    }

    class FunctionHandler(logging.Handler):
        function = None

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def emit(self, record):  # logging.LogRecord
            if not hasattr(record, "threadNameMe"):
                return GlobalLogger._instance.warns(
                    "NOTE: You should import gllogger before executing any other code.")
            if GlobalLogger.FunctionHandler.function is not None:
                if record.levelname in GlobalLogger.level_map:
                    record.levelname = GlobalLogger.level_map[record.levelname]
                record.asyncTaskName = GlobalLogger.get_asyncio_current_task_name()
                GlobalLogger.FunctionHandler.function(self.format(record))

    @classmethod
    def setFunction(cls, func, ):
        GlobalLogger.FunctionHandler.function = func

    @classmethod
    def setLogDir(cls, dir, ):
        os.makedirs(dir, exist_ok=True)
        GlobalLogger._instance.log_dir_path = dir

    class StreamHandler(logging.StreamHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def emit(self, record):
            if not hasattr(record, "threadNameMe"):
                return GlobalLogger._instance.warns(
                    "NOTE: You should import gllogger before executing any other code.")
            if record.levelname in GlobalLogger.level_map:
                record.levelname = GlobalLogger.level_map[record.levelname]
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
        if len(args) > 0:
            if isinstance(args[0], BaseException):
                return cls._better_exceptions(args[0])
            elif args[0] != "__main__":
                return super().__new__(cls, )
        if not cls._instance:
            cls._instance = super().__new__(cls, )
        return cls._instance

    def __init__(self, *args, **kwargs):
        # print("__init__", args, kwargs)
        if len(args) > 0:
            if isinstance(args[0], BaseException):
                return
            elif args[0] != "__main__":
                super().__init__(*args, **kwargs)
                # self.setLevel(logging.DEBUG)
                return
        if GlobalLogger._instance_init: return
        GlobalLogger._instance_init = True
        super().__init__(*args, **kwargs)
        self.log_dir_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "log", )
        self.output = self.OT_console
        self.log_format = None
        self.log_start_time = None
        self.log_file_path = None
        self.log_file_fp = None
        self.log_handler = None

    def init(self, output):
        if output not in (self.OT_console, self.OT_function, self.OT_logging,):
            raise ValueError(f'parameter "output" cannot be {output}.')
        self.output = output
        self.log_start_time = time.time()
        self.log_file_path = os.path.join(self.log_dir_path, time.strftime("%Y-%m-%d_%H-%M-%S.log", self.utc8()))
        if self.output == self.OT_console:
            self.log_handler = GlobalLogger.StreamHandler(None)
        elif self.output == self.OT_function:
            self.log_handler = GlobalLogger.FunctionHandler()
        elif self.output == self.OT_logging:
            os.makedirs(self.log_dir_path, exist_ok=True)
            self.log_file_fp = open(self.log_file_path, "a", encoding="utf8", buffering=1)
            self.log_handler = GlobalLogger.StreamHandler(self.log_file_fp)

        if self.output in (self.OT_console, self.OT_function,):
            _fmt = "[%(levelname)s %(asctime)s %(fullModule)s[%(lineno)d].%(className)s%(funcName)s%(threadNameMe)s%(asyncTaskName)s] %(message)s"
            _datefmt = "%H:%M:%S"
        else:
            # %(name)s pid:%(process)d %(filename)s %(module)s %(pathname)s %(thread)d %(threadName)s
            _fmt = "[%(levelname)s %(asctime)s %(fullModule)s[%(lineno)d].%(className)s%(funcName)s%(threadNameMe)s%(asyncTaskName)s] %(message)s"
            _datefmt = "%m-%d %H:%M:%S"  # %Y-
        self.log_format = logging.Formatter(_fmt, _datefmt)
        self.log_format.converter = self.utc8  # time.gmtime
        self.log_handler.setFormatter(self.log_format)
        self.set_handler()
        return self

    @staticmethod
    def utc8(*args, **kwargs):
        # (datetime.datetime.utcnow() + datetime.timedelta(hours=8)).timetuple()
        return time.gmtime(time.time() + (8 * 3600))  # gmtime localtime

    def switch(self, ):
        if self.output != self.OT_logging: return
        self.infos(f"""switch log files.""")
        os.makedirs(self.log_dir_path, exist_ok=True)
        self.unset_handler()
        self.log_handler.stream.close()
        self.log_start_time = time.time()
        self.log_file_path = os.path.join(self.log_dir_path, time.strftime("%Y-%m-%d_%H-%M-%S.log", self.utc8()))
        self.log_file_fp = open(self.log_file_path, "a", encoding="utf8", buffering=1)
        self.log_handler = GlobalLogger.StreamHandler(self.log_file_fp)
        self.log_handler.setFormatter(self.log_format)
        self.set_handler()

    @staticmethod
    def check_switch():
        if GlobalLogger._instance.output != GlobalLogger.OT_logging: return
        if time.time() - GlobalLogger._instance.log_start_time >= 60 * 60 * 12:
            GlobalLogger._instance.switch()

    @staticmethod
    def unset_handler():
        # GlobalLogger._instance.removeHandler(GlobalLogger._instance.log_handler)
        logging.getLogger().removeHandler(GlobalLogger._instance.log_handler)
        # for logger_name in logging.Logger.manager.loggerDict:
        #     logging.getLogger(logger_name).removeHandler(GlobalLogger._instance.log_handler)

    @staticmethod
    def set_handler():
        # GlobalLogger._instance.addHandler(GlobalLogger._instance.log_handler)
        logging.getLogger().addHandler(GlobalLogger._instance.log_handler)
        # logging.getLogger("abc").addHandler(self.log_handler)
        # logging.basicConfig(level=logging.DEBUG, handlers=[self.log_handler, ])
        # for logger_name in logging.Logger.manager.loggerDict:
        #     print(logging.getLogger(logger_name), )
        #     logging.getLogger(logger_name).addHandler(GlobalLogger._instance.log_handler)

    """====================================="""

    def debug(self, *args, **kwargs):
        if "extra" not in kwargs or kwargs["extra"] is None or "threadNameMe" not in kwargs["extra"]:
            # print("debug", args, kwargs)
            caller_frame = inspect.currentframe().f_back
            _fullModule = inspect.getmodule(caller_frame).__name__
            if "stacklevel" not in kwargs or kwargs["stacklevel"] is None: kwargs["stacklevel"] = 2
            if "extra" not in kwargs or kwargs["extra"] is None: kwargs["extra"] = {}
            if isinstance(kwargs["extra"], dict):
                kwargs["extra"].update({
                    "fullModule": "main" if _fullModule == "__main__" else _fullModule,
                    "className": GlobalLogger.get_class_name(caller_frame),
                    "threadNameMe": "" if threading.currentThread() == threading.main_thread() else " " + threading.current_thread().getName(),
                })
        return super().debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        if "extra" not in kwargs or kwargs["extra"] is None or "threadNameMe" not in kwargs["extra"]:
            # print("info", args, kwargs)
            caller_frame = inspect.currentframe().f_back
            _fullModule = inspect.getmodule(caller_frame).__name__
            if "stacklevel" not in kwargs or kwargs["stacklevel"] is None: kwargs["stacklevel"] = 2
            if "extra" not in kwargs or kwargs["extra"] is None: kwargs["extra"] = {}
            if isinstance(kwargs["extra"], dict):
                kwargs["extra"].update({
                    "fullModule": "main" if _fullModule == "__main__" else _fullModule,
                    "className": GlobalLogger.get_class_name(caller_frame),
                    "threadNameMe": "" if threading.currentThread() == threading.main_thread() else " " + threading.current_thread().getName(),
                })
        _result = super().info(*args, **kwargs)
        GlobalLogger._instance.log_handler.flush()
        return _result

    def warn(self, *args, **kwargs):
        if "extra" not in kwargs or kwargs["extra"] is None or "threadNameMe" not in kwargs["extra"]:
            # print("warn", args, kwargs)
            caller_frame = inspect.currentframe().f_back
            _fullModule = inspect.getmodule(caller_frame).__name__
            if "stacklevel" not in kwargs or kwargs["stacklevel"] is None: kwargs["stacklevel"] = 2
            if "extra" not in kwargs or kwargs["extra"] is None: kwargs["extra"] = {}
            if isinstance(kwargs["extra"], dict):
                kwargs["extra"].update({
                    "fullModule": "main" if _fullModule == "__main__" else _fullModule,
                    "className": GlobalLogger.get_class_name(caller_frame),
                    "threadNameMe": "" if threading.currentThread() == threading.main_thread() else " " + threading.current_thread().getName(),
                })
        _result = super().warning(*args, **kwargs)
        GlobalLogger._instance.log_handler.flush()
        return _result

    def warning(self, *args, **kwargs):
        if "extra" not in kwargs or kwargs["extra"] is None or "threadNameMe" not in kwargs["extra"]:
            # print("warning", args, kwargs)
            caller_frame = inspect.currentframe().f_back
            _fullModule = inspect.getmodule(caller_frame).__name__
            if "stacklevel" not in kwargs or kwargs["stacklevel"] is None: kwargs["stacklevel"] = 2
            if "extra" not in kwargs or kwargs["extra"] is None: kwargs["extra"] = {}
            if isinstance(kwargs["extra"], dict):
                kwargs["extra"].update({
                    "fullModule": "main" if _fullModule == "__main__" else _fullModule,
                    "className": GlobalLogger.get_class_name(caller_frame),
                    "threadNameMe": "" if threading.currentThread() == threading.main_thread() else " " + threading.current_thread().getName(),
                })
        _result = super().warning(*args, **kwargs)
        GlobalLogger._instance.log_handler.flush()
        return _result

    def error(self, *args, **kwargs):
        if "extra" not in kwargs or kwargs["extra"] is None or "threadNameMe" not in kwargs["extra"]:
            # print("error", args, kwargs)
            caller_frame = inspect.currentframe().f_back
            _fullModule = inspect.getmodule(caller_frame).__name__
            if "stacklevel" not in kwargs or kwargs["stacklevel"] is None: kwargs["stacklevel"] = 2
            if "extra" not in kwargs or kwargs["extra"] is None: kwargs["extra"] = {}
            if isinstance(kwargs["extra"], dict):
                kwargs["extra"].update({
                    "fullModule": "main" if _fullModule == "__main__" else _fullModule,
                    "className": GlobalLogger.get_class_name(caller_frame),
                    "threadNameMe": "" if threading.currentThread() == threading.main_thread() else " " + threading.current_thread().getName(),
                })
        _result = super().error(*args, **kwargs)
        GlobalLogger._instance.log_handler.flush()
        return _result

    def exception(self, *args, **kwargs):
        if "extra" not in kwargs or kwargs["extra"] is None or "threadNameMe" not in kwargs["extra"]:
            # print("exception", args, kwargs)
            caller_frame = inspect.currentframe().f_back
            _fullModule = inspect.getmodule(caller_frame).__name__
            if "stacklevel" not in kwargs or kwargs["stacklevel"] is None: kwargs["stacklevel"] = 4
            if "extra" not in kwargs or kwargs["extra"] is None: kwargs["extra"] = {}
            if isinstance(kwargs["extra"], dict):
                kwargs["extra"].update({
                    "fullModule": "main" if _fullModule == "__main__" else _fullModule,
                    "className": GlobalLogger.get_class_name(caller_frame),
                    "threadNameMe": "" if threading.currentThread() == threading.main_thread() else " " + threading.current_thread().getName(),
                })
        _result = super().exception(*args, **kwargs)
        GlobalLogger._instance.log_handler.flush()
        return _result

    """====================================="""

    @staticmethod
    def debugs(*args, sep=" "):
        caller_frame = inspect.currentframe().f_back
        _fullModule = inspect.getmodule(caller_frame).__name__
        return GlobalLogger._instance.debug(sep.join((str(i) for i in args)), stacklevel=3, extra={
            "fullModule": "main" if _fullModule == "__main__" else _fullModule,
            "className": GlobalLogger.get_class_name(caller_frame),
            "threadNameMe": "" if threading.currentThread() == threading.main_thread() else " " + threading.current_thread().getName(),
        })

    @staticmethod
    def infos(*args, sep=" "):
        caller_frame = inspect.currentframe().f_back
        _fullModule = inspect.getmodule(caller_frame).__name__
        return GlobalLogger._instance.info(sep.join((str(i) for i in args)), stacklevel=3, extra={
            "fullModule": "main" if _fullModule == "__main__" else _fullModule,
            "className": GlobalLogger.get_class_name(caller_frame),
            "threadNameMe": "" if threading.currentThread() == threading.main_thread() else " " + threading.current_thread().getName(),
        })

    @staticmethod
    def warns(*args, sep=" "):
        caller_frame = inspect.currentframe().f_back
        _fullModule = inspect.getmodule(caller_frame).__name__
        return GlobalLogger._instance.warning(sep.join((str(i) for i in args)), stacklevel=3, extra={
            "fullModule": "main" if _fullModule == "__main__" else _fullModule,
            "className": GlobalLogger.get_class_name(caller_frame),
            "threadNameMe": "" if threading.currentThread() == threading.main_thread() else " " + threading.current_thread().getName(),
        })

    @staticmethod
    def errors(*args, sep=" "):
        caller_frame = inspect.currentframe().f_back
        _fullModule = inspect.getmodule(caller_frame).__name__
        return GlobalLogger._instance.error(sep.join((str(i) for i in args)), stacklevel=3, extra={
            "fullModule": "main" if _fullModule == "__main__" else _fullModule,
            "className": GlobalLogger.get_class_name(caller_frame),
            "threadNameMe": "" if threading.currentThread() == threading.main_thread() else " " + threading.current_thread().getName(),
        })

    """====================================="""

    @staticmethod
    def getLogger(name):
        return logging.getLogger(name)

    @staticmethod
    def setGlobalLevel(level):
        return logging.getLogger().setLevel(level)

    @staticmethod
    def setLoggerClass():
        logging.setLoggerClass(GlobalLogger)
        logging.setLoggerClass = lambda *args, **kwargs: GlobalLogger._instance.warns(args, kwargs)
        return

    @staticmethod
    def loggers():
        # [print(i) for i in gL.loggers()]
        for logger_name in logging.Logger.manager.loggerDict:
            yield logging.getLogger(logger_name)

    """====================================="""

    @staticmethod
    def _better_exceptions(e):
        try:
            import better_exceptions
        except ImportError:
            import traceback
            return "".join(traceback.TracebackException.from_exception(e).format())
        else:
            _name = "_gllogger_SUPPORTS_COLOR"
            if not hasattr(better_exceptions, _name):
                setattr(better_exceptions, _name, better_exceptions.SUPPORTS_COLOR)
            if getattr(better_exceptions, _name):
                better_exceptions.SUPPORTS_COLOR = GlobalLogger._instance.output == GlobalLogger.OT_console
            # better_exceptions.MAX_LENGTH = None
            better_exceptions.encoding.ENCODING = 'utf-8'
            return "".join(better_exceptions.format_exception(type(e), e, e.__traceback__))

    @staticmethod
    def color(text):
        _ = re.search(_re1__color, text)
        head, text = _.group(1), _.group(2)
        _gn, _br, _space = "\n", "<br />", "&nbsp;"
        level = re.search(_re2__color, head).group(1)
        if level in ("WARNING", "ERROR",
                     GlobalLogger.level_map.get("WARNING", "W"), GlobalLogger.level_map.get("ERROR", "E"),):
            c = "#FF0000"
            _text, _ts = [], text.split("\n")
            for _i, i in enumerate(_ts):
                # if _i == len(_ts) - 1 and len(i) == 0: continue
                _text.append(f"{html.escape(i)}" if len(_text) == 0 else
                             f'<p style="color:{c};margin: 0;padding: 0;">{html.escape(i).replace(" ", _space)}</p>')
            return f'<p style="color:{c};margin: 0;padding: 0;">{html.escape(head)}{_text[0]}</p>{"".join(_text[1:])}'
        else:
            c = "#0000FF"
            _text, _ts = [], text.split("\n")
            for _i, i in enumerate(_ts):
                # if _i == len(_ts) - 1 and len(i) == 0: continue
                _text.append(f"{html.escape(i)}" if len(_text) == 0 else
                             f'<p style="margin: 0;padding: 0;">{html.escape(i).replace(" ", _space)}</p>')
            return f'<p style="color:{c};margin: 0;padding: 0;">{html.escape(head)}<span style="color:inherit;">{_text[0]}</span></p>{"".join(_text[1:])}'


gL = GlobalLogger
gL.setLoggerClass()
gL.setGlobalLevel(logging.DEBUG)
import os, sys, time, inspect, asyncio, threading, re, html

_re1__color = re.compile(r"^(\[.+?])(\s[\s\S]+)$")
_re2__color = re.compile(r"^\[(\w+)")
