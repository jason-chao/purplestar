"""
Lunar calendar utilities for 紫微斗數 calculation.

Uses the sxtwl library (寿星万年历) for solar-to-lunar conversion,
supporting dates from ~722 BC to 9999 AD.
"""
import sxtwl


def solar_to_lunar(year: int, month: int, day: int) -> tuple[int, int, int, bool]:
    """Convert solar date to lunar date.

    Returns (lunar_year, lunar_month, lunar_day, is_leap_month).
    lunar_month is 1-12.
    """
    d = sxtwl.fromSolar(year, month, day)
    return d.getLunarYear(), d.getLunarMonth(), d.getLunarDay(), d.isLunarLeap()


def get_year_gz(solar_year: int, solar_month: int, solar_day: int) -> tuple[int, int]:
    """Get year's heavenly stem and earthly branch indices using 立春 boundary.

    Returns (stem_index, branch_index) where stem is 0-9 and branch is 0-11.
    Uses Feb 4 as the approximate 立春 boundary (standard for 紫微斗數).
    sxtwl.getYearGZ() already uses 立春 as boundary.
    """
    d = sxtwl.fromSolar(solar_year, solar_month, solar_day)
    gz = d.getYearGZ()
    return gz.tg, gz.dz


def get_day_gz(solar_year: int, solar_month: int, solar_day: int) -> tuple[int, int]:
    """Get day's heavenly stem and earthly branch indices."""
    d = sxtwl.fromSolar(solar_year, solar_month, solar_day)
    gz = d.getDayGZ()
    return gz.tg, gz.dz


def time_to_index(hour: int, minute: int = 0) -> int:
    """Convert clock hour to 時辰 index (0-12).

    0  = 早子時 (00:00-01:00)
    1  = 丑時  (01:00-03:00)
    ...
    11 = 亥時  (21:00-23:00)
    12 = 晚子時 (23:00-00:00)
    """
    total_minutes = hour * 60 + minute
    if total_minutes < 60:       # 00:00-01:00
        return 0
    if total_minutes >= 23 * 60:  # 23:00-00:00
        return 12
    return (hour + 1) // 2


def parse_time(time_str: str | None) -> int:
    """Parse time string 'HH:MM' or 'HH' to time index. None means unknown (子時)."""
    if time_str is None or time_str.lower() in ('unknown', '未知', ''):
        return 0  # default to 早子時
    parts = time_str.strip().split(':')
    hour = int(parts[0])
    minute = int(parts[1]) if len(parts) > 1 else 0
    return time_to_index(hour, minute)
