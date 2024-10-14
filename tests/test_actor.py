import dm_env
import numpy as np
import torch
import torch.nn as nn
from dm_env.specs import Array, BoundedArray, DiscreteArray

from clowder import environment_loop, specs
from clowder.actor import FeedForwardActor
from tests import mocks


def _make_fake_env() -> dm_env.Environment:
    env_spec = specs.EnvironmentSpec(
        observations=Array(shape=(10, 5), dtype=np.float32),
        actions=DiscreteArray(num_values=3, dtype=np.int64),
        rewards=Array(shape=(), dtype=np.float32),
        discounts=BoundedArray(shape=(), dtype=np.float32, minimum=0.0, maximum=1.0),
    )
    return mocks.Environment(env_spec, episode_length=10)


class Flatten(nn.Module):
    def forward(self, input):
        return torch.flatten(input, start_dim=1)


class ArgMax(nn.Module):
    def forward(self, x):
        return torch.argmax(x, dim=-1).to(torch.int64)


def test_feedforward():
    environment = _make_fake_env()
    env_spec = specs.make_environment_spec(environment)

    network = nn.Sequential(
        Flatten(),
        nn.Linear(50, env_spec.actions.num_values),
        ArgMax(),
    )

    actor = FeedForwardActor(network)
    loop = environment_loop.EnvironmentLoop(actor, environment)
    loop.run(20)
