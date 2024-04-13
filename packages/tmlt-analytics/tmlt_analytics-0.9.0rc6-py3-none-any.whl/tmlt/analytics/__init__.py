"""`Tumult Labs' <https://tmlt.io>`_ differentially private analytics library."""

# SPDX-License-Identifier: Apache-2.0
# Copyright Tumult Labs 2024

# These gets automatically replaced by the version number during the release process
# by poetry-dynamic-versioning.
__version__ = "0.9.0-rc.6"
__version_tuple__ = (0, 9, 0, "rc", 6)

from typing import List

from tmlt.core.utils.configuration import check_java11

__all__: List[str] = []

try:
    # Addresses https://nvd.nist.gov/vuln/detail/CVE-2023-47248 for Python 3.7
    # Python 3.8+ resolve this by using PyArrow >=14.0.1, so it may not be available
    import pyarrow_hotfix
except ImportError:
    pass

check_java11()
