# Assignment HW1

The objective is to implement various search strategies to solve the 8-puzzle, as described in class.

Submit your completed code by checking it into the main branch of your GitHub repo.

The grade will be assigned mostly based on completeness and correctness.

While developing a solution, you may need to print out debugging information. However, the submitted version must produce output in exactly the same format as the code framework provided, without any additional output.

The starter repo for this assignment, available in the course GitHub org, contains an incomplete version of breadth-first search for the 8-puzzle.

---

## Preliminaries

- Ensure you have recent versions of Java and Maven installed. (e.g. `java --version` → `openjdk 21.0.7 2025-04-15 LTS`, `mvn --version` → `Apache Maven 3.9.9`.)

- Ensure you can build using `mvn clean compile` and test using `mvn test` (although some tests will fail until you complete initial parts of the assignment).

- Familiarize yourself with the framework by reading the code and the comments. 

- Ensure that you can run the `main()` method in `EightsPuzzleMain` from the command line, using:
```
java -classpath target/classes edu.dickinson.EightsPuzzleMain bfs tree -1 -1
```
We'll refer to this command as *C1* below.

The code will not yet produce the correct output; it should currently produce:

```
No solution found.
Expanded nodes: 0.
Generated nodes: 1
```

**Don't edit existing code:** This guideline applies to the whole assignment. Unless explicitly stated otherwise, do not edit existing code. The assignment should be completed by inserting new lines of code into the existing files and by adding new files. 

---

## AI Use

You are permitted unlimited AI use if desired. However, it is recommended that you do *not* use AI for this assignment, except when you have no other way to make progress. You will learn and understand the concepts of classical search algorithms by completing these questions manually as much as possible. Therefore it is recommended to turn off completions in your development environment.

---

## Question 1 (35%)

Improve the existing algorithm in the following five ways:

1. **Fill in the missing code** in the following two methods from the `EightsPuzzleWorldState` class: `getValidActions()`, and `apply()`.
   - Hint: there are `TODO` markers in locations where code needs to be added.
   - The command _C1_ above should now find a solution, but the program ignores some of the command line arguments and does not compute the number of expanded and generated nodes. Specifically, the output should be:
     ```
     Solution found.
     Expanded nodes: 0
     Generated nodes: 1
     ```

2. **Add expanded/generated node counts.** At present, the algorithm does not compute the number of expanded and generated nodes correctly. Add this functionality.
   - No `TODO` markers are provided. You will need to add some code to `ClassicalSearch.java`.
   - The output should now be as follows (some minor variation in the number of expanded and generated nodes is permissible, since this depends on your precise definitions):
     ```
     Solution found.
     Expanded nodes: 43
     Generated nodes: 121
     ```

3. **Pass the provided JUnit tests.** The provided repository includes two JUnit tests. If you run the tests (e.g. via `mvn test`), those tests should now pass.

4. **Enforce `maxNodes`.** At present, the algorithm ignores the value of `maxNodes` in the `ClassicalSearch` class. Ensure that the algorithm terminates with failure if it attempts to expand more than `maxNodes`. The special value `maxNodes == -1` indicates no maximum on the number of nodes expanded. *(From this point on in the assignment, you will need to carefully test the behavior of your algorithm to ensure that it is correct. The expected outputs will not be provided. Creating suitable JUnit tests would be one effective way of testing your code.)*

5. **Enforce `maxDepth`.** At present, the algorithm ignores the value of `maxDepth` in the `ClassicalSearch` class. Ensure that the algorithm terminates with failure if it has explored all nodes at depths up to and including `maxDepth` without finding a solution. The special value `maxDepth == -1` indicates no maximum on the depth.

6. **Implement graph search.** At present, tree search is implemented but graph search is not. Ensure that when the `graph` option is specified on the command line, the algorithm never expands the same state more than once.

---

## Question 2 (20%)

Implement depth-first search, by creating and implementing a `DepthFirstSearchNode` class that extends `SearchNode`. Also make the necessary changes to `EightsPuzzleMain` so that the `dfs` option now works from the command line.

---

## Question 3 (10%)

Implement A\* search with the number-of-misplaced-tiles heuristic described as $h_1$ in our class lectures. This can be accomplished by creating and implementing an `AStarNumTiles` class that extends `SearchNode`. Also make the necessary changes to `EightsPuzzleMain` so that the `as1` option now works from the command line.

---

## Question 4 (15%)

Implement A\* search with the Manhattan distance heuristic described as $h_2$ in our class lectures. This can be accomplished by creating and implementing an `AStarManhattan` class that extends `SearchNode`. Also make the necessary changes to `EightsPuzzleMain` so that the `as2` option now works from the command line.

---

## Question 5 (10%)

Your `AStarNumTiles` and `AStarManhattan` classes contain some shared functionality. Refactor your code to eliminate the shared functionality. Hint: one way to do this involves creating a new abstract class.

---

## Question 6 (10%)

Make any changes necessary so that the code works on different sizes of puzzle. For example, by redefining `START_BOARD` as `{ { 0, 1, 2, 3 }, { 4, 5, 6, 7 }, { 8, 9, 10, 11 }, { 12, 13, 14, 15 } }`, and declaring a suitable goal board, the code should now be able to solve 15-puzzles. It should also work for arbitrary rectangular puzzles (e.g. a 3×4 board).

Note: if your code was written using good software development technique, no other changes should be required — or at most, changes to one or two constants. If you find that further changes are required, make note of how you could avoid such problems in future projects, by avoiding the use of hard-wired assumptions in your code.

---

## Suggested Further Work

*(No extra credit is available. Completing this further work will, however, be extremely beneficial for understanding the algorithms and increasing your maturity as a computer scientist.)*

- Examine the number of nodes explored and generated for each of the algorithms implemented. Do the numbers make sense?

- The goal state provided in the code framework is a very easy goal. Rerun your algorithms on a moderately difficult goal (e.g. `{% raw %}{{0,3,1},{7,6,2},{4,8,5}}{% endraw %}`) and a difficult goal (e.g. `{% raw %}{{7,2,4},{5,0,6},{8,3,1}}{% endraw %}`). Again, do the results make sense?


- Implement iterative deepening search.

---

**Acknowledgment:** Several of the above questions are based on a lab created by Prof. Grant Braught in 2008, and I'm grateful for his permission to incorporate this material.
