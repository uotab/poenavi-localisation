import glob
import os

import cv2
import numpy as np
from PySide6.QtGui import QImage

from src.utils.feature_support import is_feature_hotkey_supported
from src.utils.layout_match import qimage_to_bgr, rank_layouts, read_image
from src.utils.poe_version_data import POE1, POE2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# A PoE1 zone with three bundled layout patterns.
ZONE_PATHS = sorted(glob.glob(os.path.join(ROOT, "maps", "PoE1", "下水道", "*.png")))


def _partial_capture(path):
    """Simulate a partly explored in-game map: an upright crop at another scale, with route lines."""
    image = read_image(path)
    height, width = image.shape[:2]
    crop = image[height // 5: height * 4 // 5, width // 6: width * 5 // 6].copy()
    crop = cv2.resize(crop, None, fx=0.8, fy=0.8)
    cv2.line(crop, (0, 0), (crop.shape[1], crop.shape[0]), (180, 110, 230), 5)
    canvas = np.full((crop.shape[0] + 120, crop.shape[1] + 160, 3), (40, 30, 28), np.uint8)
    canvas[60:60 + crop.shape[0], 80:80 + crop.shape[1]] = crop
    return canvas


def test_each_layout_is_ranked_first_for_its_own_partial_capture():
    assert len(ZONE_PATHS) >= 2
    for truth in ZONE_PATHS:
        capture = _partial_capture(truth)
        ranked = rank_layouts(capture, ZONE_PATHS)
        assert ranked[0][0] == truth


def test_stray_specks_around_the_map_do_not_change_the_result():
    """Game effects and HUD text elsewhere on screen must not flip the ranking between frames."""
    rng = np.random.default_rng(0)
    for truth in ZONE_PATHS:
        overlay = _partial_capture(truth)
        height, width = overlay.shape[:2]
        for _ in range(5):
            capture = np.full((height + 400, width + 600, 3), (40, 30, 28), np.uint8)
            capture[200:200 + height, 300:300 + width] = overlay
            for _ in range(4):
                x, y = rng.integers(6, capture.shape[1] - 6), rng.integers(6, capture.shape[0] - 6)
                cv2.circle(capture, (int(x), int(y)), 3, (200, 170, 170), 1)  # wall-coloured, so only grouping removes it
            assert rank_layouts(capture, ZONE_PATHS)[0][0] == truth


def test_capture_without_map_lines_returns_no_ranking():
    blank = np.full((300, 400, 3), (40, 30, 28), np.uint8)
    assert rank_layouts(blank, ZONE_PATHS) == []


def test_qimage_conversion_keeps_channel_order():
    image = QImage(3, 2, QImage.Format.Format_RGB32)
    image.fill(0xFF102030)  # r=0x10, g=0x20, b=0x30
    bgr = qimage_to_bgr(image)
    assert bgr.shape == (2, 3, 3)
    assert tuple(bgr[0, 0]) == (0x30, 0x20, 0x10)


def test_layout_detection_hotkey_is_poe1_only():
    assert is_feature_hotkey_supported("map_layout_detect", POE1)
    assert not is_feature_hotkey_supported("map_layout_detect", POE2)
