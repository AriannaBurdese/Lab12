from database.DB_connect import DBConnect
from model.rifugio import Rifugio
from model.sentiero import Sentiero


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    @staticmethod
    def get_nodes() -> list[Rifugio] | None:
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM rifugio")
        try:
            cursor.execute(query)
            for row in cursor:
                rifugio = Rifugio(
                    id = row['id'],
                    nome = row["nome"],
                    localita = row["localita"],
                    altitudine = row["altitudine"],
                    capienza = row["capienza"],
                    aperto = row["aperto"],
                )
                result.append(rifugio)
        except Exception as e:
            print(f"Errore durante la query: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_edges(year)-> list[Sentiero] | None:
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = ("""SELECT * 
                 FROM connessione
                 WHERE anno <= %s""")
        try:
            cursor.execute(query, (year,))
            for row in cursor:
                sentiero = Sentiero(
                    id = row['id'],
                    id_rifugio1=row['id_rifugio1'],
                    id_rifugio2=row['id_rifugio2'],
                    distanza = row['distanza'],
                    difficolta=row['difficolta'],
                    durata=row['durata'],
                    anno=row['anno'],
                )
                result.append(sentiero)
        except Exception as e:
            print(f"Errore durante la query:{e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result









