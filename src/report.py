"""Erzeugung des Einschätzungsberichts als Markdown-Dokument.

Der erzeugte Bericht folgt bewusst dem Aufbau der Checkliste
`dsgvo-ai-act-checkliste.md` aus dem Repository eu-ai-act-dsgvo-compliance-framework,
damit ein mit diesem Werkzeug erstellter Bericht unmittelbar als Nachweis im
Sinne von Schritt 4 der Checkliste abgelegt werden kann.
"""

from __future__ import annotations

from datetime import datetime

from .ai_act_classifier import AIActErgebnis
from .dsgvo_check import DSGVOErgebnis

_STATUS_ZEICHEN = {"erfüllt": "☑", "offen": "☐", "nicht einschlägig": "–"}


def erzeuge_bericht(
    systembezeichnung: str,
    ai_act_ergebnis: AIActErgebnis,
    dsgvo_ergebnis: DSGVOErgebnis,
    zusaetzliche_offene_punkte: list[str] | None = None,
    erstellt_am: datetime | None = None,
) -> str:
    """Baut den vollständigen Bericht als Markdown-Text zusammen.

    `zusaetzliche_offene_punkte` nimmt Punkte auf, die nicht aus der
    DSGVO-Prüfung stammen, insbesondere die organisatorischen Pflichten aus
    Art. 4 AI Act (`pruefe_ki_kompetenz`).
    """

    zeitstempel = (erstellt_am or datetime.now()).strftime("%d.%m.%Y %H:%M")
    zeilen: list[str] = []

    titel = systembezeichnung.strip() if systembezeichnung and systembezeichnung.strip() else "[Systembezeichnung]"
    zeilen.append(f"# Einschätzungsbericht: {titel}")
    zeilen.append("")
    zeilen.append(f"Erstellt am {zeitstempel} mit dem Automatisierten AI-Governance-Analyzer.")
    zeilen.append("")
    zeilen.append(
        "Dieser Bericht fasst die Einordnung anhand der Checkliste `dsgvo-ai-act-checkliste.md` "
        "zusammen und dient als Arbeitsgrundlage für die Dokumentation nach Schritt 4 dieser Checkliste. "
        "Er ersetzt keine Rechtsberatung im Einzelfall."
    )
    zeilen.append("")
    zeilen.append("## Einordnung nach dem AI Act")
    zeilen.append("")
    zeilen.append(f"**Ergebnis: {ai_act_ergebnis.stufe.value}**")
    zeilen.append("")
    zeilen.append(ai_act_ergebnis.hinweis)
    zeilen.append("")
    zeilen.append("### Begründungspfad")
    zeilen.append("")
    for schritt in ai_act_ergebnis.begruendung:
        markierung = "☑" if schritt.ausgeloest else "☐"
        zeilen.append(f"- {markierung} **{schritt.artikel}** — {schritt.aussage}")
    zeilen.append("")

    zeilen.append("## Datenschutzrechtliche Prüfung")
    zeilen.append("")
    if dsgvo_ergebnis.einschlaegig:
        for punkt in dsgvo_ergebnis.pruefpunkte:
            markierung = _STATUS_ZEICHEN[punkt.status]
            zeilen.append(f"- {markierung} **{punkt.artikel}** ({punkt.status}) — {punkt.aussage}")
        zeilen.append("")
        zeilen.append("### Datenschutz-Folgenabschätzung (Art. 35 DSGVO)")
        zeilen.append("")
        zeilen.append(dsgvo_ergebnis.dsfa_begruendung)
    else:
        zeilen.append(dsgvo_ergebnis.dsfa_begruendung)
    zeilen.append("")

    alle_offenen_punkte = list(dsgvo_ergebnis.offene_punkte) + list(zusaetzliche_offene_punkte or [])
    if alle_offenen_punkte:
        zeilen.append("## Offene Punkte")
        zeilen.append("")
        for punkt in alle_offenen_punkte:
            zeilen.append(f"- {punkt}")
        zeilen.append("")

    zeilen.append("---")
    zeilen.append("")
    zeilen.append(
        "Freigabe durch die Datenschutzbeauftragte bzw. den Datenschutzbeauftragten erforderlich, bevor "
        "das System auf Grundlage dieses Berichts in Betrieb genommen wird."
    )

    return "\n".join(zeilen)
