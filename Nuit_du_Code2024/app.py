import pyxel

# (0,240)
# tileheight coin gauche écran

    # Cooed : solid, xmin, xmax, ymin, ymax

SIZE = 128
COLLISION = {
    # Format CoordTileSheet : (solid , (xMin, yMin), (xMax, yMax))

    # [ biome 1]
    (2,26) : ( (0,0), (8,6)), # plateformBottom

    (1,27) : ( (0,0), (8,6)), # plateformRight
    (2,27) : ( (0,0), (8,6)), # plateformMid
    (3,27) : ( (0,0), (8,6)), # plateformLeft
    
    (8,27) : ( (0,0), (4,6)), # plateform_Corner_Left
    (8,27) : ( (0,0), (4,6)), # plateform_Corner_Right


    (7,27) : ( (5,0), (8,6)), # plateform_Flat_Corner_Left
    (8,27) : ( (0,0), (4,6)), # plateform_Flat_Corner_Right
    
    (6,25) : ( (0,0), (4,6)), # ConstructLeft
    (4,25) : ( (0,0), (4,6)), # ConstructMid
    (7,25) : ( (0,0), (4,6)), # ConstructRight

    # [ Biome 2 ]
    
    (11, 27) : ( (0,0), (8,6)), # plateformMid
    
    (7,30) : ( (0,0), (4,6)), # plateform_Corner_Left
    (8,30) : ( (0,0), (4,6)), # plateform_Corner_Right

    (16,27) : ( (5,0), (8,6)), # plateform_Flat_Corner_Left
    (17,27) : ( (0,0), (4,6)), # plateform_Flat_Corner_Right
    
    (3, 25) :( (0,0), (8,8)),
    (5, 25) : ( (0,0), (8,8))
    

}

CHECKPOINT=(7,22) #a mettre tranparent (3,21)
GOAL=(7,23) #a mettre tranparent (2,21)

GOLD_STAR=(6,17) #a mettre tranparent (0,24)
SILVER_STAR=(7,17) #a mettre tranparent (24)
BRONZE_STAR=(6,18) #a mettre tranparent (2,24)

class Game:
    def __init__(self): # initialisation
        pyxel.init(SIZE,SIZE, title='Nuit du Code', fps=60)
        pyxel.load('4.pyxres')
        pyxel.mouse(True)
        self.y = 0
        self.collision = COLLISION
        self.gravity = 0

        self.player = Player(140,64, self)
        self.entity = [self.player]
        self.Tile = None
        self.TILEMAP = 0
        self.tilemap = pyxel.tilemap(self.TILEMAP)

        self.begin = 0
        self.win = False
        self.start()
        pyxel.run(self.update, self.draw)

    def input(self):

        # [ INPUT MOUVEMENT ]
        if self.begin == 0:
            self.player.y = 64
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and 33<pyxel.mouse_x<85 and 40<pyxel.mouse_y<60:
                self.gravity = 10
                self.begin = 1
        elif self.begin == 2:
            if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT): # droite
                self.player.moving = 1
                self.player.status = 'Right'
            elif pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.KEY_LEFT): # gauche
                self.player.moving = -1
                self.player.status = 'Left'
            else:
                self.player.moving = 0
            
            if pyxel.btn(pyxel.KEY_SPACE):
     
                self.player.jump()
        
    
    def update(self):
        self.end()
        if not self.win:
            for ent in self.entity:
                ent.speed_y += self.gravity
            if self.begin == 1:
                if self.player.y > 2030:
                    self.begin = 2
            self.input()
            self.player.updatecoord()
            pyxel.flip()

    def draw(self):
        if not self.win:
            pyxel.cls(0)
            
            pyxel.camera(0,max(min(self.player.y-64,1918), 0))
            pyxel.bltm(0,0,self.TILEMAP,0,0, SIZE,2048)
            for el in self.tochange:
                pyxel.blt(el[0], el[1], 0, 16, 224, 8, 8)
                pyxel.blt(el[0], el[1], 0, el[2], el[3], 8, 8, 5)
            self.player.animations(self.player.status)
            
            
            if self.begin == 0:
                pyxel.text(33, 50, "START THE GOOSE", 7)
            pyxel.text(64, 2000, "PRESS 'LEFT'", 7)
            pyxel.flip()

    
    def start(self):
        self.begin = 0
        self.tochange = []
        for x in range(16):
            for y in range(255):
                tile = self.tilemap.pget(x, y)
                if tile != (2, 28) and tile != (2, 26) and tile != (11,28):
                    self.tochange.append([x*8, y*8, tile[0]*8, tile[1]*8])

    def end(self):
        if self.player.y < 0:
            self.win = True
            pyxel.camera(0,64)
            pyxel.cls(7)
            pyxel.text(28, 110,"Vous avez gagne(e)",1 )
            pyxel.flip()
#player.collide


class Player:
    def __init__(self, x, y, game):
        self.game = game
        self.x, self.y = x, y
        self.speed_y = 0
        self.speed = 30
        self.moving = 0
        self.status = 'Right'

    def draw(self):
        #pyxel.blt(self.x, self.y,0,0, 136,8, 8,5)
        self.animations(self.status)

    def jump(self):
        if self.collide(ground = 1):
            self.speed_y = -100
        self.y -= 2
    
    def move(self, side):
        self.moving = side
        
    def updatecoord(self):
        
        while self.collide(ground = 1):
            self.y -= 4
        self.y += self.speed_y*8/60
   
        if self.y > 2032:
            self.y = 2032
            self.speed_y = 0
        if self.moving == -1 and self.x > 0:
            self.x -= self.speed*8/60
        elif self.moving == 1 and self.x < 120:
            self.x += self.speed*8/60

        if self.collide():
            difx, dify = pyxel.sgn(self.x-self.oldx), pyxel.sgn(self.y-self.oldy)
            if dify != 0:
                difx = 0
            if dify == -1:
                self.speed_y = self.speed_y/10
            while self.collide():
                self.x -= difx
                self.y -= dify
        self.oldx, self.oldy = self.x, self.y
            
        
    
    def collide(self, ground = 0):
        
        tilecoords = (self.x//8, self.y//8)
        bd = 1
        # A|B
        # C|D
        
        if ground:
            self.y += 2
        
        # Test si Player touche en C
        tile = self.game.tilemap.pget(tilecoords[0], tilecoords[1]+1)
        if self.y%8 == 0 :
            tile = self.game.tilemap.pget(tilecoords[0], tilecoords[1])
            bd = 0
            
        if tile in self.game.collision.keys():
            bornes = self.game.collision[tile][0:2]
            if self.x%8<bornes[1][0] and self.y%8 > bornes[0][1]+1:
                if self.speed_y > 0:
                    self.speed_y = 0

                return True
        
        # Test si Player touche en D
        tile = self.game.tilemap.pget(tilecoords[0], tilecoords[1])
        if bd and self.x%8 != 0:
            tile = self.game.tilemap.pget(tilecoords[0]+1, tilecoords[1]+1)
            
        if tile in self.game.collision.keys():
            bornes = self.game.collision[tile][0:2]
            if self.x%8>bornes[0][0] and self.y%8 > bornes[0][1]+1:
                if self.speed_y > 0:
                    self.speed_y = 0

                return True
        
        if ground:
            return False
        #Tile sur les coordonnées du personnage (Test si Player touche en A)
        tile = self.game.tilemap.pget(tilecoords[0], tilecoords[1])
        if tile in self.game.collision.keys():
            bornes = self.game.collision[tile][0:2]
            if self.x%8<bornes[1][0] and self.y%8 < bornes[1][1]:

                return True
                
        
        
        # Test si Player touche en B
        tile = self.game.tilemap.pget(tilecoords[0]+1, tilecoords[1])
        if self.x%8 == 0 :
            tile = self.game.tilemap.pget(tilecoords[0], tilecoords[1])
        
        if tile in self.game.collision.keys():
            bornes = self.game.collision[tile][0:2]
            if self.x%8>bornes[0][0] and self.y%8 < bornes[1][1]:

                return True
        
        
        
        return False

    def animations(self,status):



        pyxel.blt(self.x,self.y,0, 0,0,8,8,5)
        if status == 'Right':

            pyxel.blt(self.x, self.y,0,0, 136,8,8,5 )

        if status == 'Left':
            pyxel.blt(self.x,self.y,0, 0,144,8,8,5)
            
            
Game()
