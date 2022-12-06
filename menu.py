import pygame

ANCHO = 800
ALTO = 500

pantalla = pygame.display.set_mode((ANCHO,ALTO))

#cargar botones

imagenX10 = pygame.image.load('button_10x10.png').convert_alpha()
imagenX3 = pygame.image.load('button_3x3.png').convert_alpha()
imagenSalir = pygame.image.load('button_salir.png').convert_alpha()

#clase boton
class boton:
    
    def __init__(self, x, y, imagen, escala):
        ancho = imagen.get_width()
        alto = imagen.get_height()
        self.imagen = pygame.transform.scale(imagen, (int(ancho * escala), int(alto * escala)))
        self.rect = self.imagen.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        
    def dibujar(self):
        action = False
        
        #obtener la posicion del mouse
        pos = pygame.mouse.get_pos()
        #print(pos)
        
        #obtener sobre que esta el mouse y condiciones de click
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked==False:
                self.clicked = True
                action=True
                
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        
        #dibujar botones en la pantalla
        
        pantalla.blit(self.imagen,(self.rect.x, self.rect.y))
        
        return action
    
    
    
# creamos las instanacias de los botones

botonX3 = boton(150,280,imagenX3, 0.75)
botonX10 = boton(320,280,imagenX10, 0.57)
botonSalir = boton(500,280,imagenSalir, 0.55)

# main loop

run = True
while run:
    
    
    pantalla.fill((0, 158, 255))
    
    
    if botonX3.dibujar():
        print('botonX3')
    if botonSalir.dibujar():
        print('botonSalir')
        run = False
    if botonX10.dibujar():
        print('botonX10')
    
    # eventos
    
    for event in pygame.event.get():
        #salir del juego
        
        if event.type == pygame.QUIT:
            run = False
        
    pygame.display.update()
    
pygame.quit()
        
        
        
