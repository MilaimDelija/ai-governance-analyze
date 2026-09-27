from src.ai_act_classifier import (
    AIActEingabe,
    AIActRisikostufe,
    HochrisikoEingabe,
    KIKompetenzEingabe,
    TransparenzEingabe,
    VerbotenePraktikenEingabe,
    klassifiziere,
    pruefe_ki_kompetenz,
)


def test_minimales_risiko_wenn_keine_kriterien_zutreffen():
    ergebnis = klassifiziere(AIActEingabe())
    assert ergebnis.stufe is AIActRisikostufe.MINIMAL
    assert all(not schritt.ausgeloest for schritt in ergebnis.begruendung)
    # Alle drei Abschnitte (5 + 4 + 3 Prüfpunkte) müssen durchlaufen worden sein.
    assert len(ergebnis.begruendung) == 12


def test_verboten_bei_social_scoring():
    eingabe = AIActEingabe(
        verbotene_praktiken=VerbotenePraktikenEingabe(social_scoring=True)
    )
    ergebnis = klassifiziere(eingabe)
    assert ergebnis.stufe is AIActRisikostufe.VERBOTEN
    artikel_mit_treffer = [s.artikel for s in ergebnis.begruendung if s.ausgeloest]
    assert artikel_mit_treffer == ["Art. 5 Abs. 1 lit. c AI Act"]


def test_verbot_hat_vorrang_und_bricht_pruefung_ab():
    eingabe = AIActEingabe(
        verbotene_praktiken=VerbotenePraktikenEingabe(unterschwellige_beeinflussung=True),
        hochrisiko=HochrisikoEingabe(bewerberauswahl=True),
    )
    ergebnis = klassifiziere(eingabe)
    assert ergebnis.stufe is AIActRisikostufe.VERBOTEN
    # Die Hochrisiko-Prüfpunkte wurden nicht mehr ausgewertet, da die Prüfung
    # laut Checkliste an dieser Stelle endet.
    geprueft_artikel = [s.artikel for s in ergebnis.begruendung]
    assert "Anhang III Nr. 4 lit. a AI Act" not in geprueft_artikel


def test_hochrisiko_bei_bewerberauswahl():
    eingabe = AIActEingabe(hochrisiko=HochrisikoEingabe(bewerberauswahl=True))
    ergebnis = klassifiziere(eingabe)
    assert ergebnis.stufe is AIActRisikostufe.HOCHRISIKO
    artikel_mit_treffer = [s.artikel for s in ergebnis.begruendung if s.ausgeloest]
    assert artikel_mit_treffer == ["Anhang III Nr. 4 lit. a AI Act"]


def test_hochrisiko_hat_vorrang_vor_transparenzpflicht():
    eingabe = AIActEingabe(
        hochrisiko=HochrisikoEingabe(kreditwuerdigkeitspruefung=True),
        transparenz=TransparenzEingabe(direkte_interaktion=True),
    )
    ergebnis = klassifiziere(eingabe)
    assert ergebnis.stufe is AIActRisikostufe.HOCHRISIKO
    geprueft_artikel = [s.artikel for s in ergebnis.begruendung]
    assert "Art. 50 Abs. 1 AI Act" not in geprueft_artikel


def test_transparenzpflicht_bei_chatbot():
    eingabe = AIActEingabe(transparenz=TransparenzEingabe(direkte_interaktion=True))
    ergebnis = klassifiziere(eingabe)
    assert ergebnis.stufe is AIActRisikostufe.TRANSPARENZPFLICHT
    artikel_mit_treffer = [s.artikel for s in ergebnis.begruendung if s.ausgeloest]
    assert artikel_mit_treffer == ["Art. 50 Abs. 1 AI Act"]


def test_transparenzpflicht_bei_deepfake_zeigt_korrekten_artikel():
    eingabe = AIActEingabe(transparenz=TransparenzEingabe(deepfake_erzeugung=True))
    ergebnis = klassifiziere(eingabe)
    assert ergebnis.stufe is AIActRisikostufe.TRANSPARENZPFLICHT
    artikel_mit_treffer = [s.artikel for s in ergebnis.begruendung if s.ausgeloest]
    assert artikel_mit_treffer == ["Art. 50 Abs. 4 AI Act"]


def test_ki_kompetenz_listet_alle_offenen_punkte_wenn_nichts_erfuellt():
    offene_punkte = pruefe_ki_kompetenz(KIKompetenzEingabe())
    assert len(offene_punkte) == 3


def test_ki_kompetenz_keine_offenen_punkte_wenn_alles_erfuellt():
    eingabe = KIKompetenzEingabe(
        richtlinie_bekannt=True, einweisung_erfolgt=True, teilnahme_dokumentiert=True
    )
    assert pruefe_ki_kompetenz(eingabe) == []
