"""Datenschutzrechtliche Prüfung nach Schritt 3 der Checkliste `dsgvo-ai-act-checkliste.md`.

Dieses Modul bildet die dort aufgeführten Prüfpunkte (Art. 6, 9, 13/14, 22, 28,
35 und 44 ff. DSGVO) als ausführbare Logik ab. Es liefert zu jedem Prüfpunkt
einen Status (erfüllt / offen / nicht einschlägig) sowie eine Einschätzung zur
Pflicht einer Datenschutz-Folgenabschätzung nach Art. 35 DSGVO. Diese
Einschätzung ist eine Heuristik im Sinne der in der Checkliste genannten
Regelbeispiele (umfangreiche Verarbeitung, systematische Überwachung) und
ersetzt nicht die vollständige Prüfung nach Art. 35 Abs. 3 DSGVO und der
"Muss-Liste" der zuständigen Aufsichtsbehörde.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DSGVOEingabe:
    """Angaben zu Schritt 3 der Checkliste.

    `verarbeitet_personenbezogene_daten` ist die Weiche aus Schritt 1: Wird sie
    verneint, entfällt der gesamte übrige Abschnitt, wie in der Checkliste
    vermerkt ("Schritt 3 entfällt dann größtenteils").
    """

    verarbeitet_personenbezogene_daten: bool
    rechtsgrundlage: str | None = None
    besondere_kategorien_betroffen: bool = False
    besondere_kategorien_ausnahme_vorhanden: bool = False
    auftragsverarbeitungsvertrag_vorhanden: bool = False
    drittlanduebermittlung: bool = False
    drittland_uebermittlungsgrundlage_vorhanden: bool = False
    informationspflicht_erfuellt: bool = False
    automatisierte_entscheidung_rechtliche_wirkung: bool = False
    umfangreiche_verarbeitung_oder_systematische_ueberwachung: bool = False
    loeschfristen_festgelegt: bool = False


@dataclass
class DSGVOPruefpunkt:
    """Ein einzelner Prüfpunkt mit Status."""

    artikel: str
    aussage: str
    status: str  # "erfüllt" | "offen" | "nicht einschlägig"


@dataclass
class DSGVOErgebnis:
    """Ergebnis der datenschutzrechtlichen Prüfung."""

    einschlaegig: bool
    pruefpunkte: list[DSGVOPruefpunkt]
    dsfa_erforderlich: bool
    dsfa_begruendung: str
    offene_punkte: list[str]


def pruefe(eingabe: DSGVOEingabe) -> DSGVOErgebnis:
    if not eingabe.verarbeitet_personenbezogene_daten:
        return DSGVOErgebnis(
            einschlaegig=False,
            pruefpunkte=[],
            dsfa_erforderlich=False,
            dsfa_begruendung=(
                "Es werden keine personenbezogenen Daten verarbeitet; die DSGVO ist auf diese Nutzung "
                "nicht anwendbar."
            ),
            offene_punkte=[],
        )

    pruefpunkte: list[DSGVOPruefpunkt] = []
    offene_punkte: list[str] = []

    if eingabe.rechtsgrundlage:
        pruefpunkte.append(
            DSGVOPruefpunkt(
                artikel="Art. 6 Abs. 1 DSGVO",
                aussage=f"Rechtsgrundlage der Verarbeitung: {eingabe.rechtsgrundlage}.",
                status="erfüllt",
            )
        )
    else:
        pruefpunkte.append(
            DSGVOPruefpunkt(
                artikel="Art. 6 Abs. 1 DSGVO",
                aussage="Es ist noch keine Rechtsgrundlage der Verarbeitung bestimmt.",
                status="offen",
            )
        )
        offene_punkte.append("Rechtsgrundlage der Verarbeitung nach Art. 6 Abs. 1 DSGVO festlegen.")

    if eingabe.besondere_kategorien_betroffen:
        if eingabe.besondere_kategorien_ausnahme_vorhanden:
            pruefpunkte.append(
                DSGVOPruefpunkt(
                    artikel="Art. 9 DSGVO",
                    aussage=(
                        "Es werden besondere Kategorien personenbezogener Daten verarbeitet; eine Ausnahme "
                        "nach Art. 9 Abs. 2 DSGVO liegt vor."
                    ),
                    status="erfüllt",
                )
            )
        else:
            pruefpunkte.append(
                DSGVOPruefpunkt(
                    artikel="Art. 9 DSGVO",
                    aussage=(
                        "Es werden besondere Kategorien personenbezogener Daten verarbeitet, ohne dass eine "
                        "Ausnahme nach Art. 9 Abs. 2 DSGVO belegt ist."
                    ),
                    status="offen",
                )
            )
            offene_punkte.append(
                "Ausnahme nach Art. 9 Abs. 2 DSGVO klären, bevor besondere Kategorien personenbezogener Daten verarbeitet werden."
            )
    else:
        pruefpunkte.append(
            DSGVOPruefpunkt(
                artikel="Art. 9 DSGVO",
                aussage="Es sind keine besonderen Kategorien personenbezogener Daten betroffen.",
                status="nicht einschlägig",
            )
        )

    if eingabe.auftragsverarbeitungsvertrag_vorhanden:
        pruefpunkte.append(
            DSGVOPruefpunkt(
                artikel="Art. 28 DSGVO",
                aussage="Mit dem Anbieter besteht ein Vertrag zur Auftragsverarbeitung.",
                status="erfüllt",
            )
        )
    else:
        pruefpunkte.append(
            DSGVOPruefpunkt(
                artikel="Art. 28 DSGVO",
                aussage="Mit dem Anbieter besteht noch kein Vertrag zur Auftragsverarbeitung.",
                status="offen",
            )
        )
        offene_punkte.append("Vertrag zur Auftragsverarbeitung nach Art. 28 DSGVO abschließen.")

    if eingabe.drittlanduebermittlung:
        if eingabe.drittland_uebermittlungsgrundlage_vorhanden:
            pruefpunkte.append(
                DSGVOPruefpunkt(
                    artikel="Art. 44 ff. DSGVO",
                    aussage=(
                        "Es erfolgt eine Übermittlung in ein Drittland; eine Übermittlungsgrundlage "
                        "(Angemessenheitsbeschluss oder Standardvertragsklauseln) liegt vor."
                    ),
                    status="erfüllt",
                )
            )
        else:
            pruefpunkte.append(
                DSGVOPruefpunkt(
                    artikel="Art. 44 ff. DSGVO",
                    aussage=(
                        "Es erfolgt eine Übermittlung in ein Drittland, ohne dass eine Übermittlungsgrundlage "
                        "belegt ist."
                    ),
                    status="offen",
                )
            )
            offene_punkte.append("Übermittlungsgrundlage für die Drittlandübermittlung nach Art. 44 ff. DSGVO klären.")
    else:
        pruefpunkte.append(
            DSGVOPruefpunkt(
                artikel="Art. 44 ff. DSGVO",
                aussage="Es findet keine Übermittlung personenbezogener Daten in ein Drittland statt.",
                status="nicht einschlägig",
            )
        )

    if eingabe.informationspflicht_erfuellt:
        pruefpunkte.append(
            DSGVOPruefpunkt(
                artikel="Art. 13/14 DSGVO",
                aussage="Es ist festgelegt, wie betroffene Personen über die Verarbeitung informiert werden.",
                status="erfüllt",
            )
        )
    else:
        pruefpunkte.append(
            DSGVOPruefpunkt(
                artikel="Art. 13/14 DSGVO",
                aussage="Es ist noch nicht festgelegt, wie betroffene Personen über die Verarbeitung informiert werden.",
                status="offen",
            )
        )
        offene_punkte.append("Information der betroffenen Personen nach Art. 13/14 DSGVO festlegen (z. B. in der Datenschutzerklärung).")

    if eingabe.automatisierte_entscheidung_rechtliche_wirkung:
        pruefpunkte.append(
            DSGVOPruefpunkt(
                artikel="Art. 22 DSGVO",
                aussage=(
                    "Es liegt eine automatisierte Entscheidung mit rechtlicher oder ähnlich bedeutsamer "
                    "Wirkung vor; die zusätzlichen Voraussetzungen des Art. 22 DSGVO sind zu prüfen."
                ),
                status="offen",
            )
        )
        offene_punkte.append("Zulässigkeitsvoraussetzungen einer automatisierten Entscheidung nach Art. 22 DSGVO prüfen.")
    else:
        pruefpunkte.append(
            DSGVOPruefpunkt(
                artikel="Art. 22 DSGVO",
                aussage="Es liegt keine automatisierte Entscheidung mit rechtlicher oder ähnlich bedeutsamer Wirkung vor.",
                status="nicht einschlägig",
            )
        )

    if eingabe.loeschfristen_festgelegt:
        pruefpunkte.append(
            DSGVOPruefpunkt(
                artikel="Art. 5 Abs. 1 lit. e DSGVO",
                aussage="Löschfristen für die verarbeiteten Daten sind festgelegt.",
                status="erfüllt",
            )
        )
    else:
        pruefpunkte.append(
            DSGVOPruefpunkt(
                artikel="Art. 5 Abs. 1 lit. e DSGVO",
                aussage="Löschfristen für die verarbeiteten Daten sind noch nicht festgelegt.",
                status="offen",
            )
        )
        offene_punkte.append("Löschfristen für die verarbeiteten bzw. eingegebenen Daten festlegen.")

    dsfa_gruende: list[str] = []
    if eingabe.besondere_kategorien_betroffen and eingabe.umfangreiche_verarbeitung_oder_systematische_ueberwachung:
        dsfa_gruende.append("umfangreiche Verarbeitung besonderer Kategorien personenbezogener Daten")
    if eingabe.automatisierte_entscheidung_rechtliche_wirkung:
        dsfa_gruende.append("automatisierte Entscheidung mit rechtlicher oder ähnlich bedeutsamer Wirkung")
    if eingabe.umfangreiche_verarbeitung_oder_systematische_ueberwachung and not eingabe.besondere_kategorien_betroffen:
        dsfa_gruende.append("umfangreiche Verarbeitung bzw. systematische Überwachung")

    dsfa_erforderlich = bool(dsfa_gruende)
    if dsfa_erforderlich:
        dsfa_begruendung = (
            "Eine Datenschutz-Folgenabschätzung nach Art. 35 DSGVO erscheint erforderlich, da folgende "
            "Anhaltspunkte vorliegen: " + "; ".join(dsfa_gruende) + ". Diese Einschätzung ist eine Heuristik "
            "und ersetzt nicht die vollständige Prüfung nach Art. 35 Abs. 3 DSGVO und der Muss-Liste der "
            "zuständigen Aufsichtsbehörde."
        )
    else:
        dsfa_begruendung = (
            "Nach den vorliegenden Angaben ergibt sich kein Anhaltspunkt für eine Pflicht zur "
            "Datenschutz-Folgenabschätzung nach Art. 35 DSGVO. Diese Einschätzung ist schriftlich "
            "festzuhalten, damit sie im Fall einer späteren Ausweitung der Verarbeitung erneut geprüft "
            "werden kann."
        )

    return DSGVOErgebnis(
        einschlaegig=True,
        pruefpunkte=pruefpunkte,
        dsfa_erforderlich=dsfa_erforderlich,
        dsfa_begruendung=dsfa_begruendung,
        offene_punkte=offene_punkte,
    )
