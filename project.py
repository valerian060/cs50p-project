import random
import re
import sys
import art
import pyfiglet
import csv
class Mob():
      def __init__(self,name,hp,equipped,fire=0,ice=0,phy=0,pres=0,ires=0,fres=0,choice=''):
            self.name=name
            self.hp=hp
            self.equipped=equipped
            self.fire=fire
            self.ice=ice
            self.phy=phy
            self.pres=pres
            self.ires=ires
            self.fres=fres
            self.choice=choice
      @classmethod
      def spawn(cls):
                golem=cls('Golem',10,'Quake',phy=4,pres=9,choice='P')
                firewiz=cls('Fire Wizard',5,'Burn',fire=5,choice='F')
                bandit=cls('Bandit',2,'Lunge',phy=1,choice='P')
                return [golem,firewiz,bandit]


class Player(Mob):
      def __init__(self,name='Player',equipped='',hp=10,fire=0,ice=0,phy=1,pres=0,ires=0,fres=0):
            super().__init__(name,hp,equipped,fire,ice,phy,pres,ires,fres)
            self.inventory=[]
            self.x=0
            self.y=0
            self.gold=0
            self.finger=0
            self.skill='None'
            self.flag=0
      @property
      def finger(self):
           return self._finger
      @finger.setter
      def finger(self,n):
           if n==10:
                print('''\nSukuna:"I'll show you what real jujutsu is"\n''')
                print(art.sukuna())
                sukuna(self)
           else:
                self._finger=n
      def __str__(self):
               return(f'HP-->{self.hp}\nGold-->{self.gold}\n{self.inventory}\nSkill-->{self.skill}\nEquipped-->{self.equipped}\n')
      def equip(self,item):
            swords = {'Steel Sword': 3,'Katana': 5,'Claymore': 7,'Falchion': 6,'Rapier': 4,'Cutlass': 5}
            jujutsu={'Hollow Purple':100,'Slice':30,'Slash':40}
            food={'Apple':1,'First Aid':3,'Med Kit':5,'RCT':10}
            if item in swords and item in self.inventory:
                  self.phy=swords[item]
                  self.equipped=item
                  return(f'You Equipped {item}.')
            if item in jujutsu and item in self.inventory:
                  self.phy=self.fire=self.ice=jujutsu[item]
                  self.equipped=item
                  return(f'You Equipped {item}.')
            if item in food and item in self.inventory:
                 self.hp=self.hp+food[item]
                 self.inventory.remove(item)
                 return(f'HP-->{self.hp}')
            if item=='Finger' and item in self.inventory:
                 self.finger=self.finger+1
                 self.inventory.remove('Finger')
                 return(f'You Have Consumed {self.finger}.')
            if item in ['Infinite Void','Malevolent Shrine'] and item in self.inventory:
                 self.skill=item
                 return(f'You Are Now Able To Use {item}.')
            else:
                 return("I don't think you have the facilities for that big man.")
      def loot(self,items):
            for item in items:
                 self.inventory.append(item)
      def move(self,x,y):
            self.x=self.x+x
            self.y=self.y+y

def spawn(n):
        coordinate=[]
        for _ in range(n):
           coordinate.append([random.randint(-10,10),random.randint(-10,10)])
        return coordinate
def encounter(player,coordinates,*args):
      (golem,firewiz,bandit)=args
      for item in coordinates:
           if [player.x,player.y] in coordinates[item]:
                match item:
                     case 'fingers':
                          event(player)
                     case 'bandit':
                          print('A Bandit Tries To Rob You Of Your Wares.')
                          match (input('Y-To Handover All Your Gold,N-Battle: ').upper()):
                               case 'Y':
                                    player.gold=0
                                    return('You Lost All Your Gold')
                               case 'N':
                                    return(battle(player,bandit))
                     case 'golems':
                          print('You Ran Into A Golem.')
                          return(battle(player,golem))
                     case 'firewiz':
                          print('You Come Across A Wizard Wielding Flames')
                          return(battle(player,firewiz))

                     case 'chests':
                          return(chest(player))
                     case 'Home':
                          return(sys.exit('Home Sweet Home'))
      return('Onwards')

def move(player,roll):
      dir=input('Where Next? ').lower().strip()
      if match:=re.match(r'(\d+).+(left|right).+(\d+).+(up|down)',dir):
            x=int(match.group(1))
            y=int(match.group(3))
            if (x+y)<=roll:
               if match.group(2)=='left':
                  x=-x
               if match.group(4)=='down':
                  y=-y
               player.x=player.x+x
               player.y=player.y+y
            else:
                 print('X left|right and Y up|down')
                 move(player,roll)
      else:
           print('X left|right and Y up|down')
           move(player,roll)
def compass(player,home):
     x1,y1=player.x,player.y
     x2,y2=home[0],home[1]
     x='West'
     y='South'
     distance=int(((x1 - x2)**2 + (y1 - y2)**2)**0.5)
     try:
          m=(y2-y1)/(x2-x1)
     except ZeroDivisionError:
          if y2>y1:
               return(f'{distance} To The North')
          else:
               return(f'{distance} To the South')
     if m==0:
          if x2>x1:
               return(f'{distance} To The East')
          else:
               return(f'{distance} To The West')
     if x2>x1:
          x='East'
     if y2>y1:
          y='North'
     return(f'{distance} To The {y}-{x}')
def battle(player,mob):
     hp=mob.hp
     flag=0 #initalizing the flag variable that tells whether a domain has been used or not.
     while(True):
          match input('A to Attack,F to Flee,E to Change/Use Items,D to Use Domain Expansion: '):
               case 'A':
                     print(f'You-->{player.hp}')
                     print(f'{mob.name}-->{hp}')
                     choice=input('P for Physical,I for Ice,F for Fire: ')
                     hp=attack(player,mob,hp,choice)
                     print(f'{mob.name}-->{hp}')
               case 'F':
                    n=random.randint(0,10)
                    if n<6:
                         return('You Escaped')
                    else:
                         sys.exit('You slipped and fell into the hands of a hungry flesh eating hamster.')
               case 'E':
                    art.type(f'{player}')
                    print(player.equip(input('Enter Item Name:')))
               case 'D':
                    if flag==0 and player.skill!='None':
                         turns=0
                         player,n,flag1=domain(player)
                         print(n)
                         flag=1
                    elif player.skill=='None':
                         art.type('\nYou do not have a domain.\n')
                    else:
                         print('Domain Expansion Has Already Been Used.')
          if flag==1:
               turns=turns+1
               if flag1==0 and turns==3:
                    player.phy=99999
                    print('3 Turns Have Lapsed The Domains Guarenteed Hit Will Now Take Effect')
                    hp=attack(player,mob,hp,'P')
                    player.phy=n
               elif flag1==1 and turns==3:
                    player.hp=n
                    print('You Have Run Out Of Cursed Energy')
          if(hp<=0):
               print('You Are Victorious')
               return(chest(player))
          player.hp=attack(mob,player,player.hp,mob.choice)
          print(f'You-->{player.hp}')
          if player.hp<=0:
               sys.exit('You Died')
def attack(attacker,defender,hp,choice):
     match choice:
          case 'P':
               if attacker.phy>defender.pres:
                    hp=hp+defender.pres-attacker.phy
          case 'I':
               if attacker.ice>defender.ires:
                    hp=hp+defender.ires-attacker.ice
          case 'F':
               if attacker.fire>defender.fres:
                    hp=hp+defender.fres-attacker.fire
          case _:
               print('Invalid Input')
               choice=input('P for Physical,I for Ice,F for Fire: ')
               attack(attacker,defender,hp,choice)
     print(f'{attacker.name} Used {attacker.equipped}')
     return hp
def chest(player):
     chest=['Steel Sword','Katana','Hollow Purple','Med Kit','Apple','RCT','First Aid']
     n=random.choices([1,2,3],weights=[50,30,20])
     print(f'You Found A Level {n} Chest')
     for lvl in n:
          items=random.choices(chest,[65/lvl,30-lvl,25+lvl,30+lvl,60/lvl,25+lvl,30-lvl],k=4)
     player.loot(items)
     return(f'You Found {items}')
def dice():
     return(random.randint(1,6))
def merchant(player):
     wares={'Steel Sword':5,'Katana':20,'Hollow Purple':70,'Med Kit':5,'Apple':1,'RCT':50,'First Aid':10,'Finger':1}
     match input('B-Buy,S-Sell:').upper().strip():
          case 'B':
               art.type('You Have The Gold...I Have The Wares:\n')
               for item in wares:
                    print(f'{item}-------{wares[item]} Gold')
               buy=input('Your Choice:' )
               try:
                    if player.gold<wares[buy]:
                       art.type("\nSeems You Don't Have Enough\n" )
                    else:
                       player.loot([buy])
               except:
                    art.type("Seems You Don't Have Enough\n")
          case 'S':
               n=random.choices([0.5,0.75,1],weights=[50,30,20])
               art.type(f'Lets See What You Have:{player.inventory}\n')
               print(f'The Merchant Buys At {n[0]*100}%.')
               sell=input('What Do You Want To Sell:')
               if sell in player.inventory:
                    print(f'{wares[sell]*n[0]} Is The Best I Can Offer')
                    choice=input('Y/N:').upper().strip()
                    if choice=='Y':
                         player.inventory.remove(sell)
                         player.gold=int(player.gold+(wares[sell]*n[0]))
                    else:
                         print("Well Your Loss.")
          case _:
               return player
     return player
def event(player):
          events=[{'event': '''You traverse a desolate canyon, the ground littered with bleached bones and whispering wind.\nIn the distance, a shimmering portal pulses with an unnatural light. \nAs you approach, a disembodied voice echoes from the portal:\n"I have no shape, yet I hold all things. I have no voice, yet I whisper to the stars. I have no end, yet I am filled with echoes. What am I?"''','prompt': '''Do you attempt to answer the riddle and enter the portal, or seek another path?(Y/N)''','ans': 'Y','e1': answer_void_riddle,'e2': seek_other_path},{'event':'''You stumble upon a peculiar object lying in your path. As you draw closer, you gasp in surprise. It's a severed finger, gnarled and wrinkled, with an eerie glow emanating from beneath its pale skin. An unsettling feeling washes over you, but a strange curiosity tugs at your mind.\nA voice whispers in your head, "Consume it... Unleash its power...''','prompt':'Do you dare to eat the strange finger?\nY or N:','ans':'Y','e1':finger,'e2':no_finger}]
          if player.flag==1:
               events.pop(0)
          item=random.choice(events)
          art.type(f"{item['event']}\n{item['prompt']}:")
          choice=(input()).upper()
          if choice==item['ans']:
               item['e1'](player)
          else:
               item['e2'](player)
          return(player)
def answer_void_riddle(player):
     player.flag=1
     i=0
     art.type('''\nYou step through the shimmering veil, a tremor of anticipation twisting in your gut. The voice from the portal fades, replaced by an unsettling silence that stretches on like an endless night. You stand on a plain of obsidian glass, reflected in the inky sky above. Around you, whispers rise from the ground, whispers of lost souls, yearning cries echoing in the void.\nAs the whispers coalesce, figures begin to flicker into existence. Twisted silhouettes, visages of pain and fury, their vacant eyes burning with cold fire. A thousand, no, a million cursed spirits surge towards you, a tide of darkness hungry for oblivion. Your heart clenches. Had you been so arrogant? You wished, with a burning intensity, that you'd chosen the other path.\nBut regret is a luxury the living hold. There's no path back. Only the steel in your grip and the fire in your veins. You raise your blade, a silent promise against the storm.\n''')
     while(player.hp>10):
          i=i+1
          if(i>5):
               break
          print(i)
          name=random.choice(['Yasohachi Bridge Curse','Finger Bearers','Rainbow Dragon','Dbubus'])
          attack=random.choice(['Blood Lust','Strike','Smash',])
          battle(player,mob=Mob(name,8,attack,phy=4,choice='P'))
     art.type('''\nThe first blows crash like thunder. You spin, parry, riposte, a whirlwind of desperate dance against the encroaching shadows. Each clang of metal against their spectral forms sparks with fleeting agony, a glimpse of humanity trapped within the cursed husks. But the horde is endless, a black wave washing over you, dragging you down into the abyss.\nJust as your strength falters, the world warps. Time stretches, slows, then shatters. You see glimpses of yourself, countless echoes scattered across this infinite emptiness. Each echo, a life lived, a choice made, a thread woven into the tapestry of existence. You see triumph and failure, joy and sorrow, all interconnected, echoing through the void.\nIn that maelstrom of memories, you understand. The void is not an absence, but a canvas brimming with potential. It is the space between breaths, the silence between notes, the infinite tapestry of possibilities. And within that infinity, you find a spark, a flicker of defiance.\nYour blade sings anew, its rhythm echoing across the void. Every parry, every riposte, becomes a brushstroke on that infinite canvas. You dance not just for your life, but for the endless tapestry itself, weaving a defiant song against the silence.\nThe tide begins to turn. The spirits falter, their cries turning into whimpers, their forms fading like smoke. As the last echo disintegrates, you stand panting, battered but unbroken. The obsidian plain shimmers, and the portal reopens.\nYou step back through, forever changed. The world seems brighter, the whispers of the wind carrying new meaning. You have stared into the void, and the void has stared back. And in that confrontation, you have discovered your own infinity, the spark of defiance that dances in the face of oblivion.\nThe path ahead is still uncertain, but you walk with a newfound purpose. You are a weaver of the void, a melody in the silence, a testament to the infinite resilience of the human spirit. The echoes of your battle will resonate through the void, a whispered reminder that even in the darkest corner, the light of courage can still burn.\nThis is just the beginning of your journey, forever marked by your dance with the cursed spirits and your embrace of infinity. The void may lurk in the shadows, but you now hold the brush, ready to paint your own story on its eternal canvas.\n''')
     player.loot(['Infinite Void'])
     art.type(f"\n{player.equip('Infinite Void')}\n")
def seek_other_path(player):
     ...
def finger(player):
     player.loot(['Finger'])
     print(player.equip('Finger'))
def no_finger(player):
     player.loot(['Finger'])
def sukuna(player):
     sukuna=Player('Sukuna',hp=100)
     attacks=random.choice(['Slice','Slash'])
     sukuna.inventory.append(attacks)
     sukuna.equip(attacks)
     sukuna.equipped=attacks
     flag=0
     t=0
     while(True):
          match input('A to Attack,F to Flee,E to Change/Use Items,D to Use Domain Expansion: '):
               case 'A':
                     print(f'You-->{player.hp}')
                     print(f'{sukuna.name}-->{sukuna.hp}')
                     choice=input('P for Physical,I for Ice,F for Fire: ')
                     sukuna.hp=attack(player,sukuna,sukuna.hp,choice)
                     print(f'{sukuna.name}-->{sukuna.hp}')
               case 'F':
                    n=random.randint(0,10)
                    if n<6:
                         return('You Escaped')
                    else:
                         sys.exit('You slipped and fell into the hands of a hungry flesh eating hamster.')
               case 'E':
                    art.type(f'{player}')
                    print(player.equip(input('Enter Item Name:')))
               case 'D':
                    if flag==0 and player.skill!='None':
                         turns=0
                         player,n,flag1=domain(player)
                         flag=1
                    else:
                         if flag==1:
                              art.type('\nDomain Expansion Has Already Been Used.\n')
                         elif player.skill=='None':
                              art.type('\nYou Do Not Have A Domain\n')


          if flag==1:
               turns=turns+1
               if flag1==0 and turns==3:
                    player.phy=99999
                    print('3 Turns Have Lapsed The Domains Guarenteed Hit Will Now Take Effect')
                    sukuna.hp=attack(player,sukuna,sukuna.hp,'P')
                    player.phy=n
               elif flag1==1 and turns==3:
                    player.hp=n
                    print('You Have Run Out Of Cursed Energy')
          if(sukuna.hp<=0):
               print('You Are Victorious')
               art.type("You Now Have Control Over Sukuna's Technique")
               return(player.loot(['Slice','Slash','Malevolent Shrine']))
          if t>=1:
               if t==3:
                    phy=sukuna.phy
                    print('3 Turns Have Lapsed The Domains Guarenteed Hit Will Now Take Effect')
                    sukuna.phy=9000
                    player.hp=player.hp+player.pres-sukuna.phy
                    sukuna.phy=phy
               else:
                    t=t+1

          player.hp=player.hp+player.pres-sukuna.phy
          print(f'{sukuna.name} Used {sukuna.equipped}')
          offense=['Slice','Slash','Malevolent Shrine']
          attacks=random.choice(offense)
          sukuna.inventory.append(attacks)
          if attacks=='Malevolent Shrine':
               sukuna.skill='Malevolent Shrine'
               print('Domain Expansion: Malevolent Shrine.\n You Can Only Counter It With Your Own Domain or Survive.')
               n=sukuna.phy
               t=1
               offense.remove('Malevolent Shrine')
          sukuna.equip(attacks)
          sukuna.equipped=attacks
          print(f'You-->{player.hp}')
          if player.hp<=0:
               sys.exit('You Died')
def domain(player):
     match player.skill:
          case 'Infinite Void':
               print(player.hp)
               n=player.hp
               player.hp=9999
               flag=1
          case 'Malevolent Shrine':
               flag=0
               n=player.phy
     return player,n,flag
def create_save(player):
     name=input('Enter Save Name: ')
     with open('save.csv','a') as file:
          writer=csv.DictWriter(file,fieldnames=['save','inventory','equipped','skill','fingers','flag','phy','fire','ice','hp','gold'])
          writer.writerow({'save':name,'inventory':player.inventory,'equipped':player.equipped,'skill':player.skill,'fingers':player.finger,'flag':player.flag,'phy':player.phy,'fire':player.fire,'ice':player.ice,'hp':player.hp,'gold':player.gold})
def load_save(player):
     with open('save.csv') as file:
          reader=csv.DictReader(file,fieldnames=['save','inventory','equipped','skill','fingers','flag','phy','fire','ice'])
          for row in reader:
               print(f"{row['save']}',end=' '")
          art.type('\nPlease choose the save you wish to load\n')
          save=input().strip()
     with open('save.csv') as file:
          reader=csv.DictReader(file,fieldnames=['save','inventory','equipped','skill','fingers','flag','phy','fire','ice','hp','gold'])
          for row in reader:
               if row['save']==save:
                    player.inventory=(row['inventory']).replace('[','').replace(']','').replace("'",'').split(sep=', ')
                    player.equipped=row['equipped']
                    player.skill=row['skill']
                    player.fingers=int(row['fingers'])
                    player.flag=int(row['flag'])
                    player.phy=int(row['phy'])
                    player.fire=int(row['fire'])
                    player.ice=int(row['ice'])
                    player.hp=int(row['hp'])
                    player.gold=int(row['gold'])
                    return('Save Loaded')
          return('Invalid Save')
def main():
      mobs=Mob.spawn()
      player=Player(hp=50,phy=9)
      home=spawn(1)
      coordinates={'Home':home,'chests':spawn(100),'golems':spawn(80),'firewiz':spawn(100),'bandit':spawn(100),'fingers':spawn(100)}
      player.loot(['Katana'])
      player.equip('Katana')
      art.type(pyfiglet.figlet_format('HOME'))
      art.type("\nSun bled through leaves, painting your skin with fleeting warmth. Each rustle, every snap amplified the silence, pressing in like emerald walls. Lost. Hours? Days? Panic nipped, but you squared your shoulders, a half-eaten jerky your only comfort. This forest wouldn't break you. Not today. You were more than lost, you were a survivor, and dawn would find you, carved from the wilderness itself.\n")
      while True:
           art.type('\nI-Inventory,C-Compass,E-Equip,M-Merchant,Exit-Exit,Save-Save/Load: ')
           match input().upper():
                case 'I':
                     art.type(f'{player}')
                case 'C':
                     print(compass(player,*home))
                case 'E':
                     print(player.equip(input('Enter Item Name:')))
                case 'M':
                     player=merchant(player)
                case 'EXIT':
                     sys.exit('Thank You.')
                case 'SAVE':
                     match input('S-To Save,L to Load: '):
                          case 'S':
                               create_save(player)
                          case 'L':
                               art.type(load_save(player))
                case _:
                     roll=dice()
                     art.type(f'You rolled {roll}\n')
                     move(player,roll)
                     print(player.x,player.y)
                     print(encounter(player,coordinates,*mobs))
if __name__=='__main__':
     main()




