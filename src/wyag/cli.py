import argparse
import sys

def main(argv=sys.argv[1:]):
    """Main CLI entry point."""
    args = argparser.parse_args(argv)
    match args.command:
        case 'add': cmd_add(args)
        case 'cat-file': cmd_cat_file(args)
        case 'check-ignore': cmd_check_ignore(args)
        case 'commit': cmd_commit(args)
        case 'hash-object': cmd_hash_object(args)
        case 'init': cmd_init(args)
        case 'log': cmd_log(args)
        case 'ls-files': cmd_ls_files(args)
        case 'ls-tree': cmd_ls_tree(args)
        case 'rev-parse': cmd_rev_parse(args)
        case 'rm': cmd_rm(args)
        case 'show-ref': cmd_show_ref(args)
        case 'status': cmd_status(args)
        case 'merge': cmd_merge(args)
        case 'read-tree': cmd_read_tree(args)
        case 'reset': cmd_reset(args)
        case 'tag': cmd_tag(args)
        case _: 
            print("Bad command")
            return 1
    return 0

def cmd_init(args):
    """Handle init command."""
    from wyag.commands.init import cmd_init as init_command
    return init_command(args)

# Placeholder functions for other commands
def cmd_add(args):
    raise NotImplementedError("add command not implemented")

def cmd_cat_file(args):
    raise NotImplementedError("cat-file command not implemented")

def cmd_check_ignore(args):
    raise NotImplementedError("check-ignore command not implemented")

def cmd_commit(args):
    raise NotImplementedError("commit command not implemented")

def cmd_hash_object(args):
    raise NotImplementedError("hash-object command not implemented")

def cmd_log(args):
    raise NotImplementedError("log command not implemented")

def cmd_ls_files(args):
    raise NotImplementedError("ls-files command not implemented")

def cmd_ls_tree(args):
    raise NotImplementedError("ls-tree command not implemented")

def cmd_rev_parse(args):
    raise NotImplementedError("rev-parse command not implemented")

def cmd_rm(args):
    raise NotImplementedError("rm command not implemented")

def cmd_show_ref(args):
    raise NotImplementedError("show-ref command not implemented")

def cmd_status(args):
    raise NotImplementedError("status command not implemented")

def cmd_merge(args):
    raise NotImplementedError("merge command not implemented")

def cmd_read_tree(args):
    raise NotImplementedError("read-tree command not implemented")

def cmd_reset(args):
    raise NotImplementedError("reset command not implemented")

def cmd_tag(args):
    raise NotImplementedError("tag command not implemented")

argparser = argparse.ArgumentParser(description="The Wyag command line interface.")
argSupParsers = argparser.add_subparsers(title="Commands", dest="command")
argSupParsers.required = True

argsp = argSupParsers.add_parser("init", help="Initialize a new, empty repository")
argsp.add_argument("path", metavar="directory", nargs="?", default=".", 
                   help="The path to the new repository. Defaults to the current one")


if __name__ == "__main__":
    sys.exit(main())