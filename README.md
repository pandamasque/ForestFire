# Fire Spread Percolation Computer

This is a fire spread percolation computer with an integrated GUI. It works by simulating a forest burning with different types of fire or spreading. Them it compute how much of the forest actually burned. And display a percolation curve of the forest density. Notice that some configurations give not so good results for the final curve.

## Using the interface

First of when you launch the app, you will be able to choose the spreading type and the fire type. You will also be able to configure the number of simulation and the sampling of trees density.

Then when all parameters are selected you can push the "START" button in order to start the simulation. A progress bar will be shown to visualize the time remaining.

Once the computation is over, the percolation curve is displayed in a new window.
 
## How it works

The simulator works by recursively litting on fire the trees that are in its surronding according to the fire choosen. The functions the user can choose from decide on the behaviour of the fire or the surrounding that is used.
