# 🏛️ DACH KMU-Unternehmenswert-, EBIT-Multiple- & Vereinfachtes Ertragswertverfahren-Rechner 2026 (`unternehmenswert_dach`)

[![CI & Pytest](https://github.com/DACHDigitalwerk/unternehmenswert-ebit-multiple-rechner-dach/actions/workflows/ci.yml/badge.svg)](https://github.com/DACHDigitalwerk/unternehmenswert-ebit-multiple-rechner-dach/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Live Web-App](https://img.shields.io/badge/Live_Web_App-100%25_Client_Side-10b981)](https://dachdigitalwerk.github.io/unternehmenswert-ebit-multiple-rechner/)

Finanzmathematische Python-Bibliothek und CLI (`dach-valuation`) zur **3-Methoden-Unternehmensbewertung von KMU, GmbHs und AGs** für **Deutschland (§§ 199–203 BewG mit Kapitalisierungsfaktor 13,75), Österreich (KFS/BW 1 Ertragswert & 23 % KÖSt) und die Schweiz (ESTV Kreisschreiben Nr. 28 Praktikermethode 2×EW+1×SW)** sowie nach dem **M&A Branchen-EBIT-Multiple (Enterprise Value zu Equity Value / Cash- & Debt-Free)**.

---

## 🌐 Interaktive Web-Applikation & M&A/Steuer-Fachratgeber (100 % Client-Side)

Nutzen Sie den kostenlosen Online-Rechner mit **druckfertigem DIN-A4 Unternehmenswert- & M&A-Bewertungsdossier** direkt im Browser:

- 🚀 **[DACH KMU-Unternehmenswert-, EBIT-Multiple- & Vereinfachtes Ertragswertverfahren-Rechner 2026](https://dachdigitalwerk.github.io/unternehmenswert-ebit-multiple-rechner/)**
- 📘 **[Unternehmenswert berechnen KMU 2026: EBIT-Multiple-Formel, Unternehmerlohn & Equity Value](https://dachdigitalwerk.github.io/unternehmenswert-berechnen-kmu-formel-ebit-multiple-2026.html)**
- ⚖️ **[Vereinfachtes Ertragswertverfahren (§§ 199–203 BewG): Kapitalisierungsfaktor 13,75 & Substanzwert](https://dachdigitalwerk.github.io/vereinfachtes-ertragswertverfahren-bewg-kapitalisierungsfaktor-13-75.html)**
- 🇨🇭 **[Praktikermethode Schweiz (ESTV KS 28) & KFS/BW 1 Österreich: Steuerwert-Formel & Ertragswert](https://dachdigitalwerk.github.io/praktikermethode-schweiz-unternehmensbewertung-steuerwert-formel.html)**
- 🏠 **[DACH Digitalwerk – Alle 34 Self-Serve Web-Tools im Überblick](https://dachdigitalwerk.github.io/)**

---

## ✨ Kernfunktionen

1. **M&A Branchen-EBIT-Multiple (Enterprise Value → Equity Value):**
   - Bereinigt das EBIT um den kalkulatorischen Geschäftsführer-/Unternehmerlohn, multipliziert mit dem Branchen-Multiple (SaaS, Industrie, Handwerk, Handel, Agentur) und überführt den Enterprise Value mittels Liquider Mittel (+ Cash) und Finanzschulden (- Debt) in den **Equity Value (Kaufpreis für 100 % der Anteile)**.
2. **Vereinfachtes Ertragswertverfahren nach §§ 199–203 BewG (DE):**
   - Pauschalsteuerabzug 30 % (§ 202 Abs. 3 BewG), gesetzlicher Kapitalisierungsfaktor **13,75** (§ 203 Abs. 1 BewG) und Substanzwert-Mindestwertprüfung (§ 200 Abs. 3 BewG).
3. **KFS/BW 1 Ertragswert (AT) & ESTV KS 28 Praktikermethode (CH):**
   - Ewige Rente nach KÖSt (23 % in AT) bzw. gewichtete Schweizer Praktikermethode `(2 × Ertragswert + 1 × Substanzwert) / 3`.

---

## 📦 Installation & CLI-Nutzung

```bash
pip install -e .
dach-valuation --country DE --revenue 3500000 --ebit 520000 --owner-salary 120000 --multiple 5.8 --cash 280000 --debt 450000
```

---

## ⚠️ Rechtlicher Hinweis (§ 2 RDG / § 5 StBerG / § 43 WPO)

Dieses Paket dient ausschließlich der unverbindlichen finanzmathematischen Orientierung. Es stellt kein Wirtschaftsprüfungsgutachten nach IDW S1 oder KFS/BW 1 sowie keine Steuer-, Rechts- oder M&A-Beratung dar.
