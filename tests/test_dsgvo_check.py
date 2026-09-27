from src.dsgvo_check import DSGVOEingabe, pruefe


def test_ohne_personenbezogene_daten_ist_pruefung_nicht_einschlaegig():
    ergebnis = pruefe(DSGVOEingabe(verarbeitet_personenbezogene_daten=False))
    assert ergebnis.einschlaegig is False
    assert ergebnis.pruefpunkte == []
    assert ergebnis.dsfa_erforderlich is False
    assert ergebnis.offene_punkte == []


def test_alle_anforderungen_erfuellt_hat_keine_offenen_punkte():
    eingabe = DSGVOEingabe(
        verarbeitet_personenbezogene_daten=True,
        rechtsgrundlage="Art. 6 Abs. 1 lit. b DSGVO (Vertragserfüllung)",
        besondere_kategorien_betroffen=False,
        auftragsverarbeitungsvertrag_vorhanden=True,
        drittlanduebermittlung=False,
        informationspflicht_erfuellt=True,
        automatisierte_entscheidung_rechtliche_wirkung=False,
        umfangreiche_verarbeitung_oder_systematische_ueberwachung=False,
        loeschfristen_festgelegt=True,
    )
    ergebnis = pruefe(eingabe)
    assert ergebnis.einschlaegig is True
    assert ergebnis.offene_punkte == []
    assert ergebnis.dsfa_erforderlich is False


def test_fehlende_rechtsgrundlage_erzeugt_offenen_punkt():
    ergebnis = pruefe(DSGVOEingabe(verarbeitet_personenbezogene_daten=True))
    rechtsgrundlage_punkt = next(p for p in ergebnis.pruefpunkte if p.artikel == "Art. 6 Abs. 1 DSGVO")
    assert rechtsgrundlage_punkt.status == "offen"
    assert any("Rechtsgrundlage" in punkt for punkt in ergebnis.offene_punkte)


def test_besondere_kategorien_ohne_ausnahme_erzeugt_offenen_punkt():
    eingabe = DSGVOEingabe(
        verarbeitet_personenbezogene_daten=True,
        besondere_kategorien_betroffen=True,
        besondere_kategorien_ausnahme_vorhanden=False,
    )
    ergebnis = pruefe(eingabe)
    art9_punkt = next(p for p in ergebnis.pruefpunkte if p.artikel == "Art. 9 DSGVO")
    assert art9_punkt.status == "offen"
    assert any("Art. 9 Abs. 2 DSGVO" in punkt for punkt in ergebnis.offene_punkte)


def test_besondere_kategorien_ohne_verarbeitung_ist_nicht_einschlaegig():
    eingabe = DSGVOEingabe(
        verarbeitet_personenbezogene_daten=True,
        besondere_kategorien_betroffen=False,
    )
    ergebnis = pruefe(eingabe)
    art9_punkt = next(p for p in ergebnis.pruefpunkte if p.artikel == "Art. 9 DSGVO")
    assert art9_punkt.status == "nicht einschlägig"


def test_drittlanduebermittlung_ohne_grundlage_erzeugt_offenen_punkt():
    eingabe = DSGVOEingabe(
        verarbeitet_personenbezogene_daten=True,
        drittlanduebermittlung=True,
        drittland_uebermittlungsgrundlage_vorhanden=False,
    )
    ergebnis = pruefe(eingabe)
    drittland_punkt = next(p for p in ergebnis.pruefpunkte if p.artikel == "Art. 44 ff. DSGVO")
    assert drittland_punkt.status == "offen"
    assert any("Übermittlungsgrundlage" in punkt for punkt in ergebnis.offene_punkte)


def test_dsfa_erforderlich_bei_automatisierter_entscheidung():
    eingabe = DSGVOEingabe(
        verarbeitet_personenbezogene_daten=True,
        automatisierte_entscheidung_rechtliche_wirkung=True,
    )
    ergebnis = pruefe(eingabe)
    assert ergebnis.dsfa_erforderlich is True
    assert "Art. 35" in ergebnis.dsfa_begruendung


def test_dsfa_erforderlich_bei_umfangreicher_verarbeitung_besonderer_kategorien():
    eingabe = DSGVOEingabe(
        verarbeitet_personenbezogene_daten=True,
        besondere_kategorien_betroffen=True,
        besondere_kategorien_ausnahme_vorhanden=True,
        umfangreiche_verarbeitung_oder_systematische_ueberwachung=True,
    )
    ergebnis = pruefe(eingabe)
    assert ergebnis.dsfa_erforderlich is True


def test_dsfa_nicht_erforderlich_im_normalfall():
    eingabe = DSGVOEingabe(
        verarbeitet_personenbezogene_daten=True,
        rechtsgrundlage="Art. 6 Abs. 1 lit. b DSGVO (Vertragserfüllung)",
    )
    ergebnis = pruefe(eingabe)
    assert ergebnis.dsfa_erforderlich is False
