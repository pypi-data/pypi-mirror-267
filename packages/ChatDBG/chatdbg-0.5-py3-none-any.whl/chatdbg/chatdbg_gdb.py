import json
import os
import pathlib
import sys

import gdb

import llm_utils

sys.path.append(os.path.abspath(pathlib.Path(__file__).parent.resolve()))
import old_stuff.chatdbg_utils as chatdbg_utils

# The file produced by the panic handler if the Rust program is using the chatdbg crate.
rust_panic_log_filename = "panic_log.txt"


# Set the prompt to gdb-ChatDBG
gdb.prompt_hook = lambda current_prompt: "(gdb-ChatDBG) "

last_error_type = ""


def stop_handler(event):
    """Sets last error type so we can report it later."""
    # Check if the event is a stop event
    global last_error_type
    if not hasattr(event, "stop_signal"):
        last_error_type = ""  # Not a real error (e.g., a breakpoint)
        return
    if event.stop_signal is not None:
        last_error_type = event.stop_signal


gdb.events.stop.connect(stop_handler)


# Implement the command `why`
class Why(gdb.Command):
    """Provides root cause analysis for a failure."""

    def __init__(self):
        gdb.Command.__init__(self, "why", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        try:
            frame = gdb.selected_frame()
        except:
            print("Must run the code first to ask `why`.")
            return
        global last_error_type
        if not last_error_type:
            # Assume we are running from a core dump,
            # which _probably_ means a SEGV.
            last_error_type = "SIGSEGV"
        the_prompt = buildPrompt()
        args, _ = chatdbg_utils.parse_known_args(arg.split())
        if the_prompt:
            # Call `explain` function with pieces of the_prompt  as arguments.
            chatdbg_utils.explain(the_prompt[0], the_prompt[1], the_prompt[2], args)


Why()


def buildPrompt() -> tuple[str, str, str]:
    thread = gdb.selected_thread()
    if not thread:
        return ""

    stack_trace = ""
    source_code = ""

    frames = []
    frame = gdb.selected_frame()

    # magic number - don't bother walking up more than this many frames.
    # This is just to prevent overwhelming OpenAI (or to cope with a stack overflow!).
    max_frames = 10

    # Walk the stack and build up the frames list.
    while frame is not None and max_frames > 0:
        func_name = frame.name()
        symtab_and_line = frame.find_sal()
        if symtab_and_line.symtab is not None:
            filename = symtab_and_line.symtab.filename
        else:
            filename = None
        if symtab_and_line.line is not None:
            lineno = symtab_and_line.line
            colno = None
        else:
            lineno = None
            colno = None
        args = []
        try:
            block = frame.block()
        except RuntimeError:
            print(
                "Your program must be compiled with debug information (`-g`) to use `why`."
            )
            return ""
        for symbol in block:
            if symbol.is_argument:
                name = symbol.name
                value = frame.read_var(name)
                args.append((name, value))
        frames.append((filename, func_name, args, lineno, colno))
        frame = frame.older()
        max_frames -= 1

    # Now build the stack trace and source code strings.
    for i, frame_info in enumerate(frames):
        file_name = frame_info[0]
        func_name = frame_info[1]
        line_num = frame_info[3]
        arg_list = []
        for arg in frame_info[2]:
            arg_list.append(str(arg[1]))  # Note: arg[0] is the name of the argument
        stack_trace += (
            f'frame {i}: {func_name}({",".join(arg_list)}) at {file_name}:{line_num}\n'
        )
        try:
            source_code += f"/* frame {i} */\n"
            (lines, first) = llm_utils.read_lines(filename, line_num - 10, line_num)
            block = llm_utils.number_group_of_lines(lines, first)
            source_code += f"{block}\n\n"
        except:
            # Couldn't find source for some reason. Skip file.
            pass

    # If the Rust panic log exists, append it to the error reason.
    global last_error_type
    try:
        with open(rust_panic_log_filename, "r") as log:
            panic_log = log.read()
        last_error_type = panic_log + "\n" + last_error_type
    except:
        pass

    return (source_code, stack_trace, last_error_type)
