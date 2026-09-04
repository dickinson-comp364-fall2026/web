# Detailed schedule and resources

## Class 2

* arrangements for next week's field trip on Tuesday 9/8:
  - Meet in Kaufman parking lot near the entrance to [Public Safety](https://maps.app.goo.gl/ybuyWRGDrGsb8rVm8) no later than 1:30 PM.
  - optional: Wear shoes that can get muddy if you want to stroll on the Appalachian Trail for a few minutes.
  - our route: [Kaufman parking lot to PAX1 site then Appalachian Trail](https://goo.gl/maps/P9VtDsQK7fzCum3n6)
  - We will be back on campus before the end of class at 2:45 PM.
* any questions on the syllabus?
  - Discussion of AI use policy
* review _search node_ with fields state, parent, action, depth, cost
  - show Java file `SearchNode.java` from HW1
* Show BFS via quiz1 qu1, skip DFS
* Show UCS via quiz1 qu3
* Show A* via quiz1 qu4
* define admissible heuristic, consistent heuristic:
  - admissible: never overestimates the cost to reach the goal, so \\(h(n) \leq h^*(n)\\)
  - consistent: the estimated cost of reaching the goal from a node is less than or equal to the cost of reaching a neighbor plus the estimated cost of reaching the goal from the neighbor, so \\(h(n) \leq c(n, n') + h(n')\\)
* define 8-puzzle heuristics:
  - h1: number-of-misplaced-tiles
    - h1(state) = number of tiles in the wrong position
  - h2: manhattan-distance
    - h2(state) = sum of horizontal and vertical distances of the tiles from their goal positions
* if time, review Matrix Algebra section 1


## Class 1

* Submit info on the [Github username form](https://forms.cloud.microsoft/r/9qf9hUYZfs)
* Transportation arrangements for next week's field trip
* sidetrack: check out [stoppax1.com](https://stoppax1.com/)
  - [real-time action relevant to our course](./class01/board-meeting.png)
* Syllabus: Read carefully for homework and bring questions next time
* Make sure to check out the 8-puzzle game. 
* "marshalls and crocodiles" -- group activity
* _search node_ -- essential concept -- see `SearchNode.java` from HW1
* BFS (quiz1 question 1) -- _skipped_
* DFS (quiz1 question 2) -- _skipped_
* Matrix Algebra section 1 -- see [Readings page](../readings/)

