# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
import pyxel
import time


class Player:
    def __init__(self,x,y):
        self.vie = 3
        self.vitesse = 1
        self.direction = 0
        self.x = x
        self.y = y
        self.gravite = 1
        self.puissance_saut=7
        self.vel_y=0
        self.grounded=True
        self.game_over = False
        
    
    def update(self):
        pyxel.camera(self.x -128 ,self.y-128)
        self.vel_y += self.gravite
        self.y = self.y + self.vel_y
        
 
        

            
        if pyxel.btn(pyxel.KEY_D):
            self.x = (self.x + 2)
        if pyxel.btn(pyxel.KEY_Q):
            self.x = (self.x - 2)
            
        if pyxel.btn(pyxel.KEY_SPACE):
            self.vel_y = -self.puissance_saut
            
        
            
        
        
        
        
        
        
        
        
        
        
        
        """
        print(self.grounded)
        self.vel_y=0
        if self.y <= 120:
            self.y = (self.y + self.gravite)
            if self.y >120:
                self.saut = True
        if pyxel.btn(pyxel.KEY_D):
            self.x = (self.x + 2)
        if pyxel.btn(pyxel.KEY_Q):
            self.x = (self.x - 2) 
        if pyxel.btn(pyxel.KEY_SPACE) and self.grounded:
            self.vel_y+=self.puissance_saut
            self.grounded = False

        self.y-=self.vel_y
        
            
            
        if self.y + 60 >= pyxel.height:
            self.y = pyxel.height - 60
            self.vel_y = 0
            self.grounded = True
         """      
        





class App:
    def __init__(self):
        pyxel.init(256, 256, title="Nuit du Code")
        pyxel.load("2.pyxres")
        self.player = Player(60,0)
        pyxel.run(self.update, self.draw)
        
        
    def update(self):
        self.player.update()

    
    def draw(self):
        pyxel.cls(5)
        pyxel.bltm(0,0,0,0,225,3000,256)
        
        pyxel.blt(self.player.x,self.player.y,0,0,8,16,16,5)
        """pyxel.rect(self.x, self.y, 8, 8, 9)"""
App()