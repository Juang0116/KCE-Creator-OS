from functools import lru_cache

from src.application import DiscoveryFacadeV0
from src.bootstrap import create_discovery


@lru_cache(maxsize=1)
def get_discovery() -> DiscoveryFacadeV0:
    return create_discovery()