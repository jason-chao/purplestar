"""Tests for true-solar-time correction and place-of-birth lookup."""
from datetime import date, time

import pytest

from purplestar.core.chart import generate_chart
from purplestar.core.geo import resolve_place
from purplestar.core.solar_time import (
    apply_true_solar,
    equation_of_time_minutes,
    true_solar_offset_minutes,
    tz_meridian_deg,
)


def test_eot_within_known_bounds():
    # EoT magnitude over a year stays within ~17 minutes.
    extremes = [equation_of_time_minutes(date(2020, m, 1)) for m in range(1, 13)]
    assert max(extremes) < 17.0
    assert min(extremes) > -17.0


def test_tz_meridian_taipei():
    assert tz_meridian_deg(date(2020, 6, 1), 'Asia/Taipei') == pytest.approx(120.0)


def test_offset_taipei_summer():
    # Taipei lon 121.5, tz meridian 120, EoT(2020-06-01) ≈ +2.4 min
    # Total ≈ 4*1.5 + 2.4 = ~8.4 min
    off = true_solar_offset_minutes(121.5, date(2020, 6, 1), 'Asia/Taipei')
    assert 7.0 < off < 10.0


def test_apply_true_solar_returns_offset():
    d2, t2, off = apply_true_solar(date(1990, 3, 15), time(4, 0), 121.5, 'Asia/Taipei')
    # March 15: EoT ≈ -9 min, lon offset = +6 → ~ -3 min
    assert -6.0 < off < -1.0
    assert d2 == date(1990, 3, 15)
    assert t2.hour == 3 and t2.minute > 50


def test_resolve_place_taipei():
    m = resolve_place('Taipei, TW')
    assert m is not None
    assert m.country == 'TW'
    assert m.tz == 'Asia/Taipei'
    assert 121.0 < m.lon < 122.0


def test_resolve_place_with_country_disambiguation():
    # "London" without CC → London, GB (highest population)
    m = resolve_place('London')
    assert m.country == 'GB'
    # "London, CA" → London, Ontario, Canada
    m_ca = resolve_place('London, CA')
    assert m_ca is not None
    assert m_ca.country == 'CA'


def test_resolve_place_miss_returns_none():
    assert resolve_place('NowhereCity12345') is None
    assert resolve_place('') is None


def test_chart_unchanged_without_longitude():
    """Without --longitude or resolvable --place, output matches today's behaviour."""
    c = generate_chart(gender='male', solar_date='1990-03-15',
                       time='04:00', timezone='Asia/Taipei')
    assert c['birth_data']['solar_time_correction'] == {'applied': False}
    assert c['birth_data']['place_resolution'] == {'source': 'none'}
    # Hour branch stays at 寅 for 04:00.
    assert c['birth_data']['hour_zh'] == '寅時'


def test_chart_explicit_longitude_applies_correction():
    c = generate_chart(gender='male', solar_date='1990-03-15', time='04:00',
                       timezone='Asia/Taipei', longitude=121.5)
    stc = c['birth_data']['solar_time_correction']
    assert stc['applied'] is True
    assert stc['original_time'] == '04:00'
    assert stc['longitude'] == 121.5
    assert -10 < stc['offset_minutes'] < 0
    assert c['birth_data']['place_resolution']['source'] == 'explicit'


def test_chart_place_lookup_fills_lonlat_and_tz():
    c = generate_chart(gender='male', solar_date='1990-03-15', time='04:00',
                       place='Taipei, TW')
    pr = c['birth_data']['place_resolution']
    assert pr['source'] == 'geonames'
    assert pr['matched_name'] == 'Taipei'
    assert pr['country'] == 'TW'
    assert c['birth_data']['timezone'] == 'Asia/Taipei'
    assert c['birth_data']['solar_time_correction']['applied'] is True


def test_chart_unresolvable_place_no_correction():
    c = generate_chart(gender='male', solar_date='1990-03-15', time='04:00',
                       timezone='Asia/Taipei', place='Atlantis-XYZ-Nowhere')
    assert c['birth_data']['place_resolution']['source'] == 'none'
    assert c['birth_data']['solar_time_correction'] == {'applied': False}


def test_correction_can_shift_hour_branch():
    """Pick a clock time near a 時辰 boundary and confirm TST flips it.

    03:00 sits exactly at the 丑/寅 boundary; `time_to_index` resolves
    03:00 to 寅. A westward longitude pulling solar time back to ~02:50
    should flip the bucket back to 丑.
    """
    # Use 03:05 in Asia/Taipei but with a far-western longitude (~100°E).
    # tz_meridian = 120°; lon - meridian = -20° → -80 min offset.
    c_no = generate_chart(gender='male', solar_date='1990-03-15', time='03:05',
                          timezone='Asia/Taipei')
    c_yes = generate_chart(gender='male', solar_date='1990-03-15', time='03:05',
                           timezone='Asia/Taipei', longitude=100.0)
    assert c_no['birth_data']['hour_zh'] == '寅時'
    assert c_yes['birth_data']['hour_zh'] == '丑時'
    assert c_yes['birth_data']['solar_time_correction']['applied'] is True


def test_correction_across_midnight_changes_solar_date():
    """A pre-midnight time corrected forward across midnight shifts the date."""
    # 23:55 in Asia/Taipei with lon 150° → offset = +120 min + EoT
    c = generate_chart(gender='male', solar_date='1990-03-15', time='23:55',
                       timezone='Asia/Taipei', longitude=150.0)
    bd = c['birth_data']
    assert bd['solar_time_correction']['applied'] is True
    assert bd['solar_date'] == '1990-03-16'
    assert bd['input_solar_date'] == '1990-03-15'


def test_no_double_correction_with_dst_zone():
    """Sanity: a DST zone (London BST) shouldn't double-correct.

    The tz_meridian is derived from utcoffset() at noon, which already
    includes DST. So applying the formula once on a DST clock reading
    is correct.
    """
    # London on 2020-06-01 is BST (UTC+1), so meridian is 15°.
    # With lon 0 and clock 12:00 BST, true solar ≈ 11:00 + EoT.
    off = true_solar_offset_minutes(0.0, date(2020, 6, 1), 'Europe/London')
    # 4*(0-15) + EoT(2020-06-01, ~+2.4) = -60 + 2.4 = ~-57.6 min
    assert -62 < off < -55
