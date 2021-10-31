Try it out at [**zachpetersendev.com/picarioGame**](http://zachpetersendev.com/picarioGame/)

You are a fruit. Eat the tiny dots to grow bigger, or eat other fruit that are smaller than you. Just make sure that none of the larger fruits eat you! Works on anything that can run a web browser.

Controls:
Arrow Keys : Move
Mouse : Click and hold to move in direction of cursor
Touchscreen : Touch and hold to move in that direction

This is a proof of concept game made by Dylan Tran, Zachary Petersen, John Chau, and Sterling Salvaterra. Special thanks to our amazing instructor Adam Smith at UC Santa Cruz for his advice and encouragement.

Our goal was to show that the PICO-8 can support a relatively massive number of simultaneous players in a single game given its constraints. We decided to recreate the popular agar.io to achieve this goal.

In our largest test, we had 35+ simultaneous players. Theoretically, the game can handle 64+ simultaneous players.

One of the biggest challenges we faced is that there are only 128 bytes of GPIO in the PICO-8 meaning that the each client can only handle take in 128 bytes of Input/Output per frame. We decided to represent each object with six bytes, one for ID, one for size, two for X Coordinate, and two for Y Coordinate. With 128 bytes of I/O, that meant we could update 21 objects per frame. We designated three of these objects to output (The client telling the server about changes in the player's state and the state of any objects the player eats) and the other 18 to Input (The server telling the client about the change of objects in the world).

We wrote the server in python. Since the clients can only handle 18 updated objects per frame, we implemented a spatial hashing optimization so that each client only receives updates about objects that are nearby the player. The connection between the clients and the server is made using websockets.

