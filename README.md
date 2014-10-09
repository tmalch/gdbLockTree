gdbLockTree: LockTree Algo for GDB 
===========
proof of concept - not for use

copy LockTreeCommand.py and folder gdbLockTree into /usr/share/gdb/python/gdb/command to add the command "locktree" to gdb

OR

exec 'source path/to/LockTreeCommand.py' from within gdb

implemented commands   
locktree plugins: prints all available plugins for different locks (eg pthread_mutex, SWEB Mutex)  
locktree monitore <plugin>: creates Breakpoints for the given plugin  
locktree stop: deletes all Breakpoints created by the locktree command  
locktree useless: shows all locks that are only used by one thread  
locktree check: executes locktree algorithm to detect possible deadlocks and reports result  
locktree printthreads: prints the recorded threads  
locktree printgui <thread>: opens a window with a graph view of the locktree of the given thread (needs graphviz)  
locktree printtree <thread>: prints the locktree of the given thread as ascii art  
locktree holdlocks <thread>: prints the locks currently hold by the given thread  
locktree lockinfo <lock>: prints information about the given lock. Where is it defined which threads use it and from where in the code is it called   
