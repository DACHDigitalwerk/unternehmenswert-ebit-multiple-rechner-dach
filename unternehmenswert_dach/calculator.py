# -*- coding: utf-8 -*-
"""
Finanzmathematisches Kernmodul fuer den
DACH KMU-Unternehmenswert-, EBIT-Multiple- & Vereinfachtes Ertragswertverfahren-Rechner 2026
nach §§ 199-203 BewG (DE), KFS/BW 1 (AT) und ESTV KS 28 Praktikermethode (CH).

Rechtlicher Hinweis (§ 2 RDG / § 5 StBerG / § 43 WPO):
Rein mathematische Orientierungsrechnung, kein Wirtschaftspruefungsgutachten.
"""

from dataclasses import dataclass
from typing import Dict, Any


COUNTRY_DEFAULTS: Dict[str, Dict[str, Any]] = {
    "DE": {
        "currency": "EUR",
        "tax_rate_pct": 30.0,
        "bewg_factor": 13.75,
        "default_cap_rate_pct": 9.5,
        "description": "DE: Vereinfachtes Ertragswertverfahren (§§ 199-203 BewG, 30 % Pauschalsteuer, Faktor 13,75)",
    },
    "AT": {
        "currency": "EUR",
        "tax_rate_pct": 23.0,
        "bewg_factor": 13.75,
        "default_cap_rate_pct": 9.5,
        "description": "AT: KFS/BW 1 Ertragswertverfahren (23 % KOeSt ab 2024, Ewige Rente mit WACC/Kapitalisierungszins)",
    },
    "CH": {
        "currency": "CHF",
        "tax_rate_pct": 15.0,
        "bewg_factor": 13.75,
        "default_cap_rate_pct": 8.5,
        "description": "CH: ESTV Kreisschreiben Nr. 28 Praktikermethode ((2 x Ertragswert + 1 x Substanzwert) / 3)",
    },
}

SECTOR_MULTIPLES: Dict[str, Dict[str, float]] = {
    "saas": {"ebit_multiple": 7.2, "cap_rate_pct": 8.5},
    "industrie": {"ebit_multiple": 5.8, "cap_rate_pct": 9.5},
    "handwerk": {"ebit_multiple": 4.5, "cap_rate_pct": 10.5},
    "handel": {"ebit_multiple": 4.9, "cap_rate_pct": 10.0},
    "agentur": {"ebit_multiple": 4.2, "cap_rate_pct": 11.0},
}


@dataclass
class ValuationInput:
    country: str = "DE"
    annual_revenue: float = 3_500_000.0
    adjusted_ebit_before_owner: float = 520_000.0
    imputed_owner_salary: float = 120_000.0
    ebit_multiple: float = 5.8
    cash_and_equivalents: float = 280_000.0
    financial_debt: float = 450_000.0
    substanzwert_nav: float = 850_000.0
    non_operating_assets: float = 0.0
    cap_rate_pct: float = 9.5
    tax_rate_pct: float = 30.0
    bewg_factor: float = 13.75
    share_stake_pct: float = 100.0


@dataclass
class ValuationResult:
    country: str
    currency: str
    description: str
    sustainable_ebit: float
    ebit_margin_pct: float
    sustainable_net_earnings: float
    enterprise_value_multiple: float
    net_debt_adjustment: float
    equity_value_multiple: float
    bewg_ertragswert: float
    bewg_tax_minimum_value: float
    capitalized_earnings_value: float
    ch_praktiker_value: float
    country_reference_value: float
    valuation_corridor_min: float
    valuation_corridor_max: float
    valuation_corridor_mean: float
    share_stake_pct: float
    stake_value_multiple: float
    stake_value_mean: float


def get_country_defaults(country: str) -> Dict[str, Any]:
    c = country.upper().strip()
    if c not in COUNTRY_DEFAULTS:
        raise ValueError(f"Unsupported country '{country}'. Choose from DE, AT, CH.")
    return COUNTRY_DEFAULTS[c]


def calculate_valuation(inp: ValuationInput) -> ValuationResult:
    std = get_country_defaults(inp.country)
    c = inp.country.upper().strip()

    if inp.annual_revenue < 0:
        raise ValueError("annual_revenue must be non-negative")
    if inp.ebit_multiple <= 0:
        raise ValueError("ebit_multiple must be positive")
    if inp.cap_rate_pct <= 0:
        raise ValueError("cap_rate_pct must be positive")
    if not (0.0 <= inp.tax_rate_pct < 100.0):
        raise ValueError("tax_rate_pct must be in [0, 100)")
    if not (0.0 < inp.share_stake_pct <= 100.0):
        raise ValueError("share_stake_pct must be in (0, 100]")

    sustainable_ebit = max(0.0, float(inp.adjusted_ebit_before_owner) - max(0.0, float(inp.imputed_owner_salary)))
    ebit_margin_pct = (sustainable_ebit / float(inp.annual_revenue) * 100.0) if inp.annual_revenue > 0 else 0.0

    # 1. M&A EBIT-Multiple (Enterprise Value -> Equity Value)
    ev_multiple = sustainable_ebit * float(inp.ebit_multiple)
    net_cash_debt = float(inp.cash_and_equivalents) - float(inp.financial_debt) + float(inp.non_operating_assets)
    equity_value_multiple = max(0.0, ev_multiple + net_cash_debt)

    # 2. Sustainable net earnings after flat corporate tax
    tax_ratio = float(inp.tax_rate_pct) / 100.0
    sustainable_net_earnings = sustainable_ebit * (1.0 - tax_ratio)

    # 3. German §§ 199-203 BewG Simplified Capitalized Earnings Method (Factor 13.75)
    bewg_net_de = sustainable_ebit * (1.0 - 0.30)
    bewg_ertragswert = bewg_net_de * float(inp.bewg_factor) + float(inp.non_operating_assets)
    substanz_total = max(0.0, float(inp.substanzwert_nav)) + max(0.0, float(inp.non_operating_assets))
    bewg_tax_min = max(bewg_ertragswert, substanz_total)

    # 4. Capitalized Earnings (Ewige Rente / KFS BW 1) & Swiss Praktikermethode (ESTV KS 28)
    cap_ratio = float(inp.cap_rate_pct) / 100.0
    capitalized_earnings_val = (sustainable_net_earnings / cap_ratio) + float(inp.non_operating_assets)
    ch_praktiker_val = (2.0 * capitalized_earnings_val + 1.0 * substanz_total) / 3.0

    if c == "CH":
        country_ref_val = ch_praktiker_val
    elif c == "AT":
        country_ref_val = capitalized_earnings_val
    else:
        country_ref_val = bewg_tax_min

    vals = [equity_value_multiple, bewg_tax_min, ch_praktiker_val]
    corridor_min = min(vals)
    corridor_max = max(vals)
    corridor_mean = sum(vals) / 3.0

    stake_ratio = float(inp.share_stake_pct) / 100.0
    stake_val_multiple = equity_value_multiple * stake_ratio
    stake_val_mean = corridor_mean * stake_ratio

    return ValuationResult(
        country=c,
        currency=std["currency"],
        description=std["description"],
        sustainable_ebit=round(sustainable_ebit, 2),
        ebit_margin_pct=round(ebit_margin_pct, 2),
        sustainable_net_earnings=round(sustainable_net_earnings, 2),
        enterprise_value_multiple=round(ev_multiple, 2),
        net_debt_adjustment=round(net_cash_debt, 2),
        equity_value_multiple=round(equity_value_multiple, 2),
        bewg_ertragswert=round(bewg_ertragswert, 2),
        bewg_tax_minimum_value=round(bewg_tax_min, 2),
        capitalized_earnings_value=round(capitalized_earnings_val, 2),
        ch_praktiker_value=round(ch_praktiker_val, 2),
        country_reference_value=round(country_ref_val, 2),
        valuation_corridor_min=round(corridor_min, 2),
        valuation_corridor_max=round(corridor_max, 2),
        valuation_corridor_mean=round(corridor_mean, 2),
        share_stake_pct=round(float(inp.share_stake_pct), 2),
        stake_value_multiple=round(stake_val_multiple, 2),
        stake_value_mean=round(stake_val_mean, 2),
    )
