# Chatbot Rasa per la Gestione di Collezioni

Chatbot conversazionale sviluppato con **Rasa** per la gestione di **collezioni di oggetti** (carte, auto, monete, ecc.) tramite linguaggio naturale.
Il sistema consente all’utente di consultare, cercare, aggiungere ed eliminare oggetti all’interno di collezioni persistenti.

---
## Come funziona Rasa
Come funziona Chatbot Rasa 
 
Il funzionamento di Rasa si articola in due componenti principali: il modulo NLU (Natural Language Under standing), responsabile dell’ analisi semantica dell’input dell’ utente, e il modulo Core, che si occupa di determinare la risposta più adeguata in base alla storia conversazionale. Quando un utente invia un messaggio al chatbot, ad esempio “Aggiungi una carta di tipo Leader”, il primo componente che entra in gioco è Rasa NLU. Questo modulo ha il compito di trasformare il testo grezzo in un’informazione strutturata, riconoscendo l’intent (cioè l’intenzione comunicativa dell’utente, in questo caso aggiungi_oggetto) ed  estraendo le entità rilevanti (ad esempio categoria = carta, tipo = Leader). In questo modo il sistema non si limita a leggere il testo, ma ne comprende il significato a livello semantico.   
   
Le informazioni elaborate dal NLU vengono quindi trasmesse al Rasa Core, che rappresenta il “motore decisionale” dell’architettura. Il Core valuta lo stato corrente della conversazione, ossia il contesto e gli slot già compilati, e decide la prossima azione da eseguire. Tale scelta si basa sia sulle regole e sulle stories apprese durante la fase di addestramento, sia sugli obiettivi della conversazione. A seconda dei casi, il Core può generare direttamente una risposta semplice oppure richiedere l’esecuzione di una custom action.   
   
Le azioni personalizzate vengono gestite dall’Action Server, un servizio separato che esegue codice Python scritto dallo sviluppatore. Qui è possibile implementare logiche complesse, come l’interazione con un database o con servizi esterni. Nell’esempio considerato, l’Action Server potrebbe eseguire la funzione action_aggiungi_oggetto, responsabile di salvare nel database una nuova voce relativa alla carta di tipo Leader. Una volta completata l’operazione, l’Action Server restituisce il risultato al Core, che a sua volta lo trasmette all’utente sotto forma di risposta naturale (ad esempio: “Ho aggiunto la carta Leader alla tua collezione”).   
Questo flusso di lavoro dimostra come Rasa non si limiti a fornire risposte predefinite, ma sia in grado di integrare comprensione linguistica, gestione del contesto e logiche applicative avanzate. La separazione tra i moduli NLU, Core e Action Server garantisce infatti un’architettura modulare e flessibile, facilmente estendibile a nuovi domini e capace di interagire con basi di dati e applicazioni esterne.   
   
Uno degli aspetti più rilevanti di Rasa è la possibilità di integrare azioni (actions) personalizzate, scritte in Python, che consentono al chatbot di andare oltre le semplici risposte statiche e di eseguire operazioni complesse, interagendo con basi di dati, API esterne o altri servizi applicativi. Nel progetto sviluppato, ad esempio, la gestione delle collezioni è stata implementata interamente tramite funzioni contenute nel file actions.py. Ogni volta che l’utente formula una richiesta che non può essere soddisfatta da una risposta predefinita, il sistema attiva una custom action. Questo meccanismo prevede l’avvio di un server dedicato che riceve la richiesta, esegue la logica programmata e restituisce una risposta dinamica da mostrare all’utente. È in questo contesto che vengono effettuate operazioni come l’aggiunta di un oggetto al database, la ricerca all’interno delle collezioni, la verifica della presenza di un attributo specifico o l’eliminazione guidata di un elemento.   
   
Il dialogo tra utente e chatbot è supportato da un sistema di slot, ossia variabili temporanee che permettono di conservare dati durante la conversazione. Se, ad esempio, l’utente scrive “Aggiungi una Ferrari rossa”, il sistema può memorizzare la categoria “auto” e il nome “Ferrari rossa” in due slot distinti, che potranno essere riutilizzati nei turni successivi per completare la richiesta o generare conferme più naturali. Gli slot, insieme all’elenco degli intenti, delle entità riconosciute e delle azioni disponibili, sono dichiarati all’interno del file domain.yml, che rappresenta il “cervello dichiarativo” del sistema, definendo ciò che il bot è in grado di comprendere, ricordare ed eseguire.   
Perché il sistema funzioni in maniera efficace è necessario addestrare un modello conversazionale. Il processo di training prende avvio dall’elaborazione di diversi file di configurazione:   

•	nlu.yml: che raccoglie numerosi esempi per ciascun intento;   
•	stories.yml: che descrive conversazioni complete sotto forma di sequenze di intenti e azioni;   
•	rules.yml: che impone comportamenti specifici in determinate situazioni.   
	 
L’addestramento viene eseguito con il comando rasa train e produce un pacchetto compresso nella cartella models/, contenente sia il modello NLP sia il policy ensemble addestrato, pronto per essere utilizzato.   
Un ulteriore punto di forza di Rasa è la possibilità di testare l’assistente in modo diretto. Questo può avvenire tramite la modalità interattiva da terminale (rasa shell), oppure simulando richieste utente per osservare in tempo reale il comportamento del modello. È inoltre possibile avviare il server delle azioni (rasa run actions) per verificare l’esecuzione delle funzioni Python collegate alle custom actions.   
   
Dal punto di vista architetturale, Rasa si distingue per la sua versatilità: può essere eseguito in locale, integrato con canali di messaggistica come Telegram, oppure distribuito tramite container Docker, rendendo la sua adozione adatta a diversi scenari di deployment. Nel progetto sviluppato, Rasa è stato utilizzato non solo per interpretare le richieste dell’utente, ma anche per orchestrare una logica applicativa strutturata basata su un database SQLite, popolato dinamicamente a partire da file CSV. Questa integrazione tra comprensione linguistica, logiche Python e gestione di dati persistenti ha permesso di costruire un sistema modulare e adattabile, capace di gestire diverse tipologie di collezioni e facilmente estensibile a nuovi domini applicativi.   


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
| # | Comando                               | Descrizione                          |
| - | ------------------------------------- | ------------------------------------ |
| 1 | `git clone <repository_url>`          | Clona il repository del progetto     |
| 2 | `cd CHATBOT_RASA`                     | Entra nella cartella del progetto    |
| 3 | `py -3.9 -m venv env_chatbot_rasa`    | Crea un ambiente virtuale Python 3.9 |
| 4 | `.\env_chatbot_rasa\Scripts\activate` | Attiva l’ambiente virtuale           |
| 5 | `pip install rasa pandas`             | Installa le dipendenze principali    |
| 6 | `rasa train`                          | Addestra il modello                  |
| 7 | `rasa run actions`                    | Avvia l’Action Server                |
| 8 | `rasa shell`                          | Avvia il chatbot da terminale        |


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

### Connessione server Telegram

1. Creare un bot tramite **@BotFather**
2. Inserire il token in `credentials.yml`
3. Esporre il server locale Rasa con ngrok:

```bash
ngrok http 5005
```

4. Avviare i servizi:

```bash
rasa run actions
rasa run --connector telegram --debug
```

## Riferimenti

* [https://rasa.com](https://rasa.com)
* [https://huggingface.co/rasa](https://huggingface.co/rasa)
* [https://github.com/RasaHQ/rasa-action-examples](https://github.com/RasaHQ/rasa-action-examples)

---

## Autore

Andrea Langiotti


