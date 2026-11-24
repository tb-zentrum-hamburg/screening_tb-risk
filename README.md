# TB-Screening nach § 36 IfSG – Entscheidungshilfen (allgemeine Fassung)

Interaktive Entscheidungshilfen für das risikoadaptierte TB-Screening neu zugewanderter Personen nach S3-Leitlinie TB-Risk 2025 (AWMF 020-029), neutral gestaltet und ohne Standortbezug, anwendbar für alle Gesundheitsämter und ärztlichen Praxen. Statische Seiten ohne Server, ohne Datenerhebung.

**Privates Projekt, ohne Gewähr.** Bei Fragen, Fehlermeldungen und Änderungswünschen: christian.schwarzbach@hamburg-mitte.hamburg.de.

Eigenständiges Projekt, parallel zur Hamburger Fassung (Repository `tb-zentrum-hamburg/screening`). Fachliche Änderungen betreffen häufig beide Fassungen und werden in beiden mit eigener Version nachgeführt.

| Datei | Inhalt | Version | Stand |
|---|---|---|---|
| `index.html` | Auswahlseite | 1.5 | 24.11.2026 |
| `ifsg36.html` | Untersuchung nach § 36 IfSG mit Wahl der Personengruppe (allgemein, Aufnahme-/Ankunftseinrichtung, UMA) | 1.6 | 24.11.2026 |
| `praxis.html` | Freiwilliges Screening ohne Indikation nach § 36 IfSG (Haus-, Betriebs- und weitere Ärzt(inn)en) | 1.6 | 24.11.2026 |

Fachliche Arbeitsversionen, keine automatisierte Diagnose, keine rechtsverbindliche Freigabe. Änderungsverlauf jeweils in der Seite.

## Länderdaten (Inzidenz, MDR/RR)

Die Seiten enthalten eine eingebettete Tabelle und den Knopf „Daten aktualisieren“. Er lädt `daten.json` von derselben Adresse und zeigt vor der Übernahme eine Änderungsliste (Hinweis, wenn sich die Einstufung Inzidenz > 100/100.000 oder MDR > 10 % ändert); die Übernahme gilt nur für die laufende Sitzung. `daten.json` pflegt die GitHub-Aktion `.github/workflows/daten.yml` (monatlich oder manuell) mit `tools/update_daten.py` aus den WHO-TB-Schätzungen (`e_inc_100k`, `e_rr_pct_new`). Fixwerte in `tools/pins.json` (derzeit keine) werden nie überschrieben; `tools/laender.json` ordnet Ländernamen ISO-Codes zu. `tools/patch_knopf.py` fügt den Knopf ein. Die eingebettete Tabelle wird nicht automatisch aktualisiert.

## Veröffentlichung

GitHub Pages: Branch `main`, Ordner `/` (Root). Lokal genügt das Öffnen von `index.html` im Browser.

## Versionspflege

Bei jeder Änderung die Versionsnummer anheben, den Änderungsverlauf in der Seite ergänzen und die Tabelle oben sowie die Versionsangaben in `index.html` anpassen.
