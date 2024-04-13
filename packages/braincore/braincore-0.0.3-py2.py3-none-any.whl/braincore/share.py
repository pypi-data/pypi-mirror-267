# Copyright 2024 BDP Ecosystem Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# -*- coding: utf-8 -*-


import contextlib
from typing import Any

__all__ = [
  'clear', 'set', 'get', 'save', 'load', 'context',
]

# Default, there are several shared arguments in the global context.
I = 'i'  # the index of the current computation.
T = 't'  # the current time of the current computation.
JIT_ERROR_CHECK = 'jit_error_check'  # whether to record the current computation.
FIT = 'fit'  # whether to fit the model.

_context = dict()
_NOT_PROVIDE = object()


def clear() -> None:
  """
  Clear all shared data in this computation context.
  """
  _context.clear()


def set(**kwargs) -> None:
  """
  Save shared arguments in the global context.
  """
  for k, v in kwargs.items():
    _context[k] = v


def get(key: str, default: Any = _NOT_PROVIDE, desc: str = None) -> Any:
  """
  Get shared arguments in the global context.

  Args:
    key: str
      The key of the shared argument.
    default: Any
      The default value if the key is not found.
    desc: str
      The description of the key.
  """
  if key not in _context:
    if default is _NOT_PROVIDE:
      if desc is not None:
        raise KeyError(f"Key '{key}' not found in the context. You can set it "
                       f"by `braincore.share.set({key}=value)`. {desc}")
      else:
        raise KeyError(f"Key '{key}' not found in the context. You can set it "
                       f"by `braincore.share.set({key}=value)`.")
    return default
  return _context[key]


@contextlib.contextmanager
def context(**kwargs):
  """
  A context manager to set shared arguments in the global context.
  """
  old_conflict = dict()
  for k, v in kwargs.items():
    # Save the old shared arguments.
    if k in _context:
      old_conflict[k] = _context[k]
    # Set the new shared arguments.
    _context[k] = v
  try:
    yield
  finally:
    # Remove the current shared arguments.
    for k, v in kwargs.items():
      if k in _context:
        del _context[k]
    # Restore the old shared arguments.
    set(**old_conflict)


save = set
load = get
