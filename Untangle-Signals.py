import argparse
import trace


class State:
    """
    The State class contains the progress in matching the input signal to each
    of the reference signals
    """

    def __init__(
        self,
        i: int = 0,
        j: int = 0,
        labels: list[str] = [],
        cx: bool = False,
        cy: bool = False,
    ) -> None:
        """Initializes a new State"""
        self.i = i
        self.j = j
        self.labels = labels
        self.cx = cx
        self.cy = cy


def removeDuplicates(states: list[State]) -> int:
    """Removes duplicate States within a list of States"""
    return 0


def untangleSignals(s: str, x: str, y: str) -> list[str]:
    """Performs the Untangle Signals algorithm"""
    # List containing currently active States
    active: list[State] = []

    results = []
    # for state in active:
    #     if state.cx and state.cy:
    #         results = state.labels
    print(s, x, y)

    # Print algorithm results

    # Return
    return results


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
    results = untangleSignals(s, x, y)

    # Save the output
    with open(args.output, "w") as f:
        print(results, file=f)


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
