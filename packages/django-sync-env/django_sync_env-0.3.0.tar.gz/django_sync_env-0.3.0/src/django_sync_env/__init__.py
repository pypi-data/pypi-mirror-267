from django_sync_env.utils import get_semver_version, get_version

# major.minor.patch.release.number
# release must be one of alpha, beta, rc, or final
VERSION = (0, 2, 9, "final", 0)

__version__ = get_version(VERSION)

# Required for npm package for frontend
__semver__ = get_semver_version(VERSION)
