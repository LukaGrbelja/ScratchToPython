import math
import time

import engine
from engine.events import *
from engine.operators import *
from engine.types import *
'''
import pymongo

#Spajanje na bazu podataka
myclient = pymongo.MongoClient('mongodb+srv://<USERNAME>:<PASSWORD>@<CLUSTERNAME>')
mydb = myclient["mydatabase"]

#Stvaranja kolekcije odnosno tablice u bazi
userCollection = mydb["users"]

username = input()
'''

@sprite('Stage')
class Stage(Target):
    """Sprite Stage"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 0
        self._ypos = 0
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 100, "None", [
            {
                'name': "pozadina1",
                'path': "87ec29ad216c0074c731d581c7f40c39.svg",
                'center': (240, 180),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])

        self.var_Scrollx = 0
        self.var_Score = 0
        self.var_Health = 1



        self.sprite.layer = 0




@sprite('Lik1')
class SpriteLik1(Target):
    """Sprite Lik1"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 0
        self._ypos = -100
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           1, 100, "all around", [
            {
                'name': "kostim1",
                'path': "702d6b19295a4135a0cd6c49606e2a44.svg",
                'center': (48, 50),
                'scale': 1
            },
            {
                'name': "kostim2",
                'path': "6f0c9b9f05092d28f36191d7e68d84a3.svg",
                'center': (46, 53),
                'scale': 1
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "Meow",
                'path': "83c36d806dc92327b9e7049a565c6bff.wav"
            }
        ])





        self.sprite.layer = 2

    @on_green_flag
    async def green_flag(self, util):
        util.sprites.stage.var_Scrollx = 0
        await util.send_broadcast_wait("setup")
        util.send_broadcast("player loop")
        util.send_broadcast("camera loop")
        util.send_broadcast("background loop")
        util.send_broadcast("other loops")

    @on_broadcast('player loop')
    async def broadcast_playerloop(self, util):
        self.gotoxy(0, -100)
        while True:
            if util.inputs["right arrow"]:
                self.xpos += 8
            if util.inputs["left arrow"]:
                self.xpos += -8
            if self.get_touching(util, "Heart"):
                util.sprites.stage.var_Score += 1
                self.xpos += -8
            if self.get_touching(util, "Knight"):
                util.sprites.stage.var_Health += -1
                self.xpos += 8

            await self.yield_()

    @on_broadcast('camera loop')
    async def broadcast_cameraloop(self, util):
        while True:
            if gt(self.xpos, 0):
                util.sprites.stage.var_Scrollx += 8
                self.xpos += -8
            if lt(self.xpos, 0):
                util.sprites.stage.var_Scrollx += -8
                self.xpos += 8

            await self.yield_()

    @on_broadcast('other loops')
    async def broadcast_otherloops(self, util):
        while True:
            if gt(1, util.sprites.stage.var_Health):
                '''
                #MongoDB: Update high score

                ###Provjerava postoji li korisnik, ako postoji vrati podatke o njemu
                searchQuery = { "username": username }
                existingUser = userCollection.find_one(searchQuery)

                ###U slučaju da korisnik postoji
                if existingUser:
                    ###Provjera je li završni score veći od prethodno zabilježene highscore vrijednosti
                    if int(util.sprites.stage.var_Score) > int(existingUser["highscore"]):
                        ##Ako je podatci odd korisnika se ažuriraju s novom highscore vrijednošću
                        newValues = { "$set": { "highscore": int(util.sprites.stage.var_Score) } }
                        userCollection.update_one(searchQuery, newValues)
                ###U slučaju da korisnik ne postoji
                else:
                    ###Zabilježi novog korisnika u kolekciju
                    newUser = { "username": username, "highscore": int(util.sprites.stage.var_Score) }
                    userCollection.insert_one(newUser)
                '''
                util.stop_all()
                return None

            await self.yield_()


@sprite('scratchBackground')
class SpritescratchBackground(Target):
    """Sprite scratchBackground"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 480
        self._ypos = 0
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 120, "all around", [
            {
                'name': "scratchBackground",
                'path': "0cef7fbb1cecedc552ee2a3f7a1d7d34.png",
                'center': (480, 360),
                'scale': 2
            }
        ])

        self.sounds = Sounds(
            100, [

        ])

        self.var_levelx = 480



        self.sprite.layer = 1

    @on_broadcast('setup')
    async def broadcast_setup(self, util):
        util.sprites.stage.var_Health = 1
        self.gotoxy(0, 0)
        self.costume.switch("scratchBackground")
        self.var_levelx = 0
        self.create_clone_of(util, "_myself_")
        self.costume.next()
        self.var_levelx += 480

    @on_broadcast('background loop')
    async def broadcast_backgroundloop(self, util):
        while True:
            self.xpos = (self.var_levelx - util.sprites.stage.var_Scrollx)

            await self.yield_()

    @on_broadcast('background loop')
    async def broadcast_backgroundloop1(self, util):
        while True:
            self.xpos = (self.var_levelx - util.sprites.stage.var_Scrollx)

            await self.yield_()


@sprite('Heart')
class SpriteHeart(Target):
    """Sprite Heart"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = 289
        self._ypos = -100
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 100, "all around", [
            {
                'name': "heart red",
                'path': "aac67ac6d6f7f62e12b409326d914045.svg",
                'center': (65, 56),
                'scale': 1
            },
            {
                'name': "heart purple",
                'path': "ffd0ff12e90de0463126e8b1060077fe.svg",
                'center': (66, 62),
                'scale': 1
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])

        self.var_levelx = 400



        self.sprite.layer = 3

    @on_broadcast('background loop')
    async def broadcast_backgroundloop(self, util):
        while True:
            self.xpos = (self.var_levelx - util.sprites.stage.var_Scrollx)

            await self.yield_()

    @on_broadcast('setup')
    async def broadcast_setup(self, util):
        self.gotoxy(400, -100)
        self.var_levelx = 400


@sprite('Knight')
class SpriteKnight(Target):
    """Sprite Knight"""

    def __init__(self, parent=None):
        super().__init__(parent)
        if parent is not None:
            return

        self._xpos = -200
        self._ypos = -100
        self._direction = 90
        self.shown = True
        self.pen = Pen(self)

        self.costume = Costumes(
           0, 100, "all around", [
            {
                'name': "knight",
                'path': "ced8541c52032a702ab623524ab37dc9.svg",
                'center': (75, 75),
                'scale': 1
            }
        ])

        self.sounds = Sounds(
            100, [
            {
                'name': "pop",
                'path': "83a9787d4cb6f3b7632b4ddfebf74367.wav"
            }
        ])

        self.var_levelx = -200



        self.sprite.layer = 4

    @on_broadcast('setup')
    async def broadcast_setup(self, util):
        self.gotoxy(-200, -100)
        self.var_levelx = -200

    @on_broadcast('background loop')
    async def broadcast_backgroundloop(self, util):
        while True:
            self.xpos = (self.var_levelx - util.sprites.stage.var_Scrollx)

            await self.yield_()




if __name__ == '__main__':
    engine.start_program()
