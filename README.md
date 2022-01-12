# Qix

#Requirements

Display
- The display holds the information relevant to the player’s status in the game. The requirements are as follows:
- The display shows the play’s remaining life force.
- The display shows a percentage of the field that has been claimed by the player.
- The display shows the Qix logo.
- The display shows the total points accumulated

Player
- The functions the player will perform: 
- When the player is not in a push, it must move along the white lines
- When the player is in a push, it can move into the field and create an incursion 
- There are two types of pushes: slow and fast, where the slower push accumulates more points.
- The Player must lose lifeforce when they come in contact with an enemy. If the player is still in the game during a push, they will return to their starting position from when     the push first began.

Enemies
- The enemies in this game are split into two categories: Qix and Sparc. The functionalities for each of these are:

Qix
- Qix only moves through valid areas of the field in a random direction.
- Qix upon collision with the player will reduce the player’s lifeforce
- Qix upon collision with the stix will reduce the player’s lifeforce 
- Qix should die upon being entrapped

Sparc
- Sparc only moves along the white lines in the field
- Sparc upon collision with the player will reduce the player’s lifeforce
- Sparc upon collision stix will stop the current push 
- Sparc should die and respawn upon being entrapped 
