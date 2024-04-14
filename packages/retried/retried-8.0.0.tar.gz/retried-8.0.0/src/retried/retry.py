from functools import partial
from functools import wraps
from itertools import cycle
from itertools import repeat
from itertools import tee
import logging
import time
import typing as t

from .utils import relative_to_cwd


# try:
#     from typing import ParamSpec
# except ImportError:
#     from typing_extensions import ParamSpec  # type: ignore[assignment]
# P = ParamSpec('P')  # https://docs.python.org/zh-tw/3/library/typing.html#typing.ParamSpec
# R = t.TypeVar('R')
FuncT = t.Callable  # [P, R]


logger = logging.getLogger(__package__)


_T = t.TypeVar('_T')
SingleOrTuple = t.Union[_T, tuple[_T, ...]]
SingleOrIterable = t.Union[_T, t.Iterable[_T]]


SleepT = t.Callable[[float], None]
DelayT = float
RetriesT = t.Optional[int]
LogfT = t.Callable[[t.Any], None]


class DummyLogger(logging.Logger):
    def __init__(self, logf: LogfT):
        self._logf = logf
        super().__init__(__package__ or __name__)

    def _log(self, level, msg, *args, **kwargs):
        self._logf(msg)


def sleep_on_start(
    seconds: DelayT,
    *,
    sleep: SleepT = time.sleep,
    logger: logging.Logger = logger,
):
    if not isinstance(logger, logging.Logger):
        logger = DummyLogger(logger)

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwds):
            logger.debug(
                f'{f.__qualname__} sleep {seconds} seconds on start:'
                f' '
                f'{relative_to_cwd(f.__code__.co_filename)}:{f.__code__.co_firstlineno}'
            )
            sleep(seconds)
            return f(*args, **kwds)

        return wrapper

    return decorator


def _fork_delays(delays: SingleOrIterable[DelayT]):
    if not isinstance(delays, t.Iterable):
        delays = repeat(delays)
    delays, delays_ = tee(delays)
    delays_ = cycle(delays_)
    return delays, delays_


def retry(
    retries: RetriesT = None,
    *,
    exceptions: SingleOrTuple[t.Type[Exception]] = Exception,
    error_callback: t.Optional[t.Callable[[int, Exception, DelayT, RetriesT, FuncT], None]] = None,
    sleep: SleepT = time.sleep,
    delays: SingleOrIterable[DelayT] = 0,
    first_delay: t.Optional[DelayT] = None,
    chain_exception: bool = False,
    logger: t.Union[logging.Logger, LogfT] = logger,
):
    if not isinstance(logger, logging.Logger):
        logger = DummyLogger(logger)

    def _default_error_callback(i: int, e: Exception, d: DelayT, r: RetriesT, f: FuncT):
        log_prefix = (
            f'{f.__qualname__} tried {i} of {r}:'
            f' '
            f'{relative_to_cwd(f.__code__.co_filename)}:{f.__code__.co_firstlineno}'
            f' '
            f'{e!r}'
        )
        is_last = i == r
        if not is_last:
            logger.info(f'{log_prefix} -> sleep {d} seconds')
        else:
            logger.warning(log_prefix)

    error_callback = error_callback or _default_error_callback

    def callback(i: int, e: Exception, d: DelayT, r: RetriesT, f: FuncT):
        error_callback(i, e, d, r, f)
        if i != r:
            sleep(d)

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            nonlocal delays
            delays, delays_ = _fork_delays(delays)
            function_retrying = partial(f, *args, **kwargs)
            try:
                result = function_retrying()
            except exceptions as e:
                i = 0
                callback(i, e, first_delay or next(delays_), retries, f)
                while True:
                    try:
                        result = function_retrying()
                    except exceptions as e:
                        if i == retries:
                            if chain_exception:
                                raise
                            raise e from None
                        i += 1
                        callback(i, e, next(delays_), retries, f)
                    else:
                        return result
            else:
                return result

        return wrapper

    return decorator
