#!/usr/bin/python3

import os
import socket
import psutil
import curses
import platform

def resize_terminal():
    current_os = platform.system()
    if current_os == 'Linux' or current_os == 'Darwin':
        os.system('resize -s 50 135')
    elif current_os == 'Windows':
        os.system('mode con: cols=135 lines=50')

def check_terminal_size(stdscr):
    w_rows, w_cols = stdscr.getmaxyx()
    if w_cols < 135 or w_rows < 50:
        resize_terminal()
        return False

    return True

def draw_title(stdscr, color):
    title = [
        "                                                                                                    ",
        "                                                                                           .        ",
        "                          ____  _   _ ____    _    ____ _____                           .::^!J7.      ",
        "                         / ___|| | | / ___|  / \  / ___| ____|                       .^!?JJYJYYYY?!.   ",
        "                         \___ \| | | \___ \ / _ \| |  _|  _|                      .~?JJJJ????JJY5PY.  ",
        "                          ___) | |_| |___) / ___ \ |_| | |___                  :!?JJ??????JJYYY5PG7  ",
        "   .^~!777!~^.           |____/ \___/|____/_/   \_\____|_____|             .:~?JJJ??????JJJYY55PGB~  ",
        "  ^JYYJJJJJJJJ?~.                    @dani3lfrenc                       .^!?JJJJ??????JYJYY55PGBP~   ",
        " .Y5YYJJJJ???JJJJ7~^:..                                           .:^!7?JJ????????JJYYY555PGBBJ.    ",
        " .YGP5YYYJ??????JJJJJJ?7!~^:..                            ..:^~!7?JJJJJ???????JJJJYY555PGBGBP~     ",
        "  :5BP555YYJJJ?77????JJJJJJJ???7!!~^^::......:::^^~~!!!!7???J??JJJJ??????77??JJYY555PGBGY^       ",
        "   .?GBGP555YYYJ???7!!777????JJJJJJJJJJ??????JJJJJJJJJJ??JJ???777777???J?JYYYYY55PPGBBGJ.         ",
        "     .JPBBGPP555YYYYJ???!!!!!!7777???????????????????777777!!!!!77JJJJYYY5555PPGBBP?.            ",
        "        ~J5BBBGPP5555YYYJJ???77!!!!!!!!!~!~~~!~~~!!~!!!7???JJJYYYYYY5555PPGGBBBP?~.               ",
        "           ^7YPBBBGGPPPP55555YYYJJYJJJJ??JJJJJJJJJJJJYYYY5555555PPPPGGBBB#BPJ7^.                  ",
        "              :~?PGB#BBBGGPPP555555555555555555555555PPPPGGGBB##BBG5J!~.                          ",
        "                 .^!?J5PGBBBBBBBBGGGGGGGGGGGGGGGGBBBBBB##BBGP5J?!^:.                             ",
        "                          .:^~7?Y5PPGGGGBBGGGGGGGPPP5YJ?7!~^:.                                    ",
        "                                    ...........                                                      ",
        ""
    ]
    
    



    w_rows, w_cols = stdscr.getmaxyx()

    # Calcoliamo la posizione iniziale per centrare orizzontalmente
    start_x = (w_cols - len(title[0])) // 2

    # Stampiamo il titolo riga per riga, in cima alla finestra
    for i, line in enumerate(title):
        stdscr.addstr(i, start_x, line, curses.color_pair(1) | curses.A_BOLD)

    stdscr.refresh()

    
def draw_content(stdscr):
    # GET CPU, MEM and NET usage
    cpu_usage = psutil.cpu_percent(percpu=True)
    mem_usage = psutil.virtual_memory()
    net_usage = psutil.net_io_counters(pernic=False, nowrap=True)
    processes = list(psutil.process_iter(['pid', 'name', 'username']))

    draw_title(stdscr, curses.color_pair(1))

    cpu_start_row, cpu_start_col = stdscr.getyx()
    cpu_start_col = 0
    cpu_start_row += 2

    #------------------
    # Draw the CPU info

    stdscr.addstr(cpu_start_row, cpu_start_col + 1, "CPU INFO", curses.A_BOLD | curses.color_pair(1))

    for i, usage in enumerate(cpu_usage):
        stdscr.addstr(cpu_start_row + 2 + i, cpu_start_col + 2, f"CPU {i+1}: {usage}%")

    total_cpu_usage = psutil.cpu_percent()
    stdscr.addstr(cpu_start_row + 2 + len(cpu_usage) + 1, cpu_start_col + 2, f"CPU total use: {total_cpu_usage:.2f}%")
    cpu_final_row = cpu_start_row + 2 + len(cpu_usage) + 3 


    #------------------
    # Draw the MEM info
    mem_start_row = cpu_start_row
    mem_start_col = 30
    stdscr.addstr(mem_start_row, mem_start_col, "MEMORY INFO", curses.A_BOLD | curses.color_pair(1))
    mem_available_gb = mem_usage.available / (1024 ** 3)
    mem_used_gb = mem_usage.used / (1024 ** 3)
    mem_total_gb = mem_usage.total / (1024 ** 3)
    mem_start_col += 1
    stdscr.addstr(mem_start_row + 2, mem_start_col, f"Memory available: {mem_available_gb:.2f} GB")
    stdscr.addstr(mem_start_row + 3, mem_start_col, f"Memory used: {mem_used_gb:.2f} GB")
    stdscr.addstr(mem_start_row + 5, mem_start_col, f"Total memory: {mem_total_gb:.2f} GB")

    #------------------
    # Draw the DISK info
    disk_start_row = mem_start_row
    disk_start_col = 60
    disk_usage = psutil.disk_usage('/')
    disk_free_gb = disk_usage.free / (1024 ** 3)
    disk_used_gb = disk_usage.used / (1024 ** 3)
    stdscr.addstr(disk_start_row, disk_start_col, "DISK INFO", curses.A_BOLD | curses.color_pair(1))
    disk_start_col += 1
    stdscr.addstr(disk_start_row + 2, disk_start_col, f"Disk free: {disk_free_gb:.2f} GB")
    stdscr.addstr(disk_start_row + 3, disk_start_col, f"Disk used: {disk_used_gb:.2f} GB")

    #------------------
    # Draw the NETWORK info
    net_start_row = disk_start_row
    net_start_col = 90
    stdscr.addstr(net_start_row, net_start_col, "NETWORK INFO", curses.A_BOLD | curses.color_pair(1))
    net_start_col += 1
    stdscr.addstr(net_start_row + 2, net_start_col, f"Bytes sent: {net_usage.bytes_sent}")
    stdscr.addstr(net_start_row + 3, net_start_col, f"Bytes received: {net_usage.bytes_recv}")
    stdscr.addstr(net_start_row + 4, net_start_col, f"Packets sent: {net_usage.packets_sent}")
    stdscr.addstr(net_start_row + 5, net_start_col, f"Packets received: {net_usage.packets_recv}")
    hostname = socket.gethostname()
    ipAdd = socket.gethostbyname(hostname)
    stdscr.addstr(net_start_row + 6, net_start_col, f"Local IP address: {ipAdd}")

    # Draw the PROCESSES info
    proc_start_row = cpu_final_row
    proc_start_col = 1
    stdscr.addstr(proc_start_row, proc_start_col, "PROCESSES", curses.A_BOLD | curses.color_pair(1))
    proc_start_row += 2
    stdscr.addstr(proc_start_row, proc_start_col + 1, "PID", curses.color_pair(1))
    stdscr.addstr(proc_start_row, proc_start_col + 10, "NAME", curses.color_pair(1))
    stdscr.addstr(proc_start_row, proc_start_col + 40, "USERNAME", curses.color_pair(1))

    for i, proc in enumerate(processes[cpu_final_row:], start=proc_start_row + 2):
        if i >= stdscr.getmaxyx()[0] - 2:
            break
        pid = proc.info['pid']
        name = str(proc.info['name'])[:20]
        username = str(proc.info['username'])[:15]
        stdscr.addstr(i, proc_start_col, f"{pid:5}")
        stdscr.addstr(i, proc_start_col + 10, f"{name}")
        stdscr.addstr(i, proc_start_col + 40, f"{username}")

def draw_screen(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(1000)
    curses.start_color()

    # For titles
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    # For bottom bar
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)

    while True:
        stdscr.erase()

        if not check_terminal_size(stdscr):
            stdscr.addstr(0, 0, "Resizing terminal to at least 100x20...", curses.color_pair(1))
            check_terminal_size(stdscr)
        else:
            draw_content(stdscr)
            # Draw the bottom bar
            w_rows, w_cols = stdscr.getmaxyx()
            stdscr.addstr(w_rows - 1, 0, "Press \"q\" to exit", curses.color_pair(2))
            stdscr.addstr(w_rows - 1, 20, "Press \"s\" for search", curses.color_pair(2))

        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('q'):
            break

def main():
    curses.wrapper(draw_screen)

if __name__ == "__main__":
    main()
