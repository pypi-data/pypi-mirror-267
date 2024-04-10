import datetime
from abc import ABC, abstractmethod
from typing import Any
from loguru import logger


class PrefixLogger:
    """
    添加了日志前缀功能
    """

    def __init__(self, prefix=''):
        self._prefix = prefix
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


class Task(ABC):
    """
    任务抽象类封装, 建议任务类业务统一继承该类
    """

    def __init__(self):
        self._logger = PrefixLogger(self._task_name())

    def run(self, *args, **kwargs) -> Any:
        """
        任务执行方法
        """
        now = datetime.datetime.now()
        self._logger.info('开始处理, 任务参数: args: {}, kwargs: {}', self._task_name(), args, kwargs)
        try:
            ans = self._run(*args, **kwargs)
            self._logger.info('处理完成, 本次任务执行耗时: {}, 返回值: {}, 任务参数: args: {}, kwargs: {}',
                              self._task_name(), (datetime.datetime.now() - now).total_seconds(), ans, args, kwargs)
            return ans
        except Exception as e:
            self._logger.error('出错, 本次任务执行耗时: {}, 任务参数: args: {}, kwargs: {}',
                               self._task_name(), (datetime.datetime.now() - now).total_seconds(), args, kwargs)
            raise e

    @abstractmethod
    def _run(self, *args, **kwargs) -> Any:
        """
        任务逻辑, 子类实现该方法来实现任务逻辑
        Args:
            args: 任务参数
            kwargs: 任务参数
        """
        raise NotImplemented('任务逻辑未实现')

    @abstractmethod
    def _task_name(self) -> str:
        """
        任务名称, 子类必须实现该方法
        Returns:
            任务名称
        """
        raise NotImplemented('任务名称未实现')


class AsyncTask(ABC):
    """
    async任务抽象类封装, 建议任务类业务统一继承该类
    """

    def __init__(self):
        self._logger = PrefixLogger(self._task_name())

    @abstractmethod
    def _task_name(self) -> str:
        """
        任务名称, 子类必须实现该方法
        Returns:
            任务名称
        """
        raise NotImplemented('任务名称未实现')

    async def run(self, *args, **kwargs) -> Any:
        """
        任务执行方法
        """
        now = datetime.datetime.now()
        self._logger.info('开始处理, 任务参数: args: {}, kwargs: {}', self._task_name(), args, kwargs)
        try:
            ans = await self._run(*args, **kwargs)
            self._logger.info('处理完成, 本次任务执行耗时: {}, 返回值: {}, 任务参数: args: {}, kwargs: {}',
                              self._task_name(), (datetime.datetime.now() - now).total_seconds(), ans, args, kwargs)
            return ans
        except Exception as e:
            self._logger.error('出错, 本次任务执行耗时: {}, 任务参数: args: {}, kwargs: {}',
                               self._task_name(), (datetime.datetime.now() - now).total_seconds(), args, kwargs)
            raise e

    @abstractmethod
    async def _run(self, *args, **kwargs) -> Any:
        """
        任务逻辑, 子类实现该方法来实现任务逻辑
        Args:
            args: 任务参数
            kwargs: 任务参数
        """
        raise NotImplemented('任务逻辑未实现')
