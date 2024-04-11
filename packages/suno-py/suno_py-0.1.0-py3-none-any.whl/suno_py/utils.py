import json
import time
import datetime
import random


def dict_to_pretty_string_py(the_dict):
    if not the_dict:
        return "{}"
    return json.dumps(the_dict, sort_keys=True, indent=4, separators=(',', ': '))


def random_sleep(start=1, end=3, debug=True, info=''):
    """
    随机延迟，因为如果你访问了很多页面，你的 ip 可能会被封。
    """
    sleep_time = random.randint(start, end)
    if debug:
        print(f'{info}随机延迟：{sleep_time} 秒......')
    time.sleep(sleep_time)


def get_now(fmt="%Y-%m-%d %H:%M:%S"):
    """
    获取当前日期和时间
    :return: 格式 2018-11-28 15:03:08
    """
    return datetime.datetime.now().strftime(fmt)


def second_to_time_str(seconds):
    """
    秒转换为人类阅读的时间显示，用来显示已用时间
    例如：'1小时1分1.099秒'
    """
    time_str = ''
    hour = '%01d小时' % (seconds / 3600)
    minute = '%01d分' % ((seconds % 3600) / 60)

    if hour != '0小时':
        time_str += hour

    if minute != '0分':
        time_str += minute

    # seconds
    time_str += '%01d.%03d秒' % (seconds % 60, (seconds % 1) * 1000)

    return time_str


class Timer:
    """
    计时器，可以当装饰器或者用 with 来对代码计时

    # 例子：
        >>> import time
        >>> def papapa(t):
        >>>     time.sleep(t)
        >>> with Timer() as timer:
        >>>     papapa(1)
        运行时间 1.000 秒
        >>> @Timer.time_it
        >>> def papapa(t):
        >>>     time.sleep(t)
        >>> papapa(1)
        papapa 运行时间 1.001 秒
    """

    def __init__(self, name=None):
        self.start = time.time()

        # 我们添加一个自定义的计时名称
        if isinstance(name, str):
            self.name = name + ' '
        else:
            self.name = ''

        print(f'{get_now()} 开始运行 {self.name}', )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running_time()
        return exc_type is None

    @staticmethod
    def time_it(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            print(f'{get_now()} 开始运行 {func.__name__}', )
            result = func(*args, **kwargs)
            print(f'{get_now()} 结束运行 {func.__name__}，运行时间 {second_to_time_str(time.time() - start)}', )
            return result

        return wrapper

    def running_time(self):
        stop = time.time()
        cost = stop - self.start
        print(f'{get_now()} 结束运行 {self.name}，运行时间 {second_to_time_str(cost)}', )
