"""A tiny library to define and execute checkpointed pipelines."""

import dataclasses
import json
import os
import sys
from typing import Any, Callable, Optional, Sequence, Tuple, Union

_Args = Tuple[Union['Stage', 'Pipeline'], ...]
_ArgsLike = Union['Stage', 'Pipeline', _Args]


@dataclasses.dataclass(frozen=True)
class Stage:
  """A single function abstraction that may be used to construct a pipeline."""
  func: Callable[..., Any]

  @dataclasses.dataclass
  class wrap:  # pylint: disable=invalid-name
    """A decorator that converts a function into a stage."""

    def __call__(self, func: Callable[..., Any]):
      return Stage(func)

  @classmethod
  def _make_pipeline(cls, stage: 'Stage', args: _ArgsLike) -> 'Pipeline':
    if isinstance(args, Stage):
      args = (Pipeline(args),)
    elif isinstance(args, Pipeline):
      args = (args,)
    else:
      args = tuple(Pipeline(a) if isinstance(a, Stage) else a for a in args)
    return Pipeline(stage, args)

  def __lshift__(self, other: _ArgsLike) -> 'Pipeline':
    return self._make_pipeline(self, other)

  def __rshift__(self, other: 'Stage') -> 'Pipeline':
    return self._make_pipeline(other, self)

  def __rrshift__(self, other: _ArgsLike) -> 'Pipeline':
    return self._make_pipeline(self, other)

  def __str__(self):
    return self.func.__name__

  def __repr__(self):
    return f'Stage[{self.func.__name__}]'

  def __call__(self, *args):
    return self.func(*args)


@dataclasses.dataclass(frozen=True)
class Pipeline:
  """An executable sequence of stages."""
  stage: Stage
  args: _Args = ()

  def __call__(self, cfg: Optional['Config'] = None):
    if (cfg and cfg.should_load(self.stage) and
        os.path.exists(cfg.get_checkpoint_path(self.stage))):
      print(f'[{self.stage}] Loading from checkpoint...', file=sys.stderr)
      with open(cfg.get_checkpoint_path(self.stage)) as f:
        result = json.loads(f.read())
    else:
      if cfg and cfg.should_load(self.stage):
        print(f'[{self.stage}] Checkpoint not found.', file=sys.stderr)
      args = [a(cfg) if isinstance(a, Pipeline) else a() for a in self.args]
      print(f'[{self.stage}] Running...', file=sys.stderr)
      result = self.stage(*args)
      if cfg and cfg.should_store(self.stage):
        print(f'[{self.stage}] Storing to checkpoint...', file=sys.stderr)
        with open(cfg.get_checkpoint_path(self.stage), 'w') as f:
          f.write(json.dumps(result, indent=2))
    print(f'[{self.stage}] Complete', file=sys.stderr)
    return result


@dataclasses.dataclass(frozen=True)
class Config:
  """Pipeline configuration."""
  load: Union[bool, Sequence[Union[Stage, str]]] = False
  store: Union[bool, Sequence[Union[Stage, str]]] = True
  dir: str = f'/tmp/{os.path.basename(sys.argv[0])}'

  def __post_init__(self):
    try:
      os.makedirs(self.dir)
    except FileExistsError:
      pass

  def get_checkpoint_path(self, stage: Stage) -> str:
    return os.path.join(self.dir, str(stage))

  def should_load(self, stage: Stage) -> bool:
    if isinstance(self.load, bool):
      return self.load
    else:
      return stage in self.load or str(stage) in map(str, self.load)

  def should_store(self, stage: Stage) -> bool:
    if isinstance(self.store, bool):
      return self.store
    else:
      return stage in self.store or str(stage) in map(str, self.store)
