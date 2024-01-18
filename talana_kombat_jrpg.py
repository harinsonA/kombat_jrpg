import json
from typing import Tuple, List, Dict


class Personaje:
    NOMBRE = ''
    MOVIMIENTOS = []
    GOLPES = []
    ENERGIA = 6
    COMBOS = {}
    MOVIMIENTO_BASICO = {
        'W': {
            'nombre': 'arriba',
            'ataque': 0,
        },
        'S': {
            'nombre': 'abajo',
            'ataque': 0,
        },
        'A': {
            'nombre': 'la izquierda',
            'ataque': 0,
        },
        'D': {
            'nombre': 'la derecha',
            'ataque': 0,
        },
    }
    GOLPES_BASICOS = {
        'P': {
            'nombre': 'un puño',
            'ataque': 1,
        },
        'K': {
            'nombre': 'una patada',
            'ataque': 1,
        },
    }

    @staticmethod
    def normalizar_lista(lista_de_datos: List[str]) -> List:
        return [dato.upper() for dato in lista_de_datos]

    @classmethod
    def numero_movimientos(cls) -> int:
        return len([movimiento for movimiento in cls.MOVIMIENTOS if movimiento])

    @classmethod
    def numero_golpes(cls) -> int:
        return len([golpe for golpe in cls.GOLPES if golpe])

    @classmethod
    def total_movimientos_y_golpes(cls) -> int:
        return sum([cls.numero_movimientos(), cls.numero_golpes()])

    @classmethod
    def energia_restante(cls, golpe_recibido: int = 0) -> int:
        cls.ENERGIA -= golpe_recibido
        return cls.ENERGIA

    @classmethod
    def es_un_movimiento_basico(cls, movimiento_realizado: str) -> bool:
        return movimiento_realizado in list(cls.MOVIMIENTO_BASICO.keys())

    @classmethod
    def es_un_golpe_basico(cls, movimiento_realizado: str) -> bool:
        return movimiento_realizado in list(cls.GOLPES_BASICOS)

    @classmethod
    def es_un_golpe_especial(cls, movimiento_realizado: str) -> bool:
        return movimiento_realizado in list(cls.COMBOS.keys())

    @classmethod
    def relator_de_movimiento(
        cls,
        movimientos_realizados: str,
        descripcion_de_acciones: str,
        energia_a_quitar: int
    ) -> Tuple:

        numero_de_movimientos = len(movimientos_realizados)
        movimientos_basicos = {
            **cls.MOVIMIENTO_BASICO,
            **cls.GOLPES_BASICOS,
        }

        indice = 0
        while numero_de_movimientos > 0:
            accion = movimientos_basicos.get(movimientos_realizados[indice], '')
            if not accion:
                indice += 1
                numero_de_movimientos -= 1
                continue

            if cls.es_un_movimiento_basico(movimientos_realizados[indice]):
                descripcion_de_acciones += f' se movio hacia {accion["nombre"]}'
                energia_a_quitar += accion["ataque"]

            if cls.es_un_golpe_basico(movimientos_realizados[indice]):
                descripcion_de_acciones += f' conecto {accion["nombre"]}'
                energia_a_quitar += accion["ataque"]

            indice += 1
            numero_de_movimientos -= 1

        return descripcion_de_acciones, energia_a_quitar

    @classmethod
    def acciones_ejecutadas(cls, movimientos: str, golpe: str) -> int:
        descripcion_de_acciones = f'{cls.NOMBRE}'
        energia_a_quitar = 0
        acciones = f'{movimientos}{golpe}'

        if len(movimientos) <= 3:
            if cls.es_un_golpe_especial(acciones):
                descripcion_de_acciones += f' conecto un {cls.COMBOS[acciones]["nombre"]}'
                print(f'-> {descripcion_de_acciones}')
                energia_a_quitar += cls.COMBOS[acciones]["ataque"]
                return energia_a_quitar

            descripcion_de_acciones, energia_a_quitar = \
                cls.relator_de_movimiento(acciones[:-3], descripcion_de_acciones, energia_a_quitar)

            if cls.es_un_golpe_especial(acciones[-3:]):
                descripcion_de_acciones += f' conecto un {cls.COMBOS[acciones]["nombre"]}'
                energia_a_quitar += cls.COMBOS[acciones]["ataque"]

            descripcion_de_acciones, energia_a_quitar = \
                cls.relator_de_movimiento(acciones[-3:], descripcion_de_acciones, energia_a_quitar)

            print(f'-> {descripcion_de_acciones}')
            return energia_a_quitar

        descripcion_de_acciones, energia_a_quitar = \
            cls.relator_de_movimiento(acciones[:-3], descripcion_de_acciones, energia_a_quitar)

        if cls.es_un_golpe_especial(acciones[-3:]):
            descripcion_de_acciones += f' conecto un {cls.COMBOS[acciones]["nombre"]}'
            energia_a_quitar += cls.COMBOS[acciones]["ataque"]

        descripcion_de_acciones, energia_a_quitar = \
            cls.relator_de_movimiento(acciones[-3:], descripcion_de_acciones, energia_a_quitar)

        print(f'-> {descripcion_de_acciones}')
        return energia_a_quitar


class TonynStallone(Personaje):
    NOMBRE = 'Tonyn'
    COMBOS = {
        'DSDP': {
            'nombre': 'Taladoken',
            'ataque': 3,
        },
        'SDK': {
            'nombre': 'Remuyuken',
            'ataque': 2,
        },
    }

    def __init__(self, movimientos: List, golpes: List) -> None:
        TonynStallone.MOVIMIENTOS = self.normalizar_lista(movimientos)
        TonynStallone.GOLPES = self.normalizar_lista(golpes)


class ArnardorShuatseneguer(Personaje):
    NOMBRE = 'Arnardor'
    COMBOS = {
        'SAK': {
            'nombre': 'Remuyuken',
            'ataque': 3,
        },
        'ASAP': {
            'nombre': 'Taladoken',
            'ataque': 2,
        },
    }

    def __init__(self, movimientos: List, golpes: List) -> None:
        ArnardorShuatseneguer.MOVIMIENTOS = self.normalizar_lista(movimientos)
        ArnardorShuatseneguer.GOLPES = self.normalizar_lista(golpes)


def obtener_duracion_del_combate(player1: Personaje, player2: Personaje) -> int:
    return (player1.numero_movimientos()
            if player1.total_movimientos_y_golpes() > player2.total_movimientos_y_golpes() else
            player2.numero_movimientos())


def obtener_quien_inicia_kombate(player1: Personaje, player2: Personaje) -> Tuple:
    if (player1.total_movimientos_y_golpes() < player2.total_movimientos_y_golpes()):
        return player1, player2
    return player2, player1


def talana_kombat_JRPG(datos_de_pelea: Dict) -> None:
    player1 = datos_de_pelea['player1']
    player2 = datos_de_pelea['player2']

    tonyn_stallone = TonynStallone(movimientos=player1['movimientos'], golpes=player1['golpes'])
    arnaldor_shuateseneguer = ArnardorShuatseneguer(movimientos=player2['movimientos'], golpes=player2['golpes'])

    duracion_del_combate = obtener_duracion_del_combate(tonyn_stallone, arnaldor_shuateseneguer)
    player1, player2 = obtener_quien_inicia_kombate(tonyn_stallone, arnaldor_shuateseneguer)

    print('||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||')
    print(f'|||||||||||||||||||||||  {player1.NOMBRE} VS {player2.NOMBRE}  ||||||||||||||||||||||||||||||||')
    print('||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||')
    print(f'----> Inicia: {player1.NOMBRE}\n')
    indice = 0
    while duracion_del_combate > 0:
        try:
            energia_a_quitar = player1.acciones_ejecutadas(player1.MOVIMIENTOS[indice], player1.GOLPES[indice])
            energia_restante = player2.energia_restante(energia_a_quitar)

            if energia_restante <= 0:
                print(f'\n*{player1.NOMBRE} gana la pelea y aun le queda {player1.ENERGIA} de energia*')
                break

            energia_a_quitar = player2.acciones_ejecutadas(player2.MOVIMIENTOS[indice], player2.GOLPES[indice])
            energia_restante = player1.energia_restante(energia_a_quitar)

            if energia_restante <= 0:
                print(f'\n*{player2.NOMBRE} gana la pelea y aun le queda {player2.ENERGIA} de energia*')
                break
            indice += 1
            duracion_del_combate -= 1
        except IndexError:
            break

    if player1.ENERGIA == player2.ENERGIA:
        print(f'\n*Player1 y Player2 no saben jugar pasen control*')

    if player1.ENERGIA > player2.ENERGIA:
        print(f'\n*{player1.NOMBRE} gana la pelea y aun le queda {player1.ENERGIA} de energia*')

    if player1.ENERGIA < player2.ENERGIA:
        print(f'\n*{player2.NOMBRE} gana la pelea y aun le queda {player2.ENERGIA} de energia*')
    print('\n')
    print('||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||')


# ... Simulacion de json 
KOMBAT = {
    "player1": {
        "movimientos": ["DSD", "S"],
        "golpes": ["P", ""]
    },
    "player2": {
        "movimientos": ["","ASA","DA","AAA", "", "SA"],
        "golpes": ["P", "", "P", "K", "K", "K",]
    }
}
json_de_pelea_recibido = json.dumps(KOMBAT)
datos_de_pelea = json.loads(json_de_pelea_recibido)


# ... Inicia Kombat
talana_kombat_JRPG(datos_de_pelea)
