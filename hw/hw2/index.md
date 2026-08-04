# Programming assignment 2: Decision trees

In this assignment, you will complete the implementation a decision tree. All the resources you need are provided in the starter repo for this assignment, which is available in the course GitHub org.

The resources comprise three directories: the Java source files for a code framework (`src`), the Javadoc for the code framework (`javadoc`), and some data for your experiments (`data`). You should first read all the Javadoc, concentrating especially on `AttributeSet`, `InstanceSet`, and `Distribution`. (Click on `index.html` to start reading.) Don't bother reading all of the source files; consult these as needed, if and when the Javadoc proves to be insufficient.

Glance at the data files (each has the extension `.arff`) using a text editor. A constructor for `InstanceSet` automatically reads a `.arff` file, so you need not interact with these files directly, but it will help to have some familiarity with these files when debugging your code. The file format is fairly obvious and is not described further here.

The three data files provided are `weather.nominal.arff`, `contact-lenses.arff`, and `soybeanB.arff`. The first file is a fake data set for deciding whether or not to play tennis based on the current weather conditions, authored by Ian Witten and Eibe Frank, and provided with their Weka machine learning software. This is a small, almost trivial machine learning problem. It's not very interesting, but an extremely useful file for debugging. The second file is a real data set for determining what type of contact lenses to prescribe to a patient based on their condition. The third file is a real data set for determining what type of disease a soybean has (although the file has been edited to remove so-called _missing data_, which we don't deal with in this assignment). Both the second and third files are part of a well-known collection of machine learning data collated and distributed by the University of California, Irvine, and known as the UC Irvine Machine Learning Repository.

To complete the assignment, add and/or alter code at the nine locations of the string "TODO" in the three source files `DecisionTree.java`, `DecisionTreeInternal.java`, and `DecisionTreeLeaf.java`. When finished, your code should successfully and correctly generate decision trees for all three provided data files. This is accomplished in the `main` method of DecisionTree, which accepts a single commandline argument: the name of the `.arff` file to be used. Do not edit or add code at any location other than the "TODO" markers. (Exception: you may create your own private methods if desired.)

JUnit tests are provided to help you verify that your code is working correctly.

To turn in this assignment, push changes to your private assignment repo in course GitHub org. Grading will be based largely on completeness and correctness.

---

## AI Use

The AI policy for this assignment is very similar to the previous one:
> You are permitted unlimited AI use if desired. However, it is recommended that you do *not* use AI for this assignment, except when you have no other way to make progress. You will learn and understand the concepts of decision tree algorithms by completing these questions manually as much as possible. Therefore it is recommended to turn off completions in your development environment.

