# -*- coding: utf-8 -*-
import pytest
from unternehmenswert_dach import (
    ValuationInput,
    calculate_valuation,
    get_country_defaults,
    SECTOR_MULTIPLES,
)


def test_default_de_valuation():
    inp = ValuationInput()
    res = calculate_valuation(inp)
    assert res.country == "DE"
    assert res.currency == "EUR"
    # 520,000 - 120,000 = 400,000 sustainable EBIT
    assert res.sustainable_ebit == 400_000.0
    # EV = 400,000 * 5.8 = 2,320,000
    assert res.enterprise_value_multiple == 2_320_000.0
    # Equity Value = 2,320,000 + 280,000 - 450,000 = 2,150,000
    assert res.equity_value_multiple == 2_150_000.0


def test_bewg_13_75_calculation():
    inp = ValuationInput(
        adjusted_ebit_before_owner=520_000.0,
        imputed_owner_salary=120_000.0,
        substanzwert_nav=850_000.0,
    )
    res = calculate_valuation(inp)
    # Sustainable EBIT = 400,000 -> after 30% tax = 280,000 -> * 13.75 = 3,850,000
    assert res.bewg_ertragswert == 3_850_000.0
    assert res.bewg_tax_minimum_value == 3_850_000.0


def test_bewg_substanzwert_floor():
    # § 200 Abs. 3 BewG: Substanzwert is the minimum tax value
    inp = ValuationInput(
        adjusted_ebit_before_owner=180_000.0,
        imputed_owner_salary=120_000.0,
        substanzwert_nav=1_500_000.0,
    )
    res = calculate_valuation(inp)
    # Sustainable EBIT = 60,000 -> after 30% = 42,000 * 13.75 = 577,500 < 1,500,000
    assert res.bewg_ertragswert == 577_500.0
    assert res.bewg_tax_minimum_value == 1_500_000.0


def test_ch_praktikermethode_ks28():
    std = get_country_defaults("CH")
    inp = ValuationInput(
        country="CH",
        adjusted_ebit_before_owner=500_000.0,
        imputed_owner_salary=100_000.0,
        tax_rate_pct=std["tax_rate_pct"],  # 15%
        cap_rate_pct=10.0,
        substanzwert_nav=1_400_000.0,
    )
    res = calculate_valuation(inp)
    assert res.currency == "CHF"
    # Net earnings = 400,000 * 0.85 = 340,000 -> capitalized at 10% = 3,400,000
    assert res.capitalized_earnings_value == 3_400_000.0
    # Praktikermethode = (2 * 3,400,000 + 1,400,000) / 3 = 8,200,000 / 3 = 2,733,333.33
    assert res.ch_praktiker_value == pytest.approx(2_733_333.33, abs=0.05)
    assert res.country_reference_value == res.ch_praktiker_value


def test_at_kfs_bw1_valuation():
    std = get_country_defaults("AT")
    inp = ValuationInput(
        country="AT",
        adjusted_ebit_before_owner=300_000.0,
        imputed_owner_salary=100_000.0,
        tax_rate_pct=std["tax_rate_pct"],  # 23% KÖSt
        cap_rate_pct=10.0,
    )
    res = calculate_valuation(inp)
    # 200,000 * (1 - 0.23) = 154,000 / 0.10 = 1,540,000
    assert res.sustainable_net_earnings == 154_000.0
    assert res.capitalized_earnings_value == 1_540_000.0
    assert res.country_reference_value == 1_540_000.0


def test_shareholder_stake_calculation():
    inp = ValuationInput(share_stake_pct=25.0)
    res = calculate_valuation(inp)
    assert res.stake_value_multiple == pytest.approx(res.equity_value_multiple * 0.25, abs=0.01)
    assert res.stake_value_mean == pytest.approx(res.valuation_corridor_mean * 0.25, abs=0.01)


def test_non_operating_assets_addition():
    base = calculate_valuation(ValuationInput(non_operating_assets=0.0))
    with_noa = calculate_valuation(ValuationInput(non_operating_assets=200_000.0))
    assert with_noa.equity_value_multiple == base.equity_value_multiple + 200_000.0
    assert with_noa.bewg_ertragswert == base.bewg_ertragswert + 200_000.0


def test_owner_salary_exceeds_ebit_floors_at_zero():
    inp = ValuationInput(adjusted_ebit_before_owner=80_000.0, imputed_owner_salary=120_000.0)
    res = calculate_valuation(inp)
    assert res.sustainable_ebit == 0.0
    assert res.enterprise_value_multiple == 0.0


def test_sector_presets_exist():
    assert "saas" in SECTOR_MULTIPLES
    assert SECTOR_MULTIPLES["saas"]["ebit_multiple"] > SECTOR_MULTIPLES["handwerk"]["ebit_multiple"]


def test_invalid_inputs_raise():
    with pytest.raises(ValueError):
        get_country_defaults("FR")
    with pytest.raises(ValueError):
        calculate_valuation(ValuationInput(ebit_multiple=0.0))
    with pytest.raises(ValueError):
        calculate_valuation(ValuationInput(share_stake_pct=120.0))
