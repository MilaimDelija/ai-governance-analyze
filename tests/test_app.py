"""Smoke- und Verhaltenstests für die Streamlit-Oberfläche (app.py).

Diese Tests laufen ohne Browser über Streamlits eigenes Testwerkzeug
(`streamlit.testing.v1.AppTest`), das die App headless ausführt und die
gerenderten Elemente sowie deren Werte zur Prüfung bereitstellt.
"""

from pathlib import Path

from streamlit.testing.v1 import AppTest

_APP_PFAD = Path(__file__).resolve().parent.parent / "app.py"


def _app() -> AppTest:
    at = AppTest.from_file(str(_APP_PFAD))
    at.run()
    assert not at.exception
    return at


_STUFEN_SYMBOLE = ("🔴", "🟠", "🟡", "🟢")


def _ergebnis_subheader(at: AppTest) -> str:
    # Die Ergebnis-Zeile ist die einzige Subheader-Zeile, die mit einem der
    # Stufen-Symbole beginnt; alle übrigen Subheader sind Abschnittstitel.
    return next(h.value for h in at.subheader if h.value.strip().startswith(_STUFEN_SYMBOLE))


def test_app_startet_ohne_fehler_und_zeigt_minimales_risiko_als_standard():
    at = _app()
    assert "Minimales Risiko" in _ergebnis_subheader(at)


def test_social_scoring_checkbox_fuehrt_zu_verboten():
    at = _app()
    checkbox = next(cb for cb in at.checkbox if "Social Scoring" in cb.label)
    checkbox.check()
    at.run()
    assert "Verboten" in _ergebnis_subheader(at)


def test_bewerberauswahl_checkbox_fuehrt_zu_hochrisiko():
    at = _app()
    checkbox = next(cb for cb in at.checkbox if "wählt Bewerbungen automatisiert vor" in cb.label)
    checkbox.check()
    at.run()
    assert "Hochrisiko" in _ergebnis_subheader(at)


def test_chatbot_checkbox_fuehrt_zu_transparenzpflicht():
    at = _app()
    checkbox = next(cb for cb in at.checkbox if "Chatbot oder Sprachassistent" in cb.label)
    checkbox.check()
    at.run()
    assert "Transparenzpflicht" in _ergebnis_subheader(at)


def test_personenbezogene_daten_checkbox_blendet_schritt_3_ein():
    at = _app()
    checkbox = next(cb for cb in at.checkbox if "verarbeitet personenbezogene Daten" in cb.label)
    checkbox.check()
    at.run()
    ueberschriften = [h.value for h in at.header]
    assert any("Datenschutzrechtliche Prüfung" in h for h in ueberschriften)


def test_download_button_fuer_bericht_ist_vorhanden():
    at = _app()
    assert any("Bericht als Markdown herunterladen" in db.label for db in at.download_button)
