
import psutil
import time
import curses

def draw_screen(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(1000)


    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)


    while True:
        stdscr.erase()
        #GET CPU USAGE
        cpu_usage = psutil.cpu_percent(percpu=True)
        mem_usage = psutil.virtual_memory()

        #------------------
        # Draw the CPU info


        stdscr.addstr(2, 0, "CPU USAGE", curses.A_BOLD|curses.color_pair(1))
        for i, usage in enumerate(cpu_usage):
            stdscr.addstr(4 + i, 2, f"CPU {i}: {usage}%")
        total_cpu_usage = psutil.cpu_percent()
        stdscr.addstr(4 + len(cpu_usage) + 1, 2, f"CPU TOTAL USE: {total_cpu_usage:.2f}%")

        #------------------
        #Draw the line between CPU and MEM

        y, x = stdscr.getyx()
        barrier_column_cpu_mem = 25 + 4 
        for i in range(2, y):
            stdscr.addstr(i, barrier_column_cpu_mem, "|")
        stdscr.addstr(2, barrier_column_cpu_mem + 4, "MEMORY USED", curses.A_BOLD | curses.color_pair(1))


        #------------------
        # Draw the mem info
        mem_usage = psutil.virtual_memory()
        mem_available_gb = mem_usage.available / (1024 ** 3) 
        mem_used_gb = mem_usage.used / (1024 ** 3)  

        newY, newX = stdscr.getyx()
        newY = 4
        newX = barrier_column_cpu_mem + 4 + 1
        stdscr.addstr(newY, newX, f"MEMORY AVAILABLE: {mem_available_gb:.2f} GB")
        stdscr.addstr(newY + 1, newX, f"MEMORY USED: {mem_used_gb:.2f} GB")


        stdscr.refresh()
        if stdscr.getch() == ord('q'):
            break


def main():
    curses.wrapper(draw_screen)

if __name__ == "__main__":
    main()    