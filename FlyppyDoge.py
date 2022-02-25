# Importo le librerie
import pygame
import random

# Inizializzo PyGame
pygame.init()

# Carico le immagini
sfondo = pygame.image.load('sfondo.png')
dog = pygame.image.load('dog.png')
base = pygame.image.load('base.png')
gameover = pygame.image.load('gameover.png')
tubo_giu = pygame.image.load('tubo.png')
tubo_su = pygame.transform.flip(tubo_giu, False, True)

# Costanti Globali
SCHERMO = pygame.display.set_mode((288, 512))
FPS = 50
VEL_AVANZ = 3
FONT = pygame.font.SysFont('Comic Sans MS', 50, bold=True)

class tubi_classe:
    def __init__(self):
        self.x = 300
        self.y = random.randint(-75,150)
    def avanza_e_disegna(self):
        self.x -= VEL_AVANZ
        SCHERMO.blit(tubo_giu, (self.x,self.y+230))
        SCHERMO.blit(tubo_su, (self.x,self.y-230))
    def collisione(self, dog, dogx, dogy):
         tolleranza = 20
         dog_lato_dx = dogx+dog.get_width()-tolleranza
         dog_lato_sx = dogx+tolleranza
         tubi_lato_dx = self.x + tubo_giu.get_width() 
         tubi_lato_sx = self.x 
         dog_lato_su = dogy+tolleranza
         dog_lato_giu = dogy+dog.get_height()-tolleranza
         tubi_lato_su = self.y+110
         tubi_lato_giu = self.y+210
         if dog_lato_dx > tubi_lato_sx and dog_lato_sx < tubi_lato_dx:
             if dog_lato_su < tubi_lato_su or dog_lato_giu > tubi_lato_giu:
                 you_lose()
    def fra_i_tubi(self, uccello, uccellox):
         tolleranza = 5
         dog_lato_dx = dogx+dog.get_width()-tolleranza
         dog_lato_sx = dogx+tolleranza
         tubi_lato_dx = self.x 
         tubi_lato_sx = self.x + tubo_giu.get_width()
         if dog_lato_dx > tubi_lato_dx and dog_lato_sx < tubi_lato_sx:
             return True
     

def disegna_oggetti():
    SCHERMO.blit(sfondo, (0,0))
    for t in tubi:
        t.avanza_e_disegna()
    SCHERMO.blit(dog, (dogx,dogy))
    SCHERMO.blit(base, (basex,400))
    punti_render = FONT.render(str(punti), 1, (255,255,255))
    SCHERMO.blit(punti_render, (144,0))
    

def aggiorna():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)
    
def inizializza():
    global dogx, dogy, dog_vely
    global basex
    global tubi
    global punti
    global fra_i_tubi
    dogx, dogy = 60,150
    dog_vely = 0
    basex = 0
    punti = 0
    tubi = []
    tubi.append(tubi_classe())
    fra_i_tubi = False
            

def you_lose():
    SCHERMO.blit(gameover, (70,130))
    aggiorna()
    ricominciamo = False
    while not ricominciamo:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                inizializza()
                ricominciamo = True
            if event.type == pygame.QUIT:
                pygame.quit()

# inizializzo Variabili
inizializza ()

### Ciclo Principale ##
while True:
    # Avanzamento Base
    basex -= VEL_AVANZ
    if basex < -45: basex = 0
    # Gravità
    dog_vely += 1
    dogy += dog_vely
    # Comandi
    for event in pygame.event.get():
        if ( event.type == pygame.KEYDOWN
             and event.key == pygame.K_UP ):
            dog_vely = -10
        if event.type == pygame.QUIT:
            pygame.quit()
    if tubi[-1].x < 150: tubi.append(tubi_classe()) 
    # Collisione Dog-Tubo
    for t in tubi:
        t.collisione(dog, dogx, dogy)
    if not fra_i_tubi:
        for t in tubi:
            if t.fra_i_tubi(dog, dogx):
                fra_i_tubi = True
                break
    if fra_i_tubi:
        fra_i_tubi = False
        for t in tubi:
            if t.fra_i_tubi(dog, dogx):
                fra_i_tubi = True 
                break
        if not fra_i_tubi:
            punti += 1
    # Collisione con Base
    if dogy > 450:
        you_lose()
    # Aggiornamento Schermo
    disegna_oggetti()
    aggiorna()
