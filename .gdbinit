set pagination off
set logging on
file tests/qt.out
source src/gdb.py
locktree
start
locktree monitore qmutex

