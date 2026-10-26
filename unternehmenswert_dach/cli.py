# -*- coding: utf-8 -*-
"""
CLI fuer den DACH KMU-Unternehmenswert-, EBIT-Multiple- & Ertragswert-Rechner 2026
"""

import argparse
import json
from .calculator import ValuationInput, calculate_valuation, get_country_defaults


def main():
    parser = argparse.ArgumentParser(
        description="DACH KMU-Unternehmenswert-, EBIT-Multiple- & Vereinfachtes Ertragswertverfahren-Rechner 2026"
    )
    parser.add_argument("--country", default="DE", choices=["DE", "AT", "CH"], help="Land (DE, AT, CH)")
    parser.add_argument("--revenue", type=float, default=3_500_000.0, help="Nachhaltiger Jahresumsatz")
    parser.add_argument("--ebit", type=float, default=520_000.0, help="Bereinigtes EBIT vor Unternehmerlohn")
    parser.add_argument("--owner-salary", type=float, default=120_000.0, help="Kalkulatorischer Unternehmerlohn (GF)")
    parser.add_argument("--multiple", type=float, default=5.8, help="Branchen-EBIT-Multiplikator")
    parser.add_argument("--cash", type=float, default=280_000.0, help="Liquide Mittel (Cash)")
    parser.add_argument("--debt", type=float, default=450_000.0, help="Verzinsliche Finanzverbindlichkeiten (Debt)")
    parser.add_argument("--substanzwert", type=float, default=850_000.0, help="Substanzwert (Netto-Inventarwert)")
    parser.add_argument("--stake", type=float, default=100.0, help="Gesellschafteranteil in Prozent (%%)")
    parser.add_argument("--json", action="store_true", help="Ausgabe als JSON")

    args = parser.parse_args()
    std = get_country_defaults(args.country)

    inp = ValuationInput(
        country=args.country,
        annual_revenue=args.revenue,
        adjusted_ebit_before_owner=args.ebit,
        imputed_owner_salary=args.owner_salary,
        ebit_multiple=args.multiple,
        cash_and_equivalents=args.cash,
        financial_debt=args.debt,
        substanzwert_nav=args.substanzwert,
        cap_rate_pct=std["default_cap_rate_pct"],
        tax_rate_pct=std["tax_rate_pct"],
        bewg_factor=std["bewg_factor"],
        share_stake_pct=args.stake,
    )
    res = calculate_valuation(inp)

    if args.json:
        print(json.dumps(res.__dict__, indent=2, ensure_ascii=False))
    else:
        print("=" * 76)
        print(f"DACH KMU-UNTERNEHMENSBEWERTUNG 2026 ({res.country} / {res.currency})")
        print("=" * 76)
        print(f"Systematik                 : {res.description}")
        print(f"Nachhaltiges EBIT (n. GF)  : {res.sustainable_ebit:,.2f} {res.currency} ({res.ebit_margin_pct:.1f} % Marge)")
        print(f"1. Enterprise Value (EV)   : {res.enterprise_value_multiple:,.2f} {res.currency}")
        print(f"   Equity Value (100 %)    : {res.equity_value_multiple:,.2f} {res.currency} (Net Debt: {res.net_debt_adjustment:+,.2f})")
        print(f"2. DE BewG (§ 203 13,75x)  : {res.bewg_tax_minimum_value:,.2f} {res.currency}")
        print(f"3. CH Praktikermethode     : {res.ch_praktiker_value:,.2f} {res.currency}")
        print(f"Ø Bewertungskorridor       : {res.valuation_corridor_mean:,.2f} {res.currency}")
        print(f"Anteilswert ({res.share_stake_pct:.1f} %)     : {res.stake_value_multiple:,.2f} {res.currency} (M&A Equity Value)")
        print("=" * 76)


if __name__ == "__main__":
    main()
