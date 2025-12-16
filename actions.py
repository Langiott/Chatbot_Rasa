import os
import sqlite3
import pandas as pd
from typing import Text, List, Any, Dict
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# === Setup database da CSV ===
BASE_PATH = "test/Dataset"
CSV_FILES = ["carte.csv", "auto.csv"]
DB_PATH = os.path.join(BASE_PATH, "collezioni.db")

if not os.path.exists(BASE_PATH):
    os.makedirs(BASE_PATH)

conn = sqlite3.connect(DB_PATH)
for file in CSV_FILES:
    name = os.path.splitext(file)[0].lower()
    file_path = os.path.join(BASE_PATH, file)
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
        df.to_sql(name, conn, index=False, if_exists="replace")
    else:
        print(f"⚠️ CSV non trovato: {file_path}")
conn.close()

# === Funzioni utili ===
def connetti_db():
    return sqlite3.connect(DB_PATH)

def ottieni_colonne(tabella: str) -> List[str]:
    conn = connetti_db()
    try:
        query = f"PRAGMA table_info({tabella})"
        result = pd.read_sql_query(query, conn)
        return result["name"].tolist()
    except:
        return []
    finally:
        conn.close()

# === VARIABILE GLOBALE PER MEMORIZZARE OGGETTI TEMPORANEI PER UTENTE
OGGETTI_TEMP = {}  # dict → {sender_id: {"categoria": ..., "oggetti": [...] }}


# === Azioni ===

class ActionElencaCollezioni(Action):
    def name(self) -> Text:
        return "action_elenca_collezioni"

    def run(self, dispatcher, tracker, domain):
        conn = connetti_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelle = [row[0] for row in cursor.fetchall()]
        conn.close()

        if tabelle:
            dispatcher.utter_message(text="Collezioni disponibili: " + ", ".join(tabelle))
        else:
            dispatcher.utter_message(text="⚠️ Nessuna collezione trovata.")
        return []

class ActionContaOggettiCollezione(Action):
    def name(self) -> Text:
        return "action_conta_oggetti_collezione"

    def run(self, dispatcher, tracker, domain):
        categoria = tracker.get_slot("categoria")
        if not categoria:
            dispatcher.utter_message(text="❗ Specifica una collezione.")
            return []

        conn = connetti_db()
        try:
            query = f"SELECT COUNT(*) FROM {categoria}"
            count = conn.execute(query).fetchone()[0]
            dispatcher.utter_message(text=f"Hai {count} oggetti nella collezione '{categoria}'.")
        except:
            dispatcher.utter_message(text=f"⚠️ Collezione '{categoria}' non trovata.")
        finally:
            conn.close()
        return []

class ActionMostraOggettiCollezione(Action):
    def name(self) -> Text:
        return "action_mostra_oggetti_collezione"

    def run(self, dispatcher, tracker, domain):
        categoria = tracker.get_slot("categoria")
        nome = tracker.get_slot("nome")
        if not categoria:
            dispatcher.utter_message(text="❗ Specifica una collezione.")
            return []

        conn = connetti_db()
        try:
            colonne = ottieni_colonne(categoria)
            if not colonne:
                dispatcher.utter_message(text=f"⚠️ Collezione '{categoria}' vuota o inesistente.")
                return []

            query = f"SELECT * FROM {categoria}"
            df = pd.read_sql_query(query, conn)

            if nome:
                nome_lower = nome.lower()
                mask = df.apply(lambda row: any(nome_lower in str(row[c]).lower() for c in colonne), axis=1)
                df = df[mask]

            if df.empty:
                dispatcher.utter_message(text="🔎 Nessun oggetto trovato.")
            else:
                for _, row in df.iterrows():
                    messaggio = ", ".join([f"{c}: {row[c]}" for c in colonne])
                    dispatcher.utter_message(text=f"🔍 {messaggio}")
        except Exception as e:
            dispatcher.utter_message(text=f"Errore: {str(e)}")
        finally:
            conn.close()
        return []

class ActionTrovaOggettoSpecifico(Action):
    def name(self) -> Text:
        return "action_trova_oggetto_specifico"

    def run(self, dispatcher, tracker, domain):
        categoria = tracker.get_slot("categoria")
        nome = tracker.get_slot("nome")
        if not categoria or not nome:
            dispatcher.utter_message(text="❗ Specifica sia la collezione che il nome dell'oggetto.")
            return []

        conn = connetti_db()
        try:
            colonne = ottieni_colonne(categoria)
            if not colonne:
                dispatcher.utter_message(text=f"⚠️ Collezione '{categoria}' non trovata.")
                return []

            query = f"SELECT * FROM {categoria}"
            df = pd.read_sql_query(query, conn)

            # Match cumulativo di tutte le parole nel nome su tutte le colonne
            parole = nome.lower().split()
            mask = df.apply(lambda row: all(any(parola in str(row[c]).lower() for c in colonne) for parola in parole), axis=1)
            df = df[mask]

            if df.empty:
                dispatcher.utter_message(text="🔎 Nessun oggetto trovato con quei criteri.")
            elif len(df) == 1:
                row = df.iloc[0]
                messaggio = ", ".join([f"{c}: {row[c]}" for c in colonne])
                dispatcher.utter_message(text=f"✅ Oggetto trovato: {messaggio}")
            else:
                dispatcher.utter_message(text=f"Trovati {len(df)} oggetti simili:")
                for _, row in df.iterrows():
                    messaggio = ", ".join([f"{c}: {row[c]}" for c in colonne])
                    dispatcher.utter_message(text=f"– {messaggio}")
        except Exception as e:
            dispatcher.utter_message(text=f"Errore: {str(e)}")
        finally:
            conn.close()
        return []

class ActionAggiungiOggetto(Action):
    def name(self) -> Text:
        return "action_aggiungi_oggetto"

    def run(self, dispatcher, tracker, domain):
        categoria = tracker.get_slot("categoria")
        nome = tracker.get_slot("nome")
        if not categoria or not nome:
            dispatcher.utter_message(text="❗ Specifica collezione e oggetto.")
            return []

        conn = connetti_db()
        try:
            colonne = ottieni_colonne(categoria)
            parole = nome.strip().split()
            nuova_riga = {col: parole[i] if i < len(parole) else "?" for i, col in enumerate(colonne)}

            # ✅ Usa virgolette doppie per colonne SQL (es. "set")
            colonne_str = ", ".join([f'"{col}"' for col in nuova_riga.keys()])
            valori_str = ", ".join(["?" for _ in nuova_riga])
            query = f"INSERT INTO {categoria} ({colonne_str}) VALUES ({valori_str})"
            conn.execute(query, list(nuova_riga.values()))
            conn.commit()
            dispatcher.utter_message(text="✅ Aggiunto:\n" + ", ".join([f"{k}: {v}" for k, v in nuova_riga.items()]))
        except Exception as e:
            dispatcher.utter_message(text=f"Errore inserimento: {str(e)}")
        finally:
            conn.close()
        return []

class ActionEliminaOggetto(Action):
    def name(self) -> Text:
        return "action_elimina_oggetto"

    def run(self, dispatcher, tracker, domain):
        import re
        import json

        text = tracker.latest_message.get("text", "").lower().strip()
        session_id = tracker.sender_id

        # STEP 1 — verifica se l'utente ha digitato un numero
        match = re.search(r"\b(\d+)\b", text)
        if match:
            index = int(match.group(1)) - 1

            # Recupera la lista di oggetti salvata nei tracker events
            eventi = tracker.events
            lista_salvata = None
            categoria = None

            for e in reversed(eventi):
                if e.get("event") == "slot" and e.get("name") == "eliminazione_temporanea":
                    try:
                        dati = json.loads(e.get("value"))
                        lista_salvata = dati.get("oggetti")
                        categoria = dati.get("categoria")
                        break
                    except:
                        continue

            if lista_salvata and categoria:
                if 0 <= index < len(lista_salvata):
                    oggetto = lista_salvata[index]
                    colonne = list(oggetto.keys())
                    valori = [str(oggetto[c]) for c in colonne]
                    condizioni = " AND ".join([f'"{c}" = ?' for c in colonne])

                    try:
                        conn = connetti_db()
                        conn.execute(f'DELETE FROM {categoria} WHERE {condizioni}', valori)
                        conn.commit()
                        conn.close()
                        dispatcher.utter_message(text=f"🗑️ Oggetto {index+1} eliminato.")
                    except Exception as e:
                        dispatcher.utter_message(text=f"❌ Errore eliminazione: {str(e)}")
                else:
                    dispatcher.utter_message(text="❗ Numero fuori intervallo.")
                return []

        # STEP 2 — Ricerca oggetti da eliminare
        categoria = tracker.get_slot("categoria")
        nome = tracker.get_slot("nome")

        if not categoria or not nome:
            dispatcher.utter_message(text="❗ Specifica la collezione e il nome dell’oggetto.")
            return []

        try:
            colonne = ottieni_colonne(categoria)
            conn = connetti_db()
            df = pd.read_sql_query(f"SELECT * FROM {categoria}", conn)

            parole = nome.lower().split()
            mask = df.apply(lambda r: all(any(p in str(r[c]).lower() for c in colonne) for p in parole), axis=1)
            df_filtrato = df[mask]

            if df_filtrato.empty:
                dispatcher.utter_message(text="🔎 Nessun oggetto trovato.")
            elif len(df_filtrato) == 1:
                row = df_filtrato.iloc[0]
                condizioni = " AND ".join([f'"{col}" = ?' for col in colonne])
                valori = [str(row[col]) for col in colonne]
                conn.execute(f'DELETE FROM {categoria} WHERE {condizioni}', valori)
                conn.commit()
                dispatcher.utter_message(text="🗑️ Oggetto eliminato.")
            else:
                dispatcher.utter_message(text=f"Trovati {len(df_filtrato)} oggetti simili. Digita il numero da eliminare:")
                for i, (_, row) in enumerate(df_filtrato.iterrows()):
                    descrizione = ", ".join([f"{c}: {row[c]}" for c in colonne])
                    dispatcher.utter_message(text=f"{i+1}. {descrizione}")

                # Salva i dati come stringa JSON nello slot temporaneo
                from rasa_sdk.events import SlotSet
                dati_salvati = {
                    "categoria": categoria,
                    "oggetti": df_filtrato.to_dict(orient="records")
                }
                return [SlotSet("eliminazione_temporanea", json.dumps(dati_salvati))]

        except Exception as e:
            dispatcher.utter_message(text=f"❌ Errore: {str(e)}")
        finally:
            conn.close()

        return []
