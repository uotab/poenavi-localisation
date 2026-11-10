"""Rank a zone's bundled layout images against a capture of the in-game map overlay.

Both images are reduced to a mask of the light, low-saturation map lines, so the
coloured route arrows and markers drawn on the reference images are ignored.
The capture is usually a partly explored subset of the reference, so it is used
as a template searched across scales and all 8 rotations/mirrorings.
"""

from __future__ import annotations

from functools import lru_cache

import cv2
import numpy as np

WORK_SIZE = 240  # long side of the normalised reference, in pixels
TEMPLATE_SCALES = np.linspace(0.3, 1.0, 10)  # capture size relative to the reference
MIN_CONTENT_PIXELS = 50
UNCERTAIN_MARGIN = 0.02  # best-vs-runner-up score gap below which the result is flagged
NOISE_SHARE = 0.25  # capture groups smaller than this share of the largest are discarded (life globe ~11%)


def qimage_to_bgr(image) -> np.ndarray:
    """Convert a QImage (e.g. from QScreen.grabWindow) to an OpenCV BGR array."""
    from PySide6.QtGui import QImage

    converted = image.convertToFormat(QImage.Format.Format_BGR888)
    height, width = converted.height(), converted.width()
    buffer = np.frombuffer(converted.constBits(), dtype=np.uint8, count=converted.sizeInBytes())
    rows = buffer.reshape(height, converted.bytesPerLine())
    return rows[:, : width * 3].reshape(height, width, 3).copy()


def read_image(path: str) -> np.ndarray:
    """cv2.imread cannot open non-ASCII paths on Windows (zone folders are Japanese)."""
    data = np.fromfile(path, dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"cannot decode image: {path}")
    return image


def wall_mask(bgr: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    hue, saturation, value = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    # Map walls are a pale blue-violet (hue ~105-125); HUD text is pure white (saturation 0)
    # and HUD frames/icons are gold, so both are excluded by hue and minimum saturation.
    lavender = (hue >= 100) & (hue <= 130) & (saturation >= 20)
    mask = (lavender & (saturation < 90) & (value > 110)).astype(np.uint8) * 255
    # Map lines are thin; solid bright areas (screenshot borders, UI panels) are not walls.
    solid = cv2.dilate(cv2.erode(mask, np.ones((7, 7), np.uint8)), np.ones((11, 11), np.uint8))
    return cv2.bitwise_and(mask, cv2.bitwise_not(solid))


def drop_specks(mask: np.ndarray) -> np.ndarray:
    """Drop isolated specks (game effects, HUD text) that would stretch the capture's
    bounding box and change the match from frame to frame. Map lines can be broken into
    many tiny pieces, so pieces are grouped by proximity first and whole groups smaller
    than NOISE_SHARE of the largest group are removed."""
    reach = max(5, max(mask.shape) // 60) | 1
    grouped = cv2.dilate(mask, np.ones((reach, reach), np.uint8))
    count, labels, stats, _ = cv2.connectedComponentsWithStats(grouped, connectivity=8)
    if count <= 1:
        return mask
    areas = stats[1:, cv2.CC_STAT_AREA]
    keep = np.flatnonzero(areas >= areas.max() * NOISE_SHARE) + 1
    return np.where(np.isin(labels, keep), mask, 0).astype(np.uint8)


def _crop_and_scale(mask: np.ndarray, long_side: float) -> np.ndarray | None:
    ys, xs = np.nonzero(mask)
    if len(xs) < MIN_CONTENT_PIXELS:
        return None
    cropped = mask[ys.min(): ys.max() + 1, xs.min(): xs.max() + 1]
    height, width = cropped.shape
    factor = long_side / max(height, width)
    size = (max(1, round(width * factor)), max(1, round(height * factor)))
    scaled = cv2.resize(cropped, size, interpolation=cv2.INTER_AREA)
    # Thin lines fade when shrunk; re-binarise, then blur for positional tolerance.
    scaled = (scaled > 0).astype(np.float32)
    return cv2.GaussianBlur(scaled, (0, 0), 2)


def _orientations(image: np.ndarray):
    for flipped in (image, cv2.flip(image, 1)):
        for turns in range(4):
            yield np.ascontiguousarray(np.rot90(flipped, turns))


@lru_cache(maxsize=64)
def _reference(path: str) -> np.ndarray | None:
    prepared = _crop_and_scale(wall_mask(read_image(path)), WORK_SIZE)
    if prepared is None:
        return None
    margin = WORK_SIZE // 10
    return cv2.copyMakeBorder(prepared, margin, margin, margin, margin, cv2.BORDER_CONSTANT, value=0)


def _normalised_correlation(reference: np.ndarray, template: np.ndarray) -> float:
    # cv2's *_NORMED modes blow up to ~1.0 over empty reference windows, so
    # normalise manually with the window energy floored at a share of the template's.
    template_energy = float((template * template).sum())
    raw = cv2.matchTemplate(reference, template, cv2.TM_CCORR)
    window_energy = cv2.matchTemplate(reference * reference, np.ones_like(template), cv2.TM_CCORR)
    window_energy = np.maximum(window_energy, template_energy * 0.25)
    return float((raw / np.sqrt(template_energy * window_energy)).max())


def _score(reference: np.ndarray, capture_mask: np.ndarray) -> float:
    best = 0.0
    for scale in TEMPLATE_SCALES:
        template = _crop_and_scale(capture_mask, WORK_SIZE * scale)
        if template is None:
            return best
        for oriented in _orientations(template):
            th, tw = oriented.shape
            if th > reference.shape[0] or tw > reference.shape[1]:
                continue
            best = max(best, _normalised_correlation(reference, oriented))
    return best


def rank_layouts(capture_bgr: np.ndarray, paths: list[str]) -> list[tuple[str, float]]:
    """Return (path, score) best-first; scores are in [0, 1]. Empty if the capture shows no map."""
    capture_mask = drop_specks(wall_mask(capture_bgr))
    if np.count_nonzero(capture_mask) < MIN_CONTENT_PIXELS:
        return []
    ranked = []
    for path in paths:
        reference = _reference(path)
        if reference is not None:
            ranked.append((path, _score(reference, capture_mask)))
    return sorted(ranked, key=lambda item: item[1], reverse=True)
