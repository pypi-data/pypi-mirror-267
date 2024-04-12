# Copyright (C) 2022  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from swh.scrubber.db import ScrubberDb


def get_scrubber_db(cls: str, **kwargs) -> ScrubberDb:
    if cls not in ("local", "postgresql"):
        raise ValueError(
            f"Unknown scrubber db class '{cls}', use 'postgresql' instead."
        )

    from swh.scrubber.db import ScrubberDb

    return ScrubberDb.connect(kwargs.pop("db"), **kwargs)


get_datastore = get_scrubber_db
