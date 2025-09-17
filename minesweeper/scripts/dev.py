from src.ui.tui.tui_input_parser import create_input_parser


def main() -> None:
    p = create_input_parser(True)

    try:
        ns = p.parse_args(input().split())
        print(ns)
    except SystemExit:
        print('Attempted exit (most likely by argparse)')
    except KeyboardInterrupt:
        print('Attempted keyboard interrupt')

    input('THE END! Press Enter to continue...')


if __name__ == '__main__':
    main()
