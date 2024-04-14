# Some ctypes stuff for processes

## pip install randomandroidphone

### Tested against Windows 10 / Python 3.11 / Anaconda

```py

    from ctypesprocstuff import (
        get_kids_dict,
        get_all_procs_with_children,
        iter_process,
        wmic_process_active,
        is_process_user_an_admin,
        kill_process_and_children,
        suspend_subprocess,
        resume_subprocess,
    )
    import subprocess
    import time

    qq = get_kids_dict(pid=23336, bi_rl_lr="lr")
    print(qq)

    allprocschild = get_all_procs_with_children()
    for i in iter_process():
        di = wmic_process_active(i.th32ProcessID)
        try:
            print(is_process_user_an_admin(i.th32ProcessID))
        except Exception as e:
            print(e)
        if di.get("Caption", "") == "uc_driver.exe":
            print(i.th32ProcessID)
            kill_process_and_children(i.th32ProcessID, taskkillargs=("/f",))
        print(di)


    p = subprocess.Popen("notepad.exe")
    time.sleep(5)
    suspend_subprocess(p)
    time.sleep(15)
    resume_subprocess(p)

    # kill_process_and_children(pid=15300, taskkillargs=("/f",))


    get_all_procs_with_children() -> 'list[dict]'
        A function to get all processes with their children.
        Returns a list of dictionaries containing information about processes and their children (except pid 0 and pid 4).

    get_kids_dict(pid: 'int', bi_rl_lr: "Literal['rl', 'lr', 'bi']" = 'lr') -> 'dict'
        A function that constructs a dictionary of processes and their children based on the provided process ID.

        Args:
            pid (int): The process ID for which to build the dictionary.
            bi_rl_lr (Literal["rl", "lr", "bi"], optional): The direction of the process hierarchy. Defaults to "lr" (left to right).

        Returns:
            dict: A dictionary mapping the processes and their children along with module information.

    is_process_user_an_admin(pid: 'int') -> 'bool'
        Checks if the process user identified by the given process ID is an administrator.

        Args:
            pid (int): The process ID to check for administrator privileges.

        Returns:
            bool: True if the process user is an administrator, False otherwise.

    iter_module(pid: 'int') -> 'Generator'
        A function that iterates over the modules of a specified process.

        Args:
            pid (int): The process ID for which to iterate over the modules.

        Yields:
            Generator: Yields the module information obtained from the snapshot.

    iter_process() -> 'Generator'
        A function that iterates over the processes from a snapshot and yields them.

    iter_threads() -> 'Generator'
        A function that iterates over the threads from a snapshot and yields them.

    kill_process_and_children(pid: 'int', taskkillargs: 'tuple' = ('/f',)) -> 'list[list[bytes, bytes, int]]'
        A function to kill a process and its children based on the given process ID (starting from the deepest child).
        Args:
            pid (int): The process ID of the parent process to be killed.
            taskkillargs (tuple, optional): Additional arguments for the taskkill command. Defaults to ("/f",).

        Returns:
            list[list[bytes, bytes, int]]: A list containing information about the executed kill process and its children after termination.

    resume_subprocess(proc: 'subprocess.Popen') -> 'None'
        Resumes a subprocess based on the given process handle.

        Args:
            proc (subprocess.Popen): The subprocess to be resumed.

        Returns:
            None

    suspend_subprocess(proc: 'subprocess.Popen') -> 'None'
        Suspend a subprocess by calling NtSuspendProcess with the handle of the provided subprocess.

        Parameters:
            proc (subprocess.Popen): The subprocess to be suspended.

        Returns:
            None

    wmic_process_active(pid: 'int') -> 'dict'
        Retrieves information about an active process based on the provided process ID.
        Args:
            pid (int): The process ID for which to retrieve information.

        Returns:
            dict: A dictionary containing information about the active process, including CommandLine, Caption, and ProcessId.
```