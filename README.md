# 1D-Collision-Simulator
A simplistic 1D collision simulator based around the law of conservation of momentum and transferal of kinetic energy.

The program simulates 1D simulations of two or more objects colliding with each other. The user may control the program using the following controls:

Space can be used to pause and unpause the simulation, while R resets the simulation entirely.

Pressing P will bring up a menu in the console, where the user may change statistics such as the coefficient of restitution, whether or not the walls or text above objects should be present, and also add in new objects.

Finally, clicking on an object will bring up its statistics, including mass, size, x position, and velocity. Any of these can be edited, and the object can be removed as well through this menu.

When an edit is done to the simulation from its initial state (after R is pressed), then that new setup becomes the simulation's initial state. However, if an edit is done mid-simulation, then that edit is not preserved if the simulation is brought back to its initial state.
