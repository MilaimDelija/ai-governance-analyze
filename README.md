# Automatisierter AI-Governance-Analyzer

Dieses Repository enthält eine interaktive Streamlit-Anwendung, die ein geplantes KI-System nach der Verordnung (EU) 2024/1689 (AI Act) und der Datenschutz-Grundverordnung einordnet. Es entstand als Arbeitsprobe im Rahmen einer Ausbildung zum zertifizierten Datenschutzbeauftragten (TÜV) und bildet die Checkliste `dsgvo-ai-act-checkliste.md` aus dem Repository [eu-ai-act-dsgvo-compliance-framework](https://github.com/MilaimDelija/eu-ai-act-dsgvo-compliance-framework) als ausführbare Logik ab, statt sie nur als Dokument bereitzustellen.

## Warum eine vierstufige Einordnung

Viele vereinfachte Darstellungen des AI Act reduzieren die Risikoeinordnung auf drei Stufen: verboten, hohes Risiko, geringes Risiko. Diese Vereinfachung blendet die eigenständigen Transparenzpflichten aus Art. 50 AI Act aus, die weder eine verbotene Praktik noch ein Hochrisiko-System voraussetzen, aber unabhängig davon eigene Offenlegungspflichten begründen — etwa die Kennzeichnungspflicht eines Chatbots gegenüber Website-Besuchern. Dieses Werkzeug unterscheidet deshalb konsequent vier Ergebnisse: Verboten (Art. 5), Hochrisiko (Art. 6 i. V. m. Anhang III), Transparenzpflicht (Art. 50) und Minimales Risiko. Die Pflicht zur KI-Kompetenz nach Art. 4 AI Act gilt unabhängig von dieser Einstufung für jedes eingesetzte System und wird deshalb getrennt ausgewiesen, nicht als weitere Risikostufe.

Jedes Ergebnis wird zusammen mit einem vollständigen Begründungspfad angezeigt: Für jeden geprüften Punkt ist ersichtlich, ob er zutrifft, welcher Artikel einschlägig ist und wie er wörtlich lautet. Das Ergebnis ist damit keine bloße Ampel-Anzeige, sondern nachvollziehbar und im Zweifel überprüfbar.

## Aufbau

`src/ai_act_classifier.py` enthält die Klassifizierung nach dem AI Act (Abschnitt 2 der Checkliste) sowie die separate Prüfung der KI-Kompetenz nach Art. 4.

`src/dsgvo_check.py` enthält die datenschutzrechtliche Prüfung (Abschnitt 3 der Checkliste), einschließlich einer Heuristik zur Erforderlichkeit einer Datenschutz-Folgenabschätzung nach Art. 35 DSGVO.

`src/report.py` erzeugt aus einem abgeschlossenen Durchlauf einen Markdown-Bericht im Aufbau der Checkliste, der als Nachweis nach Schritt 4 der Checkliste abgelegt werden kann.

`app.py` verbindet die drei Module zu einer Streamlit-Oberfläche, die durch die vier Schritte führt und den Bericht zum Download anbietet.

`tests/` enthält automatisierte Tests für die Klassifizierungslogik, die datenschutzrechtliche Prüfung, die Berichterstellung und — über `streamlit.testing.v1.AppTest` — für das Verhalten der Oberfläche selbst, ohne dass dafür ein Browser erforderlich ist.

## Verwendung

Voraussetzung ist Python 3.11 oder neuer.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Die Anwendung ist danach unter `http://localhost:8501` erreichbar.

## Tests

```bash
pip install -r requirements.txt
pytest
```

## Einschränkungen

Dieses Werkzeug ersetzt keine Rechtsberatung im Einzelfall. Insbesondere die endgültige Einordnung als Hochrisiko-System, die Erforderlichkeit einer Datenschutz-Folgenabschätzung und die Wirksamkeit einer konkreten Übermittlungsgrundlage in ein Drittland hängen von Umständen ab, die nur im jeweiligen Einzelfall geprüft werden können. Das Werkzeug bildet den Stand der Checkliste zum Zeitpunkt des letzten Commits ab und ist entsprechend regelmäßig gegen Änderungen der zugrunde liegenden Vorschriften zu prüfen.

## Rechtsstand

Verordnung (EU) 2024/1689 über künstliche Intelligenz (AI Act); Datenschutz-Grundverordnung (EU) 2016/679 (DSGVO).

## Lizenz

MIT-Lizenz, siehe `LICENSE`.
