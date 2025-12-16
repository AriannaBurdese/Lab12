import networkx as nx

from database.dao import DAO



class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.G = nx.Graph()
        self._id_map = {}
        self._dizionario_rifugi = {}

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        self.G.clear()  # svuoto grafo
        lista_rifugi = DAO.get_nodes()
        self._id_map = {}  # associa ogni id del rifugio all'oggetto Rifugio corrispondente
        for rifugio in lista_rifugi:
            rifugio_id = getattr(rifugio, 'id', None)
            if rifugio_id is not None:
                self._id_map[rifugio_id] = rifugio

        sentieri = DAO.get_edges(year)  # lista dei sentieri filtrata per anno
        coeff = {
            "facile": 1,
            "media": 1.5,
            "difficile": 2

        }
        for sentiero in sentieri:
            rifugio1 = self._id_map[sentiero.id_rifugio1]  # prendo gli id dei due rifugi collegati, con id_map li trasformo negli oggeti RIFUGIO corrispondenti per usarli come nodi nel grafo
            rifugio2 = self._id_map[sentiero.id_rifugio2]

            peso = float(sentiero.distanza) * float(coeff[sentiero.difficolta])
            self.G.add_edge(rifugio1,rifugio2, weight = peso)  # networkx controlla se rifugio 1 e 2 sono gia dei nodi, e se non esistono li crea.


    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        peso_min = min(nx.get_edge_attributes(self.G, "weight").values())
        peso_max = max(nx.get_edge_attributes(self.G, "weight").values())
        return peso_min, peso_max



    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        minori = 0
        maggiori = 0
        pesi = nx.get_edge_attributes(self.G, "weight")
        for peso in pesi.values():
            if peso < soglia:
                minori += 1
            elif peso > soglia:
                maggiori += 1
                #se soglia = peso non incremento

        return minori, maggiori



    """Implementare la parte di ricerca del cammino minimo"""
    #due metodi: ricorsivo e con networkx
    #metodo con network x

    def getPercorsoMinimo(self, soglia):
        #filtro archi del grafo
        G_filtrato = nx.Graph()
        G_filtrato.add_nodes_from(self.G.nodes)
        for u,v,data in self.G.edges(data=True):
            if data['weight'] > soglia:
                G_filtrato.add_edge(u, v, weight = data['weight'])
        percorsi_minimi = []
        miglior_costo = float("inf")
        nodi = list(G_filtrato.nodes)

        for i in range(len(nodi)):
            for j in range(i + 1, len(nodi)):
                source = nodi[i]  # ← QUI nasce vSource
                target = nodi[j]  # ← QUI nasce vTarget

                #cerco percorso minimo, costo = somma pesi archi
                try:
                    costo, percorso = nx.single_source_dijkstra(G_filtrato, source, target, weight="weight")
                    #controllo che abbia almeno 2 archi
                    if (len(percorso)) >= 3:
                        if costo < miglior_costo:
                                miglior_costo = costo
                                percorsi_minimi = [(source, target, percorso)]
                        elif costo == miglior_costo:
                            percorsi_minimi.append((source, target,percorso))

                except nx.NetworkXNoPath:
                    continue


            result = []
            for source, target, percorso in percorsi_minimi:
                for k in range(len(percorso) - 1):
                    u = percorso[k]
                    v = percorso[k + 1]
                    peso = G_filtrato[u][v]["weight"]
                    result.append((u, v, peso))
        return result ,miglior_costo

    """def getPercorsoMinimo(self, soglia):
        # Creo il grafo filtrato
        G_filtrato = nx.Graph()
        G_filtrato.add_nodes_from(self.G.nodes)
        for u, v, data in self.G.edges(data=True):
            if data['weight'] > soglia:
                G_filtrato.add_edge(u, v, weight=data['weight'])

        percorsi_minimi = []
        miglior_costo = float("inf")
        nodi = list(G_filtrato.nodes)

        # Funzione ricorsiva per esplorare tutti i percorsi tra source e target
        def ricorsione(nodo_corrente, target, percorso, costo):
            nonlocal percorsi_minimi, miglior_costo

            percorso.append(nodo_corrente)

            if nodo_corrente == target:
                if len(percorso) >= 2:
                    if costo < miglior_costo:
                        miglior_costo = costo
                        percorsi_minimi = [(list(percorso), costo)]
                    elif costo == miglior_costo:
                        percorsi_minimi.append((list(percorso), costo))
                percorso.pop()
                return

            for vicino in G_filtrato.neighbors(nodo_corrente):
                if vicino not in percorso:
                    peso = G_filtrato[nodo_corrente][vicino]["weight"]
                    ricorsione(vicino, target, percorso, costo + peso)

            percorso.pop()

        # Provo tutte le coppie di nodi
        for i in range(len(nodi)):
            for j in range(i + 1, len(nodi)):
                ricorsione(nodi[i], nodi[j], [], 0)

        # Trasformo i percorsi in formato (u, v, peso)
        result = []
        for percorso, costo in percorsi_minimi:
            arco_percorso = []
            for k in range(len(percorso) - 1):
                u = percorso[k]
                v = percorso[k + 1]
                peso = G_filtrato[u][v]["weight"]
                arco_percorso.append((u, v, peso))
            result.append((arco_percorso, costo))


        return result, miglior_costo"""












