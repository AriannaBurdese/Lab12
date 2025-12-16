from dataclasses import dataclass
@dataclass
class Rifugio:
    id: int
    nome: str
    localita: str
    altitudine: str
    capienza: str
    aperto: str

    def __str__(self):
        return f" { self.nome}"
    def __repr__(self):
        return f"{ self.nome}"
    def __hash__(self):
        return hash(self.id)