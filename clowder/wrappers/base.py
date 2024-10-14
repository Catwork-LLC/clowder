"""Environment wrapper base class."""

from typing import Callable, Sequence

import dm_env


class EnvironmentWrapper(dm_env.Environment):
    """Environment that wraps another environment.

    This exposes the wrapped environment with the `.environment` property and also
    defines `__getattr__` so that attributes are invisibly forwarded to the
    wrapped environment (and hence enabling duck-typing).
    """

    _environment: dm_env.Environment

    def __init__(self, environment: dm_env.Environment):
        self._environment = environment

    def __getattr__(self, name):
        if name.startswith("__"):
            raise AttributeError(f"attempted to get missing private attribute '{name}'")
        return getattr(self._environment, name)

    @property
    def environment(self) -> dm_env.Environment:
        return self._environment

    # The following lines are necessary because methods defined in
    # `dm_env.Environment` are not delegated through `__getattr__`, which would
    # only be used to expose methods or properties that are not defined in the
    # base `dm_env.Environment` class.

    def step(self, action) -> dm_env.TimeStep:
        return self._environment.step(action)

    def reset(self) -> dm_env.TimeStep:
        return self._environment.reset()

    def action_spec(self):
        return self._environment.action_spec()

    def discount_spec(self):
        return self._environment.discount_spec()

    def observation_spec(self):
        return self._environment.observation_spec()

    def reward_spec(self):
        return self._environment.reward_spec()

    def close(self):
        return self._environment.close()


def wrap_all(
    environment: dm_env.Environment,
    wrappers: Sequence[Callable[[dm_env.Environment], dm_env.Environment]],
) -> dm_env.Environment:
    """Given an environment, wrap it in a list of wrappers."""
    for w in wrappers:
        environment = w(environment)

    return environment
