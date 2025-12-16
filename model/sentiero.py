from dataclasses import dataclass
import datetime
@dataclass
class Sentiero:
    id:int
    id_rifugio1: int
    id_rifugio2: int
    distanza : float
    difficolta: float
    durata: datetime.time
    anno:int

    def __str__(self):
        return f"{self.id, self.id_rifugio1, self.id_rifugio2, self.distanza, self.difficolta, self.durata, self.anno}"

    def __repr__(self):
        return f"{self.id, self.id_rifugio1, self.id_rifugio2, self.distanza, self.difficolta, self.durata, self.anno}"
