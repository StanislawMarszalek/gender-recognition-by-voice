from argparse import ArgumentParser
from time import perf_counter
from warnings import simplefilter
from functions import gender_recognition


def main()->None:

    parser=ArgumentParser(usage="gender_recognition.py [FILE] [OPTION]\n" \
    "Try gender_recognition.py -h or gender_recognition.py --help for more information.")
    parameters=parser.add_argument_group("Algorithm parameters")
    add_info=parser.add_argument_group("Additional information")
    parameters.add_argument("file",
                            type=str,
                            help="Path to the .wav file")
    parameters.add_argument("-fr","--frame_ms",
                            type=int,
                            help="Frames length in milliseconds (deafault value: 150)")
    parameters.add_argument("-hop","--hop_ms",
                            type=int,
                            help="Hop length in milliseconds (deafault value: 30)")
    parameters.add_argument("-it","--iterations",
                            type=int,
                            help="Number of iterations for Harmonic Product Spectrum algorithm (deafault value: 3)")
    add_info.add_argument("-w","--warnings",
                          action="store_true",
                          help="Show warnings")
    add_info.add_argument("-t","--time",
                          action="store_true",
                          help="Show execution time in milliseconds")

    args=parser.parse_args()
    pathfile=args.file
    frame_ms=args.frame_ms if args.frame_ms is not None and args.frame_ms>0 else 150
    hop_ms=args.hop_ms if args.hop_ms is not None and args.hop_ms>0 else 30
    iterations=args.iterations if args.iterations is not None and args.iterations>0 else 3
    simplefilter("default") if args.warnings else simplefilter("ignore")

    start=perf_counter()
    result=gender_recognition(pathfile,frame_ms,hop_ms,iterations)
    stop=perf_counter()
    if result in ['M','W']:
        print(f"Result: {result}")
        if args.time:
            print(f"Time: {(stop-start)*1000}")
    else:
        print(f"ERROR:{result}")


if __name__=="__main__":
    main()
