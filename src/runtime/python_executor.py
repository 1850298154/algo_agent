import multiprocessing
import re
import sys
from io import StringIO
from typing import Any, Dict, Optional

def sanitize_input(query: str) -> str:
    """Sanitize input to the python REPL.

    Remove whitespace, backtick & python
    (if llm mistakes python console as terminal)

    Args:
        query: The query to sanitize

    Returns:
        str: The sanitized query
    """
    query = re.sub(r"^(\s|`)*(?i:python)?\s*", "", query)
    query = re.sub(r"(\s|`)*$", "", query)
    return query

def worker(
    command: str,
    globals: Optional[Dict],
    locals: Optional[Dict],
    queue: multiprocessing.Queue,
) -> None:
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    try:
        cleaned_command = sanitize_input(command)
        exec(cleaned_command, globals, locals)
        sys.stdout = old_stdout
        queue.put(mystdout.getvalue())
    except Exception as e:
        sys.stdout = old_stdout
        queue.put(repr(e))

def run(
        command: str, 
        globals: dict[str, Any] | None = None, 
        locals: Optional[Dict] = None, 
        timeout: Optional[int] = None
    ) -> str:

    """Run command with own globals/locals and returns anything printed.
    Timeout after the specified number of seconds."""

    queue: multiprocessing.Queue = multiprocessing.Queue()

    # Only use multiprocessing if we are enforcing a timeout
    if timeout is not None:
        # create a Process
        p = multiprocessing.Process(
            target=worker, args=(command, globals, locals, queue)
        )

        # start it
        p.start()

        # wait for the process to finish or kill it after timeout seconds
        p.join(timeout)

        if p.is_alive():
            p.terminate()
            return "Execution timed out"
    else:
        worker(command, globals, locals, queue)
    # get the result from the worker function
    return queue.get()
