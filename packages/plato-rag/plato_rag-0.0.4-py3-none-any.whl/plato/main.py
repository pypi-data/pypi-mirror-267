import argparse 
import os

from .api import Plato


def upload(args):
    client = Plato(os.environ["PLATO_API_KEY"],
                   os.environ["PLATO_ORG_ID"])
    if args.dir:
        print(f"Uploading directory {args.dir}")
        client.upload(dir=args.dir)
    elif args.file:
        print(f"Upload file {args.file}")
        client.upload(file=args.file)
    elif args.link:
        print(f"Uploading website link {args.link}")
        client.upload(link=args.link)


def ask(args):
    client = Plato(os.environ["PLATO_API_KEY"],
                   os.environ["PLATO_ORG_ID"])
    print(client.complete(args.question))


def main():
    parser = argparse.ArgumentParser(description="Plato CLI tool")
    subparsers = parser.add_subparsers()

    parser_upload = subparsers.add_parser('upload', help='Upload files, directories/folders, or links')
    group = parser_upload.add_mutually_exclusive_group(required=True)
    group.add_argument('--dir', type=str, help='Directory to upload')
    group.add_argument('--file', type=str, help='File to upload')
    group.add_argument('--link', type=str, help='Link to upload content from')
    parser_upload.set_defaults(func=upload)

    parser_ask = subparsers.add_parser('ask', help='Ask a question')
    parser_ask.add_argument('--question', type=str, required=True, help='Question to ask')
    parser_ask.set_defaults(func=ask)
    
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()