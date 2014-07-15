set pagination off
set logging on
file tests/a.out
source src/gdb.py
locktree
b pthread_mutex_lock
start
c

