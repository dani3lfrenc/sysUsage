#!/usr/bin/env python3


import os
import psutil
import curses
import platform



def search_resource():
    pass

def resize_terminal():
    current_os = platform.system()
    if current_os == 'Linux' or current_os == 'Darwin':
        os.system('resize -s 30 100')
    elif current_os == 'Windows':
        os.system('mode con: cols=100 lines=30')

def check_terminal_size(stdscr):
    while True:
        w_rows, w_cols = stdscr.getmaxyx()
        if w_cols >= 100 and w_rows >= 20:
            break
        stdscr.clear()
        stdscr.addstr(0, 0, "Resizing terminal to at least 100x20...", curses.color_pair(1))
        stdscr.refresh()
        resize_terminal()
        stdscr.refresh()
        curses.napms(1000)


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

    check_terminal_size(stdscr)


    while True:
        stdscr.erase()

        # GET CPU USAGE and MEM USAGE
        cpu_usage = psutil.cpu_percent(percpu=True)
        mem_usage = psutil.virtual_memory()



        #------------------
        # Draw the bottom bar
        w_rows, w_cols = stdscr.getmaxyx()
        stdscr.addstr(w_rows-1, 0, "Press \"q\" to exit", curses.color_pair(2))
        rows, cols = stdscr.getyx()
        stdscr.addstr(w_rows-1, cols +2 , "Press \"s\" for search", curses.color_pair(2))

        #------------------
        # Draw the CPU info
        cpu_start_row = 2
        cpu_start_col = 0

        stdscr.addstr(cpu_start_row, cpu_start_col, "CPU INFO", curses.A_BOLD | curses.color_pair(1))

        for i, usage in enumerate(cpu_usage):
            stdscr.addstr(cpu_start_row + 2 + i, cpu_start_col + 2, f"CPU {i}: {usage}%")

        total_cpu_usage = psutil.cpu_percent()
        stdscr.addstr(cpu_start_row + 2 + len(cpu_usage) + 1, cpu_start_col + 2, f"CPU total use: {total_cpu_usage:.2f}%")


        #------------------
        # Draw the line between CPU and MEM
        barrier_column_cpu_mem = 30
        for i in range(cpu_start_row, 14):
            stdscr.addstr(i, barrier_column_cpu_mem, "|")

        #------------------
        # Draw the MEM info
        mem_start_row = cpu_start_row
        mem_start_col = barrier_column_cpu_mem + 4
        stdscr.addstr(mem_start_row, mem_start_col, "MEMORY INFO", curses.A_BOLD | curses.color_pair(1))
        mem_available_gb = mem_usage.available / (1024 ** 3)
        mem_used_gb = mem_usage.used / (1024 ** 3)
        mem_total_gb = mem_usage.total / (1024 ** 3)
        mem_start_col+=1
        stdscr.addstr(mem_start_row + 2, mem_start_col, f"Memory avaiable: {mem_available_gb:.2f} GB")
        stdscr.addstr(mem_start_row + 3, mem_start_col, f"Memory used: {mem_used_gb:.2f} GB")
        stdscr.addstr(mem_start_row + 5, mem_start_col, f"Total memory: {mem_total_gb:.2f} GB")


        #------------------
        # Draw the line between MEM and DISK
        barrier_column_mem_disk = 62
        for i in range(mem_start_row, 14):
            stdscr.addstr(i, barrier_column_mem_disk, "|")


        #------------------
        # Draw the DISK info
        disk_start_row = mem_start_row
        disk_start_col = barrier_column_mem_disk + 4
        disk_usage = psutil.disk_usage('/')
        disk_free_gb = disk_usage.free / (1024 ** 3)
        disk_used_gb = disk_usage.used / (1024 ** 3)
        stdscr.addstr(disk_start_row, disk_start_col, "DISK INFO", curses.A_BOLD | curses.color_pair(1))
        disk_start_col+= 1
        stdscr.addstr(disk_start_row + 2, disk_start_col, f"Disk free : {disk_free_gb:.2f} GB")
        stdscr.addstr(disk_start_row + 3, disk_start_col, f"Disk used: {disk_used_gb:.2f} GB")

        #------------------
        # Draw the line between MEM and DISK
        barrier_column_mem_disk = 90
        for i in range(disk_start_row, 14):
            stdscr.addstr(i, barrier_column_mem_disk, "|")


        stdscr.refresh()
        key = stdscr.getch()
        if key == ord('s'):
            search_resource()
        elif key == ord('q'):
            break

def main():
    curses.wrapper(draw_screen)

if __name__ == "__main__":
    main()
