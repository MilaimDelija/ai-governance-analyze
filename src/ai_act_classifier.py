"""Einordnung eines KI-Systems nach der Verordnung (EU) 2024/1689 (AI Act).

Dieses Modul bildet die vier Prüfschritte aus Abschnitt 2 der Checkliste
`dsgvo-ai-act-checkliste.md` (Repository eu-ai-act-dsgvo-compliance-framework)
als ausführbare Logik ab: verbotene Praktiken nach Art. 5, Hochrisiko-Einstufung
nach Art. 6 i. V. m. Anhang III, Transparenzpflichten nach Art. 50 und die von
der Risikostufe unabhängige Pflicht zur KI-Kompetenz nach Art. 4.

Die Reihenfolge der Prüfung folgt der Checkliste: Sobald eine verbotene Praktik
vorliegt, endet die Prüfung an dieser Stelle, da eine Nutzung ohnehin nicht
zulässig ist. Erst wenn keine verbotene Praktik vorliegt, wird die
Hochrisiko-Einstufung geprüft, und erst wenn auch diese negativ ausfällt, die
Transparenzpflichten. Ein System kann also nicht gleichzeitig als "Verboten"
und als "Hochrisiko" eingestuft werden; die höhere Stufe hat Vorrang, weil sie
die Nutzung insgesamt ausschließt.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class AIActRisikostufe(str, Enum):
    """Die vier Ergebnisstufen der Einordnung.

    Der AI Act selbst kennt kein einheitliches Etikett für die vierte Stufe;
    "Minimales Risiko" wird hier verwendet, um sie von der dritten Stufe
    abzugrenzen, die zwar keine verbotene oder hochriskante Nutzung darstellt,
    aber eigenständige Offenlegungspflichten nach Art. 50 AI Act auslöst. Die
    gängige Vereinfachung auf drei Stufen (verboten / hoch / gering) blendet
    diese Offenlegungspflichten aus und wird deshalb hier bewusst nicht
    übernommen.
    """

    VERBOTEN = "Verboten"
    HOCHRISIKO = "Hochrisiko"
    TRANSPARENZPFLICHT = "Transparenzpflicht (Art. 50 AI Act)"
    MINIMAL = "Minimales Risiko"


@dataclass
class VerbotenePraktikenEingabe:
    """Angaben zu Art. 5 Abs. 1 AI Act.

    Jedes Feld entspricht einer der in der Checkliste aufgeführten verbotenen
    Praktiken. Ein Wert von True bedeutet, dass das System die jeweilige
    Praktik tatsächlich ausübt (nicht, dass die Praktik ausgeschlossen ist).
    """

    unterschwellige_beeinflussung: bool = False
    ausnutzung_schutzbeduerftigkeit: bool = False
    social_scoring: bool = False
    biometrische_kategorisierung_sensibel: bool = False
    emotionserkennung_arbeitsplatz: bool = False


@dataclass
class HochrisikoEingabe:
    """Angaben zu Art. 6 i. V. m. Anhang III AI Act."""

    bewerberauswahl: bool = False
    beschaeftigtenbewertung: bool = False
    kreditwuerdigkeitspruefung: bool = False
    produktsicherheitsrelevant: bool = False


@dataclass
class TransparenzEingabe:
    """Angaben zu Art. 50 AI Act."""

    direkte_interaktion: bool = False
    synthetische_medieninhalte: bool = False
    deepfake_erzeugung: bool = False


@dataclass
class KIKompetenzEingabe:
    """Angaben zu Art. 4 AI Act.

    Diese Pflicht gilt für jedes KI-System unabhängig von dessen
    Risikoeinstufung und fließt deshalb nicht in die Klassifizierung nach
    `klassifiziere` ein, sondern wird über `pruefe_ki_kompetenz` separat
    ausgewertet.
    """

    richtlinie_bekannt: bool = False
    einweisung_erfolgt: bool = False
    teilnahme_dokumentiert: bool = False


@dataclass
class AIActEingabe:
    """Zusammenfassung aller Angaben zu Schritt 2 der Checkliste."""

    verbotene_praktiken: VerbotenePraktikenEingabe = field(default_factory=VerbotenePraktikenEingabe)
    hochrisiko: HochrisikoEingabe = field(default_factory=HochrisikoEingabe)
    transparenz: TransparenzEingabe = field(default_factory=TransparenzEingabe)


@dataclass
class Begruendungsschritt:
    """Ein einzelner Prüfpunkt im Begründungspfad.

    `ausgeloest` zeigt an, ob die im jeweiligen Artikel beschriebene
    Voraussetzung im konkreten Fall erfüllt ist (unabhängig davon, ob dies zu
    einer für das Unternehmen günstigen oder ungünstigen Einordnung führt).
    """

    artikel: str
    aussage: str
    ausgeloest: bool


@dataclass
class AIActErgebnis:
    """Ergebnis der Klassifizierung mit vollständigem Begründungspfad."""

    stufe: AIActRisikostufe
    begruendung: list[Begruendungsschritt]
    hinweis: str


_PRUEFUNGEN_VERBOTEN = (
    (
        "unterschwellige_beeinflussung",
        "Art. 5 Abs. 1 lit. a AI Act",
        "Das System nutzt unterschüwellige Techniken, die eine Person zu deren Schaden wesentlich beeinflussen können.".replace("unterschüwellige", "unterschwellige"),
    ),
    (
        "ausnutzung_schutzbeduerftigkeit",
        "Art. 5 Abs. 1 lit. b AI Act",
        "Das System nutzt eine Schutzbedürftigkeit aufgrund von Alter, Behinderung oder sozialer bzw. wirtschaftlicher Lage aus.",
    ),
    (
        "social_scoring",
        "Art. 5 Abs. 1 lit. c AI Act",
        "Das System bewertet oder klassifiziert Personen anhand ihres sozialen Verhaltens mit nachteiliger Wirkung (Social Scoring).",
    ),
    (
        "biometrische_kategorisierung_sensibel",
        "Art. 5 Abs. 1 lit. g AI Act",
        "Das System leitet aus biometrischen Daten sensible Merkmale ab, etwa politische Meinung oder sexuelle Orientierung.",
    ),
    (
        "emotionserkennung_arbeitsplatz",
        "Art. 5 Abs. 1 lit. f AI Act",
        "Das System erkennt Emotionen am Arbeitsplatz außerhalb der engen medizinischen oder sicherheitsbezogenen Ausnahmen.",
    ),
)

_PRUEFUNGEN_HOCHRISIKO = (
    (
        "bewerberauswahl",
        "Anhang III Nr. 4 lit. a AI Act",
        "Das System wählt Bewerbungen automatisiert vor, bewertet sie oder lehnt sie ab.",
    ),
    (
        "beschaeftigtenbewertung",
        "Anhang III Nr. 4 lit. b AI Act",
        "Das System bewertet Beschäftigte oder beeinflusst Entscheidungen über Beförderung oder Kündigung.",
    ),
    (
        "kreditwuerdigkeitspruefung",
        "Anhang III Nr. 5 lit. b AI Act",
        "Das System prüft die Kreditwürdigkeit oder Bonität natürlicher Personen.",
    ),
    (
        "produktsicherheitsrelevant",
        "Art. 6 Abs. 1 AI Act i. V. m. Anhang I",
        "Das System ist Sicherheitsbauteil eines Produkts, das bereits einer produktrechtlichen Konformitätsbewertung unterliegt.",
    ),
)

_PRUEFUNGEN_TRANSPARENZ = (
    (
        "direkte_interaktion",
        "Art. 50 Abs. 1 AI Act",
        "Das System tritt gegenüber Kunden oder Dritten direkt in Erscheinung, etwa als Chatbot oder Sprachassistent.",
    ),
    (
        "synthetische_medieninhalte",
        "Art. 50 Abs. 2 AI Act",
        "Das System erzeugt oder verändert Bild-, Audio- oder Videoinhalte, die authentisch wirken könnten.",
    ),
    (
        "deepfake_erzeugung",
        "Art. 50 Abs. 4 AI Act",
        "Das System erzeugt oder verändert Inhalte, die als Deepfake im Sinne des AI Act einzuordnen sind.",
    ),
)


def _bewerte(quelle: object, pruefungen: tuple[tuple[str, str, str], ...]) -> tuple[list[Begruendungsschritt], list[str]]:
    schritte: list[Begruendungsschritt] = []
    ausgeloeste_artikel: list[str] = []
    for feldname, artikel, aussage in pruefungen:
        ausgeloest = bool(getattr(quelle, feldname))
        schritte.append(Begruendungsschritt(artikel=artikel, aussage=aussage, ausgeloest=ausgeloest))
        if ausgeloest:
            ausgeloeste_artikel.append(artikel)
    return schritte, ausgeloeste_artikel


def klassifiziere(eingabe: AIActEingabe) -> AIActErgebnis:
    """Ordnet ein System anhand der Angaben aus Schritt 2 der Checkliste ein.

    Die Prüfung erfolgt in der Reihenfolge Art. 5 → Art. 6/Anhang III → Art. 50,
    exakt wie in der Checkliste beschrieben. Sobald eine Stufe zutrifft, werden
    die nachfolgenden Stufen nicht mehr geprüft, weil die Checkliste an dieser
    Stelle selbst vorsieht, dass "das Verfahren endet" bzw. weitergehende
    Pflichten unabhängig von einer Transparenzprüfung greifen.
    """

    begruendung: list[Begruendungsschritt] = []

    verboten_schritte, verboten_treffer = _bewerte(eingabe.verbotene_praktiken, _PRUEFUNGEN_VERBOTEN)
    begruendung.extend(verboten_schritte)
    if verboten_treffer:
        return AIActErgebnis(
            stufe=AIActRisikostufe.VERBOTEN,
            begruendung=begruendung,
            hinweis=(
                "Die geplante Nutzung ist nach Art. 5 AI Act nicht zulässig. Das Verfahren endet an dieser "
                "Stelle; eine Prüfung der Hochrisiko-Kriterien oder der Transparenzpflichten erübrigt sich, "
                "da die Nutzung bereits auf dieser Stufe ausgeschlossen ist. Die zuständige Fachabteilung "
                "sowie die Datenschutzbeauftragte bzw. der Datenschutzbeauftragte sind zu informieren."
            ),
        )

    hochrisiko_schritte, hochrisiko_treffer = _bewerte(eingabe.hochrisiko, _PRUEFUNGEN_HOCHRISIKO)
    begruendung.extend(hochrisiko_schritte)
    if hochrisiko_treffer:
        return AIActErgebnis(
            stufe=AIActRisikostufe.HOCHRISIKO,
            begruendung=begruendung,
            hinweis=(
                "Es handelt sich voraussichtlich um ein Hochrisiko-System im Sinne des AI Act. Diese "
                "Einschätzung ersetzt nicht die weitergehenden Pflichten aus Titel III Kapitel 2 AI Act "
                "(Risikomanagementsystem, Daten-Governance, technische Dokumentation, menschliche Aufsicht, "
                "Registrierung in der EU-Datenbank), die vor einer Inbetriebnahme zu prüfen sind."
            ),
        )

    transparenz_schritte, transparenz_treffer = _bewerte(eingabe.transparenz, _PRUEFUNGEN_TRANSPARENZ)
    begruendung.extend(transparenz_schritte)
    if transparenz_treffer:
        return AIActErgebnis(
            stufe=AIActRisikostufe.TRANSPARENZPFLICHT,
            begruendung=begruendung,
            hinweis=(
                "Das System ist weder verboten noch hochriskant, unterliegt aber eigenständigen "
                "Transparenzpflichten aus Art. 50 AI Act. Die dort vorgesehene Kennzeichnung bzw. "
                "Offenlegung ist vor der Inbetriebnahme umzusetzen."
            ),
        )

    return AIActErgebnis(
        stufe=AIActRisikostufe.MINIMAL,
        begruendung=begruendung,
        hinweis=(
            "Nach den geprüften Kriterien ergeben sich keine spezifischen Pflichten aus Art. 5, Art. 6 "
            "oder Art. 50 AI Act. Unabhängig von dieser Einstufung bleibt die KI-Kompetenz nach Art. 4 "
            "AI Act zu gewährleisten, da diese Pflicht für sämtliche KI-Systeme unabhängig von ihrer "
            "Risikoeinstufung gilt."
        ),
    )


def pruefe_ki_kompetenz(eingabe: KIKompetenzEingabe) -> list[str]:
    """Prüft die organisatorischen Pflichten aus Art. 4 AI Act.

    Gibt eine Liste offener Punkte zurück; eine leere Liste bedeutet, dass alle
    drei Voraussetzungen aus Abschnitt 2.4 der Checkliste erfüllt sind.
    """

    offene_punkte: list[str] = []
    if not eingabe.richtlinie_bekannt:
        offene_punkte.append(
            "Interne KI-Richtlinie ist den betroffenen Mitarbeitenden noch bekannt zu machen (Art. 4 AI Act)."
        )
    if not eingabe.einweisung_erfolgt:
        offene_punkte.append(
            "Einweisung in die konkreten Grenzen und Fehlerquellen des Systems steht noch aus (Art. 4 AI Act)."
        )
    if not eingabe.teilnahme_dokumentiert:
        offene_punkte.append(
            "Teilnahme an der Einweisung ist noch nicht dokumentiert (Art. 4 AI Act)."
        )
    return offene_punkte
