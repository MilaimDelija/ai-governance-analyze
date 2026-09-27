"""Automatisierter AI-Governance-Analyzer.

Interaktive Oberfläche, die ein geplantes KI-System anhand der vier Schritte
aus der Checkliste `dsgvo-ai-act-checkliste.md` (Repository
eu-ai-act-dsgvo-compliance-framework) einordnet: Systeminventar, Einordnung
nach dem AI Act, datenschutzrechtliche Prüfung und Dokumentation. Jedes
Ergebnis wird zusammen mit dem zugrunde liegenden Begründungspfad angezeigt,
und die vollständige Einschätzung lässt sich als Markdown-Bericht
herunterladen.
"""

from __future__ import annotations

import streamlit as st

from src.ai_act_classifier import (
    AIActEingabe,
    HochrisikoEingabe,
    KIKompetenzEingabe,
    TransparenzEingabe,
    VerbotenePraktikenEingabe,
    klassifiziere,
    pruefe_ki_kompetenz,
)
from src.dsgvo_check import DSGVOEingabe, pruefe as dsgvo_pruefe
from src.report import erzeuge_bericht

st.set_page_config(page_title="AI-Governance-Analyzer", page_icon="⚖️", layout="wide")

STUFEN_SYMBOL = {
    "Verboten": "🔴",
    "Hochrisiko": "🟠",
    "Transparenzpflicht (Art. 50 AI Act)": "🟡",
    "Minimales Risiko": "🟢",
}
STATUS_SYMBOL = {"erfüllt": "☑", "offen": "☐", "nicht einschlägig": "–"}

st.title("Automatisierter AI-Governance-Analyzer")
st.caption(
    "Ordnet ein geplantes KI-System nach der Verordnung (EU) 2024/1689 (AI Act) und der DSGVO ein, "
    "ausgehend von der Checkliste `dsgvo-ai-act-checkliste.md` aus dem Repository "
    "eu-ai-act-dsgvo-compliance-framework."
)

with st.expander("Hinweis zur Verwendung"):
    st.write(
        "Dieses Werkzeug bildet die vier Prüfschritte der Checkliste als ausführbare Logik ab und zeigt "
        "zu jedem Ergebnis den zugrunde liegenden Begründungspfad mit den jeweils einschlägigen Artikeln. "
        "Es ersetzt keine Rechtsberatung im Einzelfall; insbesondere die endgültige Einordnung als "
        "Hochrisiko-System, die Erforderlichkeit einer Datenschutz-Folgenabschätzung und die Wirksamkeit "
        "einer konkreten Übermittlungsgrundlage in ein Drittland hängen von Umständen ab, die nur im "
        "jeweiligen Einzelfall geprüft werden können."
    )

st.header("Schritt 1 — Systeminventar")

spalte_links, spalte_rechts = st.columns(2)
with spalte_links:
    systemname = st.text_input("Name des Systems")
    anbieter = st.text_input("Anbieter")
with spalte_rechts:
    abteilung = st.text_input("Betroffene Abteilung(en)")
    integrationsform = st.radio(
        "Nutzungsform",
        ("Fertiges Produkt (z. B. Weboberfläche)", "Integration in eigene Anwendung (z. B. über API)"),
        horizontal=True,
    )

zweck = st.text_area("Zweck der geplanten Nutzung im Unternehmen", height=80)

verarbeitet_pbd = st.checkbox(
    "Das System verarbeitet personenbezogene Daten von Kunden, Beschäftigten oder Dritten."
)

st.divider()
st.header("Schritt 2 — Einordnung nach dem AI Act")

st.subheader("2.1 Verbotene Praktiken (Art. 5 AI Act)")
st.caption("Ankreuzen, wenn die Aussage auf das geplante System zutrifft.")
unterschwellig = st.checkbox(
    "Das System nutzt unterschwellige Techniken, die eine Person zu deren Schaden wesentlich beeinflussen können."
)
ausnutzung = st.checkbox(
    "Das System nutzt eine Schutzbedürftigkeit aufgrund von Alter, Behinderung oder sozialer bzw. wirtschaftlicher Lage aus."
)
social_scoring = st.checkbox(
    "Das System bewertet oder klassifiziert Personen anhand ihres sozialen Verhaltens mit nachteiliger Wirkung (Social Scoring)."
)
biometrisch = st.checkbox(
    "Das System leitet aus biometrischen Daten sensible Merkmale ab, etwa politische Meinung oder sexuelle Orientierung."
)
emotionserkennung = st.checkbox(
    "Das System erkennt Emotionen am Arbeitsplatz außerhalb der engen medizinischen oder sicherheitsbezogenen Ausnahmen."
)

st.subheader("2.2 Hochrisiko-Einstufung (Art. 6 i. V. m. Anhang III AI Act)")
bewerberauswahl = st.checkbox("Das System wählt Bewerbungen automatisiert vor, bewertet sie oder lehnt sie ab.")
beschaeftigtenbewertung = st.checkbox(
    "Das System bewertet Beschäftigte oder beeinflusst Entscheidungen über Beförderung oder Kündigung."
)
kreditwuerdigkeit = st.checkbox("Das System prüft die Kreditwürdigkeit oder Bonität natürlicher Personen.")
produktsicherheit = st.checkbox(
    "Das System ist Sicherheitsbauteil eines Produkts, das bereits einer produktrechtlichen Sicherheitsprüfung unterliegt."
)

st.subheader("2.3 Transparenzpflichten (Art. 50 AI Act)")
direkte_interaktion = st.checkbox(
    "Das System tritt gegenüber Kunden oder Dritten direkt in Erscheinung, etwa als Chatbot oder Sprachassistent."
)
synthetisch = st.checkbox("Das System erzeugt oder verändert Bild-, Audio- oder Videoinhalte, die authentisch wirken könnten.")
deepfake = st.checkbox("Das System erzeugt oder verändert Inhalte, die als Deepfake einzuordnen sind.")

st.subheader("2.4 KI-Kompetenz (Art. 4 AI Act)")
st.caption("Diese Pflicht gilt unabhängig von der Risikoeinstufung des Systems für jedes eingesetzte KI-System.")
richtlinie_bekannt = st.checkbox("Die betroffenen Mitarbeitenden haben die interne KI-Richtlinie zur Kenntnis genommen.")
einweisung_erfolgt = st.checkbox("Eine Einweisung in die konkreten Grenzen und Fehlerquellen des Systems hat stattgefunden.")
teilnahme_dokumentiert = st.checkbox("Die Teilnahme an der Einweisung ist dokumentiert.")

ai_act_eingabe = AIActEingabe(
    verbotene_praktiken=VerbotenePraktikenEingabe(
        unterschwellige_beeinflussung=unterschwellig,
        ausnutzung_schutzbeduerftigkeit=ausnutzung,
        social_scoring=social_scoring,
        biometrische_kategorisierung_sensibel=biometrisch,
        emotionserkennung_arbeitsplatz=emotionserkennung,
    ),
    hochrisiko=HochrisikoEingabe(
        bewerberauswahl=bewerberauswahl,
        beschaeftigtenbewertung=beschaeftigtenbewertung,
        kreditwuerdigkeitspruefung=kreditwuerdigkeit,
        produktsicherheitsrelevant=produktsicherheit,
    ),
    transparenz=TransparenzEingabe(
        direkte_interaktion=direkte_interaktion,
        synthetische_medieninhalte=synthetisch,
        deepfake_erzeugung=deepfake,
    ),
)
ai_act_ergebnis = klassifiziere(ai_act_eingabe)

ki_kompetenz_offene_punkte = pruefe_ki_kompetenz(
    KIKompetenzEingabe(
        richtlinie_bekannt=richtlinie_bekannt,
        einweisung_erfolgt=einweisung_erfolgt,
        teilnahme_dokumentiert=teilnahme_dokumentiert,
    )
)

st.divider()

if verarbeitet_pbd:
    st.header("Schritt 3 — Datenschutzrechtliche Prüfung")

    rechtsgrundlage = st.selectbox(
        "Rechtsgrundlage der Verarbeitung (Art. 6 Abs. 1 DSGVO)",
        (
            "",
            "Art. 6 Abs. 1 lit. a DSGVO (Einwilligung)",
            "Art. 6 Abs. 1 lit. b DSGVO (Vertragserfüllung bzw. vorvertragliche Maßnahme)",
            "Art. 6 Abs. 1 lit. c DSGVO (rechtliche Verpflichtung)",
            "Art. 6 Abs. 1 lit. e DSGVO (öffentliches Interesse)",
            "Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse)",
        ),
    )

    besondere_kategorien = st.checkbox("Es werden besondere Kategorien personenbezogener Daten nach Art. 9 DSGVO eingegeben.")
    besondere_kategorien_ausnahme = False
    if besondere_kategorien:
        besondere_kategorien_ausnahme = st.checkbox("Eine Ausnahme nach Art. 9 Abs. 2 DSGVO liegt vor.")

    avv_vorhanden = st.checkbox("Mit dem Anbieter besteht ein Vertrag zur Auftragsverarbeitung nach Art. 28 DSGVO.")

    drittland = st.checkbox("Es erfolgt eine Verarbeitung außerhalb des EWR (Drittlandübermittlung).")
    drittland_grundlage = False
    if drittland:
        drittland_grundlage = st.checkbox(
            "Eine Übermittlungsgrundlage (Angemessenheitsbeschluss oder Standardvertragsklauseln) liegt vor."
        )

    informationspflicht = st.checkbox(
        "Es ist festgelegt, wie betroffene Personen nach Art. 13/14 DSGVO über die Verarbeitung informiert werden."
    )

    automatisierte_entscheidung = st.checkbox(
        "Es liegt eine automatisierte Entscheidung mit rechtlicher oder ähnlich bedeutsamer Wirkung nach Art. 22 DSGVO vor."
    )

    umfangreiche_verarbeitung = st.checkbox(
        "Die Verarbeitung ist umfangreich oder erfolgt im Rahmen einer systematischen Überwachung."
    )

    loeschfristen = st.checkbox("Löschfristen für die verarbeiteten bzw. eingegebenen Daten sind festgelegt.")

    dsgvo_eingabe = DSGVOEingabe(
        verarbeitet_personenbezogene_daten=True,
        rechtsgrundlage=rechtsgrundlage or None,
        besondere_kategorien_betroffen=besondere_kategorien,
        besondere_kategorien_ausnahme_vorhanden=besondere_kategorien_ausnahme,
        auftragsverarbeitungsvertrag_vorhanden=avv_vorhanden,
        drittlanduebermittlung=drittland,
        drittland_uebermittlungsgrundlage_vorhanden=drittland_grundlage,
        informationspflicht_erfuellt=informationspflicht,
        automatisierte_entscheidung_rechtliche_wirkung=automatisierte_entscheidung,
        umfangreiche_verarbeitung_oder_systematische_ueberwachung=umfangreiche_verarbeitung,
        loeschfristen_festgelegt=loeschfristen,
    )
    dsgvo_ergebnis = dsgvo_pruefe(dsgvo_eingabe)
    st.divider()
else:
    dsgvo_ergebnis = dsgvo_pruefe(DSGVOEingabe(verarbeitet_personenbezogene_daten=False))

st.header("Ergebnis")

symbol = STUFEN_SYMBOL.get(ai_act_ergebnis.stufe.value, "")
st.subheader(f"{symbol} {ai_act_ergebnis.stufe.value}")
st.write(ai_act_ergebnis.hinweis)

with st.expander("Begründungspfad — AI Act", expanded=True):
    for schritt in ai_act_ergebnis.begruendung:
        markierung = "☑" if schritt.ausgeloest else "☐"
        st.markdown(f"- {markierung} **{schritt.artikel}** — {schritt.aussage}")

if dsgvo_ergebnis.einschlaegig:
    with st.expander("Begründungspfad — DSGVO", expanded=True):
        for punkt in dsgvo_ergebnis.pruefpunkte:
            markierung = STATUS_SYMBOL[punkt.status]
            st.markdown(f"- {markierung} **{punkt.artikel}** ({punkt.status}) — {punkt.aussage}")
        st.markdown(f"**Datenschutz-Folgenabschätzung:** {dsgvo_ergebnis.dsfa_begruendung}")

alle_offenen_punkte = list(dsgvo_ergebnis.offene_punkte) + ki_kompetenz_offene_punkte
if alle_offenen_punkte:
    st.subheader("Offene Punkte")
    for punkt in alle_offenen_punkte:
        st.markdown(f"- {punkt}")

st.divider()
st.header("Schritt 4 — Dokumentation")

bericht = erzeuge_bericht(
    systembezeichnung=systemname,
    ai_act_ergebnis=ai_act_ergebnis,
    dsgvo_ergebnis=dsgvo_ergebnis,
    zusaetzliche_offene_punkte=ki_kompetenz_offene_punkte,
)

st.download_button(
    "Bericht als Markdown herunterladen",
    data=bericht,
    file_name="ai-governance-bericht.md",
    mime="text/markdown",
)

with st.expander("Bericht anzeigen"):
    st.markdown(bericht)
