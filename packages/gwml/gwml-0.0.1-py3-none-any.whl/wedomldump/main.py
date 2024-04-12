from wedomldump.mldump import MLdump
from wedomldump.command import CommandParser


def main():
    args = CommandParser().get_args()
    mldump = MLdump()

    if args.command == "push":
        mldump.initPush(args)
