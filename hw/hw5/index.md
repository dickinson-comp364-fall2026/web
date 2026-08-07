# Assignment HW5: Transformers

**under construction**: This assignment is still being developed. Please check back later for the full instructions.

In this assignment, you will complete the implementation of a transformer model. All the resources you need are provided in the starter repo for this assignment, which is available in the course GitHub org. 
<!-- The README file in the starter repo contains a description of the task and the data. -->

To complete the assignment, add and/or alter code at the locations of the string "TODO" in the source file `train_transformer.py`.

To turn in this assignment, push changes to your private assignment repo in the course GitHub org. Grading will be based largely on completeness and correctness.

## Optional extension exercises

1. Play around with the structure of network by altering the configuration file in the `configs` directory (e.g., adjust num layers, num features, stride length, kernel width). Which settings produce better results and/or faster training? 
2. Run training on a larger dataset. To do this, edit the config file. Replace the two occurrences of `_300.csv` with `_1000.csv`, `_2000.csv`, ... , or `_5000.csv`. Do the results improve with more training data? How does the training time change?
3. The whole point of this assignment was to learn how to implement a 1D convolutional network. But does it actually work better than a simpler alternative for this application? Create an MLP that solves the same task and compare its performance in terms of training time and accuracy.
4. The idea of projecting latitude from temperature patterns seems cool, but it's hard to appreciate that our network is actually doing this based only on a report of mean squared error. Create a visualization that shows the successes and failures of the trained network, perhaps by overlaying on a map of the US.

---

## AI Use

The AI policy for this assignment is very similar to the previous ones:
> You are permitted unlimited AI use if desired. However, it is recommended that you do *not* use AI for this assignment, except when you have no other way to make progress. You will learn and understand the concepts of convolutional neural networks by completing these questions manually as much as possible. Therefore it is recommended to turn off completions in your development environment.

