import copy
import sys
import pygame
import random
import numpy as np

from variables import *

#! --- PYGAME SETUP ---

pygame.init()
ventana = pygame.display.set_mode( (ANCHURA, ALTURA) )
pygame.display.set_caption('TIC TAC TOE')
ventana.fill( FONDO )

#! --- Clases ---

class tabla:

    def __init__(self):       
        self.posiciones = np.zeros( (FILAS, COLS) )
        self.posicionesVacias = self.posiciones # [posiciones]
        self.posicionesMarcadas = 0

    # * la variable mostrar es la que nos indica si debemos o no mostrar una victoria y para que lo haga al mismo tiempo
    # * que nos indica quien es el ganador ( si lo hay)
    
    
    # * dibuja la linea de victoria y retorna quien es el ganador
    def verificarGanador(self, mostrar=False):
        '''
            @return 0 si no hay ganador todavia
            @return 1 si el jugador 1 es el ganador
            @return 2 si el jguador 2 es el ganador
        '''

        #* victorias de manera vertical
        for col in range(COLS):
            if self.posiciones[0][col] == self.posiciones[1][col] == self.posiciones[2][col] != 0:
                if mostrar:
                    color = COLOR_CIRC if self.posiciones[0][col] == 2 else COLOR_EQUIS
                    posInicio = (col * SIZE_CUADROS + SIZE_CUADROS // 2, 20)
                    posFin = (col * SIZE_CUADROS + SIZE_CUADROS // 2, ALTURA - 20)
                    pygame.draw.line(ventana, color, posInicio, posFin, ANCHURA_LINEA)
                return self.posiciones[0][col]

        #* victorias de manera horizontal
        for fila in range(FILAS):
            if self.posiciones[fila][0] == self.posiciones[fila][1] == self.posiciones[fila][2] != 0:
                if mostrar:
                    color = COLOR_CIRC if self.posiciones[fila][0] == 2 else COLOR_EQUIS
                    posInicio = (20, fila * SIZE_CUADROS + SIZE_CUADROS // 2)
                    posFin = (ANCHURA - 20, fila * SIZE_CUADROS + SIZE_CUADROS // 2)
                    pygame.draw.line(ventana, color, posInicio, posFin, ANCHURA_LINEA)
                return self.posiciones[fila][0]

        #* victorias diagonales descendentes
        if self.posiciones[0][0] == self.posiciones[1][1] == self.posiciones[2][2] != 0:
            if mostrar:
                color = COLOR_CIRC if self.posiciones[1][1] == 2 else COLOR_EQUIS
                posInicio = (20, 20)
                posFin = (ANCHURA - 20, ALTURA - 20)
                pygame.draw.line(ventana, color, posInicio, posFin, ANCHURA_EQUIS)
            return self.posiciones[1][1]
        
        # * victorias diagonales ascendentes
        if self.posiciones[2][0] == self.posiciones[1][1] == self.posiciones[0][2] != 0:
            if mostrar:
                color = COLOR_CIRC if self.posiciones[1][1] == 2 else COLOR_EQUIS
                posInicio = (20, ALTURA - 20)
                posFin = (ANCHURA - 20, 20)
                pygame.draw.line(ventana, color, posInicio, posFin, ANCHURA_EQUIS)
            return self.posiciones[1][1]

        # * no hay victoria aun (no significa empate)
        return 0

    def marcarCuadro(self, fila, col, jugador):
        self.posiciones[fila][col] = jugador
        self.posicionesMarcadas += 1

    def cuadroVacio(self, fila, col):
        return self.posiciones[fila][col] == 0

    def get_posicionesVacias(self):
        posicionesVacias = []
        for fila in range(FILAS):
            for col in range(COLS):
                if self.cuadroVacio(fila, col):
                    posicionesVacias.append( (fila, col) )
        
        return posicionesVacias

    def estaLleno(self):
        return self.posicionesMarcadas == 9

    def isempty(self):
        return self.posicionesMarcadas == 0

class ia:

    # * el parametro de modo es el que nos define si la ia esta retornando las posiciones en modo random
    # * o lo esta haciendo aplicando minimax
    def __init__(self, modo=1, jugador=2):
        self.modo = modo
        self.jugador = jugador

    #! --- Modo random ---

    # * metodo que nos retorna una posicion random, para el modo de juego en el que la ia no evalua si es lo mejor o no
    def rnd(self, tabla):
        posicionesVacias = tabla.get_posicionesVacias()
        idx = random.randrange(0, len(posicionesVacias))
        # * literalmente elige una posicion aleatoria (tupla) entre las vacias y la retorna para elegirla como posiscion
        return posicionesVacias[idx] # (fila, col)



    #! --- Modo minimax ---

    def minimax(self, tabla, maximizando):
        
        # * establecemos los casos terminales, ya que verificarGanador nos retorna un valor entre 0 y 2
        # * con lo que podemos saber si aun no hay ganador, si el jugador 1 es el ganador o es el jugador 2
        # * con lo cual nos es posible que el algoritmo sepa, al estar minimizando, cual seria la mejor opcion a tomar
        # * intenta minimizar las ganancias, como lo vimos en clase, del jugador contrario, en este caso, de la persona (nosotros)
        caso = tabla.verificarGanador()

        # * caso en el que le jugador 1 es el ganador 
        if caso == 1:
            return 1, None #* teniendo en cuenta que se retorna el estado y el mejor movimiento, siendo un caso terminal no habria mejor movimiento

        # * caso en el que le jugador 2 es el ganador 
        if caso == 2:
            return -1, None

        # * caso en el que la tabla se encuentra llena de posiciones
        elif tabla.estaLleno():
            return 0, None

        # * en el caso en el que este maximizando
        # * es lo mismo que en le caso de que se este minimizando, simplemente, que 
        # * la explicacion mas a detalle esta en el siguiente caso
        if maximizando:
            max_eval = -100
            mejorMovimiento = None
            posicionesVacias = tabla.get_posicionesVacias()

            for (fila, col) in posicionesVacias:
                temp_tabla = copy.deepcopy(tabla)
                temp_tabla.marcarCuadro(fila, col, 1)
                evaluacion = self.minimax(temp_tabla, False)[0]
                if evaluacion > max_eval:
                    max_eval = evaluacion
                    mejorMovimiento = (fila, col)

            return max_eval, mejorMovimiento

        # * en el caso en el que este minimzando
        elif not maximizando:
            # * elegimos un numero grande para que sea reemplazado por la evaluacion del minimax, en clase lo vimos con el inf
            # * ya que cualquier valor es menor que inf, lo importante es que sea reemplazable por el algoritmo al ser mayor
            # * que los casos termianles
            evaluacionMinima = 100
            
            # * extraemos los cuadros que estan sin marcar en el estado del juego actual
            mejorMovimiento = None
            posicionesVacias = tabla.get_posicionesVacias()

            # * Vamos iterando entre todas los posibles movimientos, lo cual obtenemos con 
            # * posicionesVacias, ya que solo nos dara la lista de posiciones en las que no hay ningun jugador todavia marcado
            
            for (fila, col) in posicionesVacias:
                # * creamos una copia de la tabla actual, ya que no queremos modificar la real
                # * solo queremos ir verificando recursivamente hacia adentro de ella de manera temporal para retrnar
                # * su mejor movimiento
                temp_tabla = copy.deepcopy(tabla)
                temp_tabla.marcarCuadro(fila, col, self.jugador)
                
                # * lo evaluamos recursivamente hasta llegar a los casos base, o caso terminal y saber cual seria 
                # * el mejor movimiento entre todos los posibles, y eso es lo que guardamos en evaluacion, el caso terminal      
                # * le ponemos el valor de true para que vaya iterando, tal como lo vimos en clase, ya que como el juego,
                # * va por turnos, entre minimizar y maximizar, asi mismo va cambiando entre jugadores, 
                # * por eso arriba marcarCuadro se le envia el otro jugador      
                evaluacion = self.minimax(temp_tabla, True)[0]
                
                # * aqui es donde se reemplaza al checkear la primera movida, ya que evaluacionMinima lo pusimos en 100,
                # * y los reemplazamos por los nuevos valores
                if evaluacion < evaluacionMinima:
                    evaluacionMinima = evaluacion
                    mejorMovimiento = (fila, col)

            # * retornamos la evaluacion, que fue el caso encontrado como mejor, y la movida
            return evaluacionMinima, mejorMovimiento


    #! --- evaluacion principal ---

    def evaluacion(self, main_tabla):
        
        # * elegimos una poscion aleatoria entre las posibles, para el modo de juego aleatorio, si la variable modo=0
        if self.modo == 0:
            # * eleccion aleatoria
            evaluacion = 'random'
            movimiento = self.rnd(main_tabla)
        else:
            # * tambien retornamos la evaluacion, el caso terminal, y el mejor movimimiento posible,
            # * como inicialmente lo pasamos con maximizando = False, el se encargara de minimizar las ganancias
            # * por lo tanto, si evaluacion nos da un resultado de -1, significa que vamos a perder asegurado
            
            # * eleccion del codigo minimax
            evaluacion, movimiento = self.minimax(main_tabla, False)

        # * finalmente nos retorna dicha informacion en un print por consola
        print(f'la IA se decicio {movimiento} con un resultado de: {evaluacion}')

        return movimiento # * y nos quedamos con la movida (fila, columna)

class Juego:

    def __init__(self):
        self.tabla = tabla()
        self.ia = ia()
        self.jugador = 1         #! 1-equis  #2-circulos
        self.modoDeJuego = 'ia'    #! pvp o IA
        self.ejecutando = True
        self.dibujarLineas()

    #! --- metodos de dibujo ---

    # * metodo para dibujar las lineas de la cuadicula
    def dibujarLineas(self):
        # * el fondo
        ventana.fill( FONDO )

        # * lineas verticales
        pygame.draw.line(ventana, COLOR_LINEA, (SIZE_CUADROS, 0), (SIZE_CUADROS, ALTURA), ANCHURA_LINEA)
        pygame.draw.line(ventana, COLOR_LINEA, (ANCHURA - SIZE_CUADROS, 0), (ANCHURA - SIZE_CUADROS, ALTURA), ANCHURA_LINEA)

        # * lineas horizontales
        pygame.draw.line(ventana, COLOR_LINEA, (0, SIZE_CUADROS), (ANCHURA, SIZE_CUADROS), ANCHURA_LINEA)
        pygame.draw.line(ventana, COLOR_LINEA, (0, ALTURA - SIZE_CUADROS), (ANCHURA, ALTURA - SIZE_CUADROS), ANCHURA_LINEA)

    # * metodo que usamos para dibujar las figuras del circulo y la equis de cada jugador
    def dibujarFiguras(self, fila, col):
        if self.jugador == 1:
            # * dibujar equis
            # * linea descendente
            start_desc = (col * SIZE_CUADROS + BORDE, fila * SIZE_CUADROS + BORDE)
            end_desc = (col * SIZE_CUADROS + SIZE_CUADROS - BORDE, fila * SIZE_CUADROS + SIZE_CUADROS - BORDE)
            pygame.draw.line(ventana, COLOR_EQUIS, start_desc, end_desc, ANCHURA_EQUIS)
            
            # * linea ascendente
            start_asc = (col * SIZE_CUADROS + BORDE, fila * SIZE_CUADROS + SIZE_CUADROS - BORDE)
            end_asc = (col * SIZE_CUADROS + SIZE_CUADROS - BORDE, fila * SIZE_CUADROS + BORDE)
            pygame.draw.line(ventana, COLOR_EQUIS, start_asc, end_asc, ANCHURA_EQUIS)
        
        elif self.jugador == 2:
            # * dibujar circulo
            centro = (col * SIZE_CUADROS + SIZE_CUADROS // 2, fila * SIZE_CUADROS + SIZE_CUADROS // 2)
            pygame.draw.circle(ventana, COLOR_CIRC, centro, RADIO, ANCHURA_CIRC)




    #! --- Otros metodos ---

    # * aqui creamos algunas funciones que nos son de utilidad
    
    # * un jugador hace una movida
    def hacerMovimiento(self, fila, col):
        self.tabla.marcarCuadro(fila, col, self.jugador)
        self.dibujarFiguras(fila, col)
        self.cambiarTurno()

    # * cambiar al siguiente jugador, nos aprovechamos de que son solamente dos jugadores
    def cambiarTurno(self):
        self.jugador = self.jugador % 2 + 1

    # * cambiamos el modo de juego al siguiente
    def cambiarModoDeJuego(self):
        if self.modoDeJuego == 'pvp':
            self.modoDeJuego = 'ia' 
        else:
            self.modoDeJuego = 'pvp'

    # * verificamos si el tablero esta lleno o si ya hay un ganador, por eso debe ser distinto de 0
    # * le ponemos el parametro de True para que si hay ganador, lo checkee con la linea que indique la victoria
    def terminoJuego(self):
        return self.tabla.verificarGanador(mostrar=True) != 0 or self.tabla.estaLleno()

    # * cada que se resetea, se inicia de nuevo el constructor para settear todo a su valor por defecto y comenzar de nuevo
    def reiniciar(self):
        self.__init__()

def main():

    #! --- Objetos ---

    juego = Juego()
    tabla = juego.tabla
    ia = juego.ia



    #! --- mainloop ---

    while True:
        
        # * eventos
        for event in pygame.event.get():

            # * cerrar el juego
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # * evento de presionar una tecla
            if event.type == pygame.KEYDOWN:

                # * con 'g' cambiamos el modo de juego
                if event.key == pygame.K_g:
                    juego.cambiarModoDeJuego()

                # * con 'r' reseteamos el juego
                if event.key == pygame.K_r:
                    juego.reiniciar()
                    tabla = juego.tabla
                    ia = juego.ia

                # * con el '0' decisiones disponibles completamente aleatorias  
                if event.key == pygame.K_0:
                    ia.modo = 0
                
                # * con el '1' decisiones disponibles elegidas por el metodo minimax
                if event.key == pygame.K_1:
                    ia.modo = 1

            # * evento de dar click sobre la ventana, la cual dividimos con la funcion piso
            # * para que se nos acople a la matriz actual   
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                fila = pos[1] // SIZE_CUADROS
                col = pos[0] // SIZE_CUADROS
                
                # * marcar una casilla como movimiento, se puede hacer solo cuando dicha casilla 
                # * esta vacia y el juego sigue corriendo, aun no ha terminado
                if tabla.cuadroVacio(fila, col) and juego.ejecutando:
                    juego.hacerMovimiento(fila, col)

                    if juego.terminoJuego():
                        juego.ejecutando = False


        # * llamado inicial a la IA, donde, si el modo, el jugador, y el estado del juego corresponden, la IA actua 
        # * haciendo un movimiento
        if juego.modoDeJuego == 'ia' and juego.jugador == ia.jugador and juego.ejecutando:

            # * actualizamos la ventana
            pygame.display.update()

            # * retornamos la posicion y llamamos al metodo para que la aplique
            fila, col = ia.evaluacion(tabla)
            juego.hacerMovimiento(fila, col)

            # * si el juego se termina por cualquiera de las 3 razones, terminamos el juego poniendo ejecutando en False
            if juego.terminoJuego():
                juego.ejecutando = False
            
        pygame.display.update()

main()