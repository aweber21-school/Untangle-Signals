import argparse
import trace
from itertools import batched

# Global counter for the number of states sifted through to remove duplicates
duplicatesSifted = 0

# Global counter for the number of states created
statesCreated = 0

# Global counter for the number of symbols processed
symbolsProcessed = 0


class State:
    """
    The State class contains the progress in matching the input signal to each
    of the reference signals
    """

    def __init__(
        self,
        i: int = 0,
        j: int = 0,
        labels: str = "",
        cx: int = 0,
        cy: int = 0,
        start: int = -1,
        end: int = -1,
        best: int = -1,
    ) -> None:
        """Initializes a new State"""
        self.i = i
        self.j = j
        self.labels = labels
        self.cx = cx
        self.cy = cy
        self.start = start
        self.end = end
        self.best = best


def removeDuplicates(states: list[State]) -> list[State]:
    """Removes duplicate States within a list of States"""
    global duplicatesSifted

    seen = set()
    results = []

    # Loop through all States
    for state in states:
        # Create a tuple with all of the items that make a State unique to use
        # as a key
        key = (state.i, state.j, state.cx, state.cy)

        # Mark the key as seen and append the State to the results list
        if key not in seen:
            seen.add(key)
            results.append(state)

        duplicatesSifted += 1

    return results


def untangleSignals(
    s: str, x: str, y: str
) -> tuple[list[list[int]], list[list[int]], list[int]]:
    """Performs the Untangle Signals algorithm"""
    global statesCreated
    global symbolsProcessed

    # List containing currently active States
    active: list[State] = []

    # Loop through all symbols in the input signal
    for position in range(len(s)):
        symbol = s[position]
        new: list[State] = []

        # New States
        # Beginning of X signal
        if symbol == x[0]:
            new.append(
                State(
                    i=(1 % len(x)),
                    j=(0),
                    labels=("x"),
                    cx=(1 // len(x)),
                    cy=(0),
                    start=(position),
                    end=(-1),
                    best=(-1),
                )
            )
            statesCreated += 1

        # Beginning of Y signal
        if symbol == y[0]:
            new.append(
                State(
                    i=(0),
                    j=(1 % len(y)),
                    labels=("y"),
                    cx=(0),
                    cy=(1 // len(y)),
                    start=(position),
                    end=(-1),
                    best=(-1),
                )
            )
            statesCreated += 1

        # Existing States
        for state in active:
            # End hasn't been found yet, keep evaluating against X and Y
            if state.end == -1:
                # Symbol is next for X
                if symbol == x[state.i]:
                    newi = (state.i + 1) % len(x)
                    newcx = state.cx + ((state.i + 1) // len(x))
                    newbest = state.best
                    if newi == 0 and state.j == 0 and newcx > state.cx:
                        newbest = position

                    new.append(
                        State(
                            i=(newi),
                            j=(state.j),
                            labels=(state.labels + "x"),
                            cx=(newcx),
                            cy=(state.cy),
                            start=(state.start),
                            end=(-1),
                            best=(newbest),
                        )
                    )
                    statesCreated += 1

                # Symbol is next for Y
                if symbol == y[state.j]:
                    newj = (state.j + 1) % len(y)
                    newcy = state.cy + ((state.j + 1) // len(y))
                    newbest = state.best
                    if state.i == 0 and newj == 0 and newcy > state.cy:
                        newbest = position

                    new.append(
                        State(
                            i=(state.i),
                            j=(newj),
                            labels=(state.labels + "y"),
                            cx=(state.cx),
                            cy=(newcy),
                            start=(state.start),
                            end=(-1),
                            best=(newbest),
                        )
                    )
                    statesCreated += 1

                # Symbol is not next for either X or Y, state ends
                if symbol != x[state.i] and symbol != y[state.j]:
                    new.append(
                        State(
                            i=(state.i),
                            j=(state.j),
                            labels=(state.labels),
                            cx=(state.cx),
                            cy=(state.cy),
                            start=(state.start),
                            end=(position),
                            best=(state.best),
                        )
                    )
                    statesCreated += 1

        symbolsProcessed += 1

        # Remove duplicate states after each symbol is processed
        active = removeDuplicates(new)

    results = ""
    best = 0
    for state in active:
        if state.cx > 0 and state.cy > 0 and (state.best - state.start) > best:
            best = state.best - state.start
            results = (("n" * state.start) + state.labels)[: state.best + 1].ljust(
                len(s), "n"
            )

    # Reorganize algorithm results
    xSymbols = []
    for position in range(len(results)):
        if results[position] == "x":
            xSymbols.append(position)
    xSymbols = [list(xSignal) for xSignal in batched(xSymbols, len(x))]

    ySymbols = []
    for position in range(len(results)):
        if results[position] == "y":
            ySymbols.append(position)
    ySymbols = [list(ySignal) for ySignal in batched(ySymbols, len(x))]

    nSymbols = []
    for position in range(len(results)):
        if results[position] == "n":
            nSymbols.append(position)

    # Return
    return xSymbols, ySymbols, nSymbols


def getArguments() -> argparse.Namespace:
    """Get the program's arguments"""
    # Program information
    parser = argparse.ArgumentParser(
        prog="Untangle-Signals",
        description="Executes the Untangle Signals algorithm",
    )

    # Run a trace
    parser.add_argument(
        "-t",
        "--trace",
        action="store_true",
        help="Runs a trace on the algorithm",
    )

    # Specify specific input file if desired
    parser.add_argument(
        "-i",
        "--input",
        action="store",
        default="input.txt",
        help="Specify input file name; can be used for specific inputs when the "
        "'P' flag is omitted, otherwise will save input file to given location",
    )

    # The s signal to use in the Untangle Signals algorithm
    parser.add_argument(
        "-s",
        "--s",
        action="store",
        default="",
        help="The s signal to use in the Untangle Signals algorithm",
    )

    # The x signal to use in the Untangle Signals algorithm
    parser.add_argument(
        "-x",
        "--x",
        action="store",
        default="",
        help="The x signal to use in the Untangle Signals algorithm",
    )

    # The y signal to use in the Untangle Signals algorithm
    parser.add_argument(
        "-y",
        "--y",
        action="store",
        default="",
        help="The y signal to use in the Untangle Signals algorithm",
    )

    # Output file
    parser.add_argument(
        "-o",
        "--output",
        action="store",
        default="output.txt",
        help="Specify output file name",
    )

    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    s: str = ""
    x: str = ""
    y: str = ""

    # Save provided inputs if all are given
    if args.s and args.x and args.y:
        with open(args.input, "w") as f:
            print((args.s, args.x, args.y), file=f)

    # Input
    try:
        with open(args.input, "r") as f:
            for line in f.readlines():
                s, x, y = eval(line)
    except FileNotFoundError:
        print(f"Could not find {args.input}")
        exit()

    # Run the Untangle Signals algorithm
    xSymbols, ySymbols, nSymbols = untangleSignals(s, x, y)

    # Print algorithm results
    print(f"Number of States Sifted for Duplicates: {duplicatesSifted}")
    print(f"Number of States Created: {statesCreated}")
    print(f"Number of Symbols Processed: {symbolsProcessed}")

    # Save the output
    with open(args.output, "w") as f:
        print("X: " + str(xSymbols), file=f)
        print("Y: " + str(ySymbols), file=f)
        print("N: " + str(nSymbols), file=f)


if __name__ == "__main__":
    # Get the program's arguments
    args = getArguments()

    # Run a trace
    if args.trace:
        # Create Trace object
        tracer = trace.Trace(
            ignoredirs=[],
            trace=0,
            count=1,
        )

        # Run trace
        tracer.run("main(args)")

        # Make a report
        r = tracer.results()
        r.write_results(show_missing=True, coverdir="traceOutput")

    # Run normally
    else:
        main(args)
