# Chatbot Rasa per la Gestione di Collezioni

Chatbot conversazionale sviluppato con **Rasa** per la gestione di **collezioni di oggetti** (carte, auto, monete, ecc.) tramite linguaggio naturale.
Il sistema consente all’utente di consultare, cercare, aggiungere ed eliminare oggetti all’interno di collezioni persistenti.

---

## Funzionalità principali

* Gestione di più collezioni tematiche
* Ricerca degli oggetti anche tramite nome parziale
* Aggiunta dinamica di nuovi elementi
* Eliminazione guidata e sicura degli oggetti
* Persistenza dei dati tramite **SQLite** o **CSV**
* Integrazione con **Telegram**

---

## Tecnologie utilizzate

* **Python 3.9**
* **Rasa** (NLU + Core)
* **Pandas**
* **SQLite**
* **Telegram Bot API**
* **ngrok**
* **Visual Studio Code**

> ⚠️ Rasa non supporta Python ≥ 3.10

---

## Struttura del progetto

```
project/
├── actions/
│   ├── actions.py
│   └── actions_NOSQL.py
├── data/
│   ├── nlu.yml
│   ├── rules.yml
│   └── stories.yml
├── test/
│   └── Dataset/
│       ├── carte.csv
│       ├── auto.csv
│       └── collezioni.db
├── scripts/
├── domain.yml
├── config.yml
├── credentials.yml
└── endpoints.yml
```

---

## Installazione

### Clonazione del repository

```bash
git clone <repository_url>
cd CHATBOT_RASA
```

### Creazione ambiente virtuale

```bash
py -3.9 -m venv env_chatbot_rasa
```

### Attivazione ambiente

```bash
.\env_chatbot_rasa\Scripts\activate
```

### Installazione dipendenze

```bash
pip install rasa pandas
```

> ❗ Non aggiornare `pip`, per evitare incompatibilità con Rasa.

---

## Training del modello

```bash
rasa train
```

---

## Avvio del chatbot in locale

### Avvio Action Server

```bash
rasa run actions
```

### Avvio chatbot da terminale

```bash
rasa shell
```

---

## Gestione dei dati

* I dati iniziali sono forniti tramite file **CSV**
* All’avvio del bot vengono automaticamente convertiti in **SQLite**
* Ogni collezione corrisponde a una tabella del database
* Gli attributi delle collezioni sono dinamici e dipendono dal dataset

---

## Azioni disponibili

* `action_elenca_collezioni`
* `action_conta_oggetti_collezione`
* `action_mostra_oggetti_collezione`
* `action_trova_oggetto_specifico`
* `action_aggiungi_oggetto_collezione`
* `action_elimina_oggetto_collezione`

---

## Esempi di comandi

```
Ciao
Mostrami le collezioni
Quanti oggetti ci sono nella collezione carte?
Cerca Luffy nella collezione carte
Aggiungi una Ferrari rossa
Elimina il 2
```

---

## Integrazione con Telegram

### Requisiti

* Rasa 3.6.21
* aiogram 2.25.1
* aiohttp 3.9.5

### Procedura

1. Creare un bot tramite **@BotFather**
2. Inserire il token in `credentials.yml`
3. Esporre il server Rasa con ngrok:

```bash
ngrok http 5005
```

4. Avviare i servizi:

```bash
rasa run actions
rasa run --connector telegram --debug
```

---

## Modalità NoSQL (opzionale)

È disponibile una versione alternativa senza database SQL, basata esclusivamente su file **CSV**.
Questa modalità utilizza:

* parsing deterministico
* parsing fuzzy (similarità testuale)

File di riferimento: `actions_NOSQL.py`

---

## Riferimenti

* [https://rasa.com](https://rasa.com)
* [https://huggingface.co/rasa](https://huggingface.co/rasa)
* [https://github.com/RasaHQ/rasa-action-examples](https://github.com/RasaHQ/rasa-action-examples)

---

## Autore

Progetto sviluppato a scopo **didattico e sperimentale**.

---

Se vuoi, al prossimo passo posso:

* ridurlo ulteriormente in **README minimal**
* aggiungere **badge GitHub**
* scrivere una sezione **Future Work**
* adattarlo per **progetto universitario / esame**

Dimmi tu 👍

