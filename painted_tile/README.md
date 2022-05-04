## Problem Statement
In the Tile Painting planning domain, a robotos paints tiles according to a certain color pattern. The robots can move to an adjacent tile unless that tile is painted. They can also color the tile adjacent to them using their spray gun if it is not painted or occupied.

We are given the initial location of the robot, and which tiles should be painted in the given colors. There are tow kinds of actions:

1. Robot at tile T1 paints tile T2:
   * SetRed(T1,T2):
      * **Preconditions**: At(T1)&Adj(T1,T2)&*not*Red(T2)&*not*Blue(T2)
      * **Effects**: Red(T2)
   * SetBlue(T1,T2):
      * **Preconditions**: At(T1)&Adj(T1,T2)&*not*Red(T2)&*not*Blue(T2)
      * **Effects**: Blue(T2)
2. Robot goes from tile T1 to tile T2:
   1. Move(T1, T2):
      1. **Precondtions**: At(T1)&Adj(T1,T2)&*not*Blue(T2)&*not*Red(T2)
      2. **Effects**: At(T2)

A tile of type T can be any of the 25 tiles, t0, ..., t24

## Run directory
```txt
D:\source\repos\ai\painted_tile\pokorie.bat
```