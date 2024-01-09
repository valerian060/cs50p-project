# 'HOME'-A TEXT BASED ADVENTURE GAME
#### Video Demo:  <https://youtu.be/5p2PO9lPp4c>
#### Description:
A Text-Based adventure game where your objective is to reach your home, along the way encountering events spawned randomly on a 2-D coordinate axis.
## About The Program
#### Mob( ) Class
Creates instances/objects of the Mob class that represent in-game enemies with attributes hp,name,equipped item,elemental attacks and resistances.
The spawn function is a class method in the mob class that spawns mobs i.e instances of the Mob class,it returns a list of said instances.
### Player( ) Class
The Player() class inherits the \__init__( ) class from its super class Mob,and has some of its own attributes, namely:

__inventory__:A list of items the player possesses.

__x and y__ :The co-ordinates of the player.

__gold__:The amount of gold the player possesses.

__finger__:The number of fingers the player possesses,with a setter and getter that limits them to 10,on which a hidden boss is triggered.

__skill__:The skill the player has equipped.

The Player class also has some of its own functions:

__equip( )__: Equips Items on the condition that they are also in the players inventory.

__loot( )__: Updates player inventory.

__move( )__: Updates player position.

__finger(self,n)__:setter for finger attribute, calls sukuna() when fingers exceed 10.




### spawn(n)
Returns a list of coordinates in x and y axis of length n.

### encounter(player, coordinates, *args)
Takes the player, coordinates and a list of mobs as arguments, it then iterates over the 'coordinates' key and checks if the player's current position matches that of the key-value using a match case conditional branching statement,if none of the keys have coordinates matching
then defaults to "onwards".

### move(player, roll)

Function that handles player movement on the axis,roll is the dice roll. Uses match() from the re library to validate and parses the user input, extracting information related to user choice of movement using the group() function from the re library.

### compass(player, home)

This function takes the player instance and coordinates of home as arguements, returning the distance calculated using the distance formula and its direction by the slope of the line connecting the players current position and home.

### battle(player, mob)

This function handles turn-based combat in the game, taking two arguements, the first parameter is the player instance and the second being an instance of the Mob() or Player() class. Makes use of match case to give the player 4 options, A to attack,F to flee,E to change/equip items,D to use domain expansion, domain expansion can only be used once in a fight for which I have used the flag variable.

The __Attack__ option calls the attack() function,which returns the second parameter's hitpoints, the reason I store this return value in the hp variable is so that the mob's hp attribute remains unchanged, and all changes are solely reflected on the temporary hp variable.

The __Domain__ option triggers a domain, that provides stat buffs to the player, on use the flag variable is set to 1, thus preventing repeated use, also starts a turn counter.

The __Flee__ option uses the randint() function from the random library, generating a number depending on which the evasion is successful or not.

### attack(attacker, defender, hp, choice)
Handles damage calculation factoring the players type of attack,the damage it deals,and factors the defenders resistances to that particular element, returns the resulting hp of the adversary.

### chest(player)
Rewards the player with a chest with randomised drops, I have made use of the random library and its weight parameter to simulate this, the items are added to the inventory attribute of the player.

### dice(player)
Returns a random number from 1 to 6.

### merchant(player)
This function allows the player to purchase/sell wares from/to the merchant, uses a dict with key-value pairs of item name and its value. The merchant also buys at randomly decided rates, using the random.choices() function from the random library.

### event(player)
This functions handles events the player may encounter in game, these are stored in a dictionary, with keynames, event, prompt, ans(the correct answer that triggers the event), e1 and e2(outcomes).To prevent certain one time events from being triggered I have used the flag attribute of the Player class.
The dictionaries structure provides a framework for adding more events.

### answer_void_riddle(player)
This function handles the void event, I have used a while loop to simulate the player battling a horde of enemies, and used a list to randomise attacks and enemy names.


### seek_another_path(player)
This a placeholder function for the alternate choice for the void event.

### finger(player) and no_finger(player)
These are the outcome functions for the finger event.

### sukuna(player)
This is the function for the hidden boss battle, it is like the battle(player) but allows the boss to use varying attacks, using a list and like the player use domains, another element in the games battle system, inspired by the series Jujutsu Kaisen.

### domain(player)
This function handles the domain aspect of the combat system, uses match case to decide between the two available domains in the game, returning the original value of the changed parameter,the player object and a flag that signifies which skill was used.

### create_save(player) and load_save(player)
This function provides the ability to save games, for this I have used a csv file and the DictReader and DictWriter functions to write and parse the strings from the resulting csv.

### art.py
This python file has the functions type(text) and sukuna(), the type function uses sleep function from the time module for a typing effect, the sukuna() returns an ASCII art of the games hidden boss.

### main()
This is the main function, creates the player instances and mob instances, and a dictionary of coordinates, the dictionary consists of key-values pairs of the points of interest as key names and their list of coordinates from the spawn(n) function.

I have made use of an infinite while loop and match case to give the user options,
>  art.type('\nI-Inventory,C-Compass,E-Equip,M-Merchant,Exit-Exit,Save-Save/Load: ')

By default the roll() is called followed by the move(player) function.