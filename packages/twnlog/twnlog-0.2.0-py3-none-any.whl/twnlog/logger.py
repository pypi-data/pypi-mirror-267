"""
loguru 封装类，导入即可直接使用
# 当前文件名 twnlog.py
"""

from functools import wraps
import sys
import datetime
import loguru
from pathlib import Path
import configparser

# 单例类的装饰器
def singleton_class_decorator(cls):
    """
    装饰器，单例类的装饰器
    """
    # 在装饰器里定义一个字典，用来存放类的实例。
    _instance = {}

    # 装饰器，被装饰的类
    @wraps(cls)
    def wrapper_class(*args, **kwargs):
        # 判断，类实例不在类实例的字典里，就重新创建类实例
        if cls not in _instance:
            # 将新创建的类实例，存入到实例字典中
            _instance[cls] = cls(*args, **kwargs)
        # 如果实例字典中，存在类实例，直接取出返回类实例
        return _instance[cls]

    # 返回，装饰器中，被装饰的类函数
    return wrapper_class


@singleton_class_decorator
class Logger:
    def __init__(self):
        self._logger = None
        self.logger_add()

    def read_ini(self):
        # print(Path(Path(__file__).parent, 'log.ini'))
        config = configparser.ConfigParser(inline_comment_prefixes=('#', ';')) # 添加可以读取行内注释的参数
        config.read(Path(Path(__file__).parent, 'log.ini'), encoding="UTF-8")

        return config

    def get_project_path(self, project_path=None):
        if project_path is None:
            # 当前项目文件的，绝对真实路径
            # 路径，一个点代表当前目录，两个点代表当前目录的上级目录
            project_path = Path(__file__).parent.parent
        # 返回当前项目路径
        return project_path

    def get_log_path(self, path):
        # 项目目录
        project_path = self.get_project_path()
        # 项目日志目录
        project_log_dir = Path(path, 'Logs')
        # 日志文件名
        project_log_filename = '{}.log'.format(datetime.date.today())
        # 日志文件路径
        project_log_path = Path(project_log_dir, project_log_filename)

        # 确保日志目录存在
        if not project_log_dir.exists():
            project_log_dir.mkdir(parents=True, exist_ok=True)

        # 确保日志文件存在（如果不存在，则创建一个空文件）
        if not project_log_path.exists():
            project_log_path.touch()

        return project_log_path

    def logger_add(self):
        # 清空所有设置
        loguru.logger.remove()  # 清空所有设置

        # 读取配置
        config = self.read_ini()
        self._logger = loguru.logger
        # 控制台输出
        if config.get('StderrLog', 'is_open').lower() == "on":
            self._logger.add(
                # 控制台打印
                sys.stderr,
                format="[<green>{time:YYYY-MM-DD HH:mm:ss}</green> {level:<8}| "  # 颜色>时间
                                   "{process.name} | "  # 进程名
                                   "{thread.name} | "  # 进程名
                                "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
                                ":<cyan>{line}</cyan> | "  # 行号
                                "<level>{message}</level>",  # 日志内容
                level=config.get('StderrLog', 'level'),
                backtrace=True,
                diagnose=True
            )

        # 文件保存
        if config.get('FileLog', 'is_open').lower() == "on":
            project_log_path= self.get_log_path(config.get("FileLog", 'path'))
            # print(project_log_path)
            # 返回日志路径
            self._logger.add(
                # 保存的路径
                sink=project_log_path,
                # 日志创建周期
                rotation=config.get('FileLog', 'rotation'),
                # 保存
                retention=config.get('FileLog', 'retention'),
                # 文件的压缩格式
                compression='zip',
                # 编码格式
                encoding="utf-8",
                # 支持异步存储
                enqueue=True,
				# 输出格式
                format="[{time:YYYY-MM-DD HH:mm:ss} {level:<8} | {file}:{module}.{function}:{line}]  {message}",
                level=config.get('FileLog', 'level'),
                backtrace=True,
                diagnose=True
            )

    @property
    def get_logger(self):
        return self._logger


'''
# 实例化日志类
'''
logger = Logger().get_logger


if __name__ == '__main__':
    logger.debug('调试代码')
    logger.info('输出信息')
    logger.success('输出成功')
    logger.warning('错误警告')
    logger.error('代码错误')
    logger.critical('崩溃输出')
    logger.exception('log 异常')

    """
    在其他.py文件中，只需要直接导入已经实化的logger类即可
    例如导入访视如下：例
    from project.twnlog import twnlog
    然后直接使用logger即可
    """
    # twnlog.info('----原始测试----')


