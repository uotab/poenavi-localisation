"""Global pytest isolation for files that PoENavi normally writes per user."""

import os
import tempfile

_TEST_USER_DATA_DIR = tempfile.mkdtemp(prefix="poenavi-pytest-user-data-")
os.environ.setdefault("POENAVI_USER_DATA_DIR", _TEST_USER_DATA_DIR)
# 実運用用daemon writerをpytest終了時のQt teardownへ残さない。
os.environ.setdefault("POETORE_DISABLE_PERFORMANCE_LOG", "1")


import pytest  # noqa: E402


@pytest.fixture(autouse=True)
def _restore_ui_locale():
    """Tests that switch to English must not leak that locale into later tests."""
    from src.utils.i18n import JA, get_locale, set_locale

    original = get_locale()
    yield
    if get_locale() != original:
        set_locale(original if original else JA)
