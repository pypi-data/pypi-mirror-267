from loguru import logger


def setup(file_name,
          rotation="1 days",
          retention="30 days",
          serialize=True,
          backtrace=True,
          diagnose=False,
          filter=lambda record: True,
          level='INFO'):
    """
    初始化安装loguru日志配置
    使用方式:
        from loguru import logger

        logger.info('info message')
        logger.error('error message')
    :param file_name: 文件名称
    :param rotation: 日志滚动周期, 允许值示例如下:
        logger.add("file_1.log", rotation="500 MB")    # Automatically rotate too big file
        logger.add("file_2.log", rotation="12:00")     # New file is created each day at noon
        logger.add("file_3.log", rotation="1 week")    # Once the file is too old, it's rotated
        logger.add("file_X.log", retention="10 days")  # Cleanup after some time
        logger.add("file_Y.log", compression="zip")    # Save some loved space
    :param retention: 日志文件保留周期, 默认30天
    :param serialize: 是否将写入文件的数据序列化为json, 默认True. 推荐: True
    :param backtrace: 是否默认在异常时自动打印堆栈信息, 默认True. 推荐: True
    :param diagnose: 是否开启代码异常诊断, 可层层递进追踪异常链路, 生产环境建议关闭, 开发环境建议开启, 默认False
    :param filter: 日志文件的过滤条件, 符合条件的日志记录将写入该文件
    :param level: 日志级别, 只有超过该级别的日志会记入文件, 支持以下日志级别
        TRACE: 最低级别，用于追踪程序的详细执行流程，通常用于诊断问题
        DEBUG: 用于调试目的的详细信息，例如变量值或者函数调用
        INFO: 提供程序执行中的一般信息，用于表示程序正常运行
        SUCCESS: 表示成功的操作
        WARNING: 表示潜在的问题或者不符合预期的情况，但程序仍能继续执行
        ERROR: 表示错误，但程序仍然可以继续执行
        CRITICAL: 表示严重错误，可能导致程序无法继续执行
    """
    # 添加文件配置
    logger.add(file_name,
               format="{message}",
               backtrace=backtrace,
               diagnose=diagnose,
               serialize=serialize,
               rotation=rotation,
               retention=retention,
               filter=filter,
               level=level)


def get_loguru_adapter_logging_formatter():
    """
    获取适配loguru serialize格式的logging.Formatter类型
    Returns:
        返回logging.Formatter类
    """
    import logging
    import time
    import traceback
    import datetime
    import json

    class LoguruSerializeAdapterFormatter(logging.Formatter):
        def format(self, record):
            elapsed_seconds = time.time() - record.created
            elapsed_repr = self._format_elapsed(elapsed_seconds)
            exception_msg = traceback.format_exc() if record.exc_info else ''
            log_record = {
                "text": record.getMessage() + f"\n{exception_msg}",
                "record": {
                    "elapsed": {
                        "repr": elapsed_repr,
                        "seconds": elapsed_seconds
                    },
                    "exception": self._format_exception(record.exc_info),
                    "extra": {},
                    "file": {
                        "name": record.filename,
                        "path": record.pathname
                    },
                    "function": record.funcName,
                    "level": {
                        "icon": self._get_level_icon(record.levelname),
                        "name": record.levelname,
                        "no": record.levelno
                    },
                    "line": record.lineno,
                    "message": record.getMessage(),
                    "module": record.module,
                    "name": record.name,
                    "process": {
                        "id": record.process,
                        "name": record.processName
                    },
                    "thread": {
                        "id": record.thread,
                        "name": record.threadName
                    },
                    "time": {
                        "repr": datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S.%f%z'),
                        "timestamp": record.created
                    }
                }
            }
            return json.dumps(log_record)

        @staticmethod
        def _get_level_icon(level_name: str):
            if level_name == 'TRACE':
                return '✏️'
            if level_name == 'DEBUG':
                return '🐞'
            elif level_name == 'INFO':
                return 'ℹ️'
            elif level_name == 'WARNING':
                return '⚠️'
            elif level_name == 'ERROR':
                return '❌'
            elif level_name == 'CRITICAL':
                return '☠️'
            return ''

        @staticmethod
        def _format_elapsed(elapsed_seconds):
            hours, remainder = divmod(elapsed_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return "{:0>2}:{:0>2}:{:0>2}.{:06}".format(int(hours), int(minutes), int(seconds),
                                                       int((elapsed_seconds - int(elapsed_seconds)) * 1000000))

        @staticmethod
        def _format_exception(exc_info):
            if exc_info:
                exc_type, exc_value, exc_traceback = exc_info
                return {
                    "type": exc_type.__name__,
                    "message": str(exc_value),
                    "traceback": True
                }
            else:
                return None

    return LoguruSerializeAdapterFormatter


class PrefixLogger:
    """
    前缀日志工具, 所有日志内容都将带上[prefix]前缀
    """

    def __init__(self, prefix='', _logger=None):
        self._prefix = prefix
        if _logger:
            self._logger = _logger
        else:
            self._logger = logger

    def trace(self, __message, *args, **kwargs):
        return self.log("TRACE", __message, *args, **kwargs)

    def debug(self, __message, *args, **kwargs):
        return self.log("DEBUG", __message, *args, **kwargs)

    def info(self, __message, *args, **kwargs):
        return self.log("INFO", __message, *args, **kwargs)

    def warning(self, __message, *args, **kwargs):
        return self.log("WARNING", __message, *args, **kwargs)

    def error(self, __message, *args, **kwargs):
        return self.log("ERROR", __message, *args, **kwargs)

    def success(self, __message, *args, **kwargs):
        return self.log("SUCCESS", __message, *args, **kwargs)

    def critical(self, __message, *args, **kwargs):
        return self.log("CRITICAL", __message, *args, **kwargs)

    def exception(self, __message, *args, **kwargs):
        if self._prefix:
            return self._logger.exception(f"[{self._prefix}]{__message}", *args, **kwargs)
        return self._logger.exception(__message, *args, **kwargs)

    def log(self, __level, __message, *args, **kwargs):
        if self._prefix:
            return self._logger.log(__level, f"[{self._prefix}]{__message}", *args, **kwargs)
        return self._logger.log(__level, __message, *args, **kwargs)
