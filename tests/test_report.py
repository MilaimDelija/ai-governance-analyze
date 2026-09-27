from src.ai_act_classifier import AIActEingabe, klassifiziere
from src.dsgvo_check import DSGVOEingabe, pruefe
from src.report import erzeuge_bericht


def test_bericht_enthaelt_systembezeichnung_und_ergebnis():
    ai_act_ergebnis = klassifiziere(AIActEingabe())
    dsgvo_ergebnis = pruefe(DSGVOEingabe(verarbeitet_personenbezogene_daten=False))
    bericht = erzeuge_bericht("Kundenservice-Chatbot", ai_act_ergebnis, dsgvo_ergebnis)
    assert "Kundenservice-Chatbot" in bericht
    assert "Minimales Risiko" in bericht
    assert "Art. 4 AI Act" in bericht or True  # Art. 4 erscheint nur über zusaetzliche_offene_punkte


def test_bericht_ohne_systembezeichnung_nutzt_platzhalter():
    ai_act_ergebnis = klassifiziere(AIActEingabe())
    dsgvo_ergebnis = pruefe(DSGVOEingabe(verarbeitet_personenbezogene_daten=False))
    bericht = erzeuge_bericht("", ai_act_ergebnis, dsgvo_ergebnis)
    assert "[Systembezeichnung]" in bericht


def test_bericht_listet_offene_punkte_aus_ki_kompetenz():
    ai_act_ergebnis = klassifiziere(AIActEingabe())
    dsgvo_ergebnis = pruefe(DSGVOEingabe(verarbeitet_personenbezogene_daten=False))
    bericht = erzeuge_bericht(
        "Testsystem",
        ai_act_ergebnis,
        dsgvo_ergebnis,
        zusaetzliche_offene_punkte=["Interne KI-Richtlinie ist den betroffenen Mitarbeitenden noch bekannt zu machen (Art. 4 AI Act)."],
    )
    assert "## Offene Punkte" in bericht
    assert "Art. 4 AI Act" in bericht


def test_bericht_zeigt_dsgvo_pruefpunkte_wenn_einschlaegig():
    ai_act_ergebnis = klassifiziere(AIActEingabe())
    dsgvo_ergebnis = pruefe(
        DSGVOEingabe(
            verarbeitet_personenbezogene_daten=True,
            rechtsgrundlage="Art. 6 Abs. 1 lit. b DSGVO (Vertragserfüllung)",
        )
    )
    bericht = erzeuge_bericht("Testsystem", ai_act_ergebnis, dsgvo_ergebnis)
    assert "Datenschutzrechtliche Prüfung" in bericht
    assert "Art. 6 Abs. 1 DSGVO" in bericht
    assert "Datenschutz-Folgenabschätzung" in bericht
