# Untangle-Signals
This repository contains the Untangle Signals algorithm for EN.605.621 Programming Assignment 3

## Implementation
The Untangle Signals algorithm is implemented in Python. This algorithm can be
ran the same way as any other Python script, along with flags to control
functionality. An example command line command is shown below:

```
python Untangle-Signals.py -t -s 100010101 -x 101 -y 0 -i inputFile.txt -o outputFile.txt
```

## Files
This repository contains this README, the source code for the Untangle Signals
algorithm, traces, and test cases. The file structure is shown below:

```
Untangle-Signals
|---> README.md
|---> Untangle-Signals.py
|---> traces/
|     |---> trace-s#/
|     |     |---> input-s#.txt
|     |     |---> output-s#.txt
|     |     |---> results-s#.txt
|     |     |---> traceOutput-s#/
|     |           |---> Untangle-Signals.cover
|     |---> ...
|---> testCases/
      |---> s#/
      |     |---> input-s#.txt
      |     |---> output-s#.txt
      |     |---> results-s#.txt
      |     |---> traceOutput-s#/
      |           |---> Untangle-Signals.cover
      |---> ...
```
