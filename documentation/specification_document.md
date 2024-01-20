# Project Specification Document

## Project Description

Degree programme: Bachelor's in Computer Science (Tietojenkäsittelytie­teen kandiohjelma)

This project aims to create a program that is able to generate a procedural dungeon/building interior environment on a 2D top-down grid efficiently based on user defined parameters. The rooms will be randomly distributed and randomly connected by hallways, but being guaranteed to be connected by at least one connecting path. 

In this project I will be using English for both the code and documentation.

## Programming Language

This project will use Python as the primary language. 

I personally know Python and C# relatively well and can peer review projects made in those languages.

## Algorithms and Data Structures

This project will primarily make use of the Bowyer–Watson method for computing Delaunay triangulation. The generated graph will be used for room and hallway generation. 

Another algorithm to be used is Prim's algorithm for creating a minimum spanning tree. This will be used to ensure that the generated environment has a guaranteed path between all points in the graph.

A* will also be used to transpose the connections on the weighted undirected graph on a 2D square grid to model hallways.

In terms of custom data structures I will use the previously mentioned weighted undirected graph for triangulation, a binary heap and adjacency list for Prim's algorithm.

I am using these algorithms and data structures because of their efficiency and flexibility.

## Inputs and Outputs

In the program the user can input the number of rooms, size of rooms and how many additional connections will be added between rooms, in addition to the guaranted main path. A seed for the random generator can also be inputed so that environments with identical seeds and parameters always create the same output.

The output will be a 2D top-down grid environment with rooms and connecting hallways, similar to a 2D top-down video game level. The output will be viewable in the program.

## Target Efficiency

The efficiency of the Bowyer–Watson method using optimizations is O(n log n), where n is the number of points used to triangulate. I will be aiming for the O(n log n) efficiency with n determining the number of rooms that are to be generated. The other algorithms, Prim's algorithm and A* have relatively similar time complexities, ( O(Edges log Vertices) in the case of Prim's ). As the complexity depends on edge and vertex counts, exact efficiency will depend on a case-by-case basis.

## Sources

https://en.wikipedia.org/wiki/Delaunay_triangulation

https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm

https://en.wikipedia.org/wiki/Minimum_spanning_tree

https://en.wikipedia.org/wiki/Prim%27s_algorithm

https://en.wikipedia.org/wiki/Binary_heap

https://en.wikipedia.org/wiki/Adjacency_list

https://en.wikipedia.org/wiki/A*_search_algorithm
