from typing import ParamSpec, Callable, Awaitable, TypeVar
from functools import wraps
from .promise import Promise

A = TypeVar('A')

P = ParamSpec('P')
def lift(f: Callable[P, Awaitable[A]]) -> Callable[P, Promise[A]]:
  """Lift a function `f` to return an `AsyncIter`"""
  @wraps(f)
  def _f(*args: P.args, **kwargs: P.kwargs) -> Promise[A]:
    return Promise(f(*args, **kwargs))
  return _f