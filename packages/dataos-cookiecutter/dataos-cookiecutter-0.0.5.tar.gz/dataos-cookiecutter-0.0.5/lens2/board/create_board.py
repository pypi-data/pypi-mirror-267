from lens2.board import generate_board, start_board


def add_subparser(subparsers):
    rill_parser = subparsers.add_parser("board", help="Create lens2 view board")
    rill_parser.add_argument("action", choices=["create", "start"], help="Create or start lens2 board to explore view.")

    rill_parser.add_argument("-n", "--name", required=True,
                             help="Name of the view/s (comma separated) to perform "
                                  "create or start board")


def execute_board(args):
    views = [name.strip() for name in args.name.split(',')]
    if args.action == "create":
        generate_board.execute_create(views)
    elif args.action == "start":
        start_board.executes_start(views)
