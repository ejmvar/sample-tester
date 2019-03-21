# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



import logging
from typing import Iterable

from sampletester import convention

def new(convention_spec: str,
               user_paths: Iterable[str] = None):
  """Returns a new registry based on the `convention_spec` and `user_paths`.

  The registry contains all the environments generated by the named convention
  when passed the `user_paths`.

  The `convention_spec` is specified as "NAME:ARG,ARG,...". The array of ARGs is passed
  to the NAMEd convention upon initialization.
  """
  parts = convention_spec.split(":", 1)
  convention_name = parts[0]
  convention_args = parts[1].split(",") if len(parts) > 1 else None

  user_paths = user_paths or []
  registry = Registry()
  registry.add(*convention.generate_environments([convention_name], convention_args, user_paths))
  return registry

class Registry:
  """Stores the registered test execution environments."""

  def __init__(self):
    self.envs = {}

  def add(self, *environments):
    """Instantiates and stores a new testenv.Base with the given parameters.
    """
    for env in environments:
      self.envs[env.name()] = env

  def get_names(self):
    """Returns the names of all the registered environments."""
    return list(self.envs.keys())

  def list(self):
    """Return all the registered environments."""
    return self.envs.values()