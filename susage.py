import psutil
import curses


def search_resource():
    pass




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

        stdscr.addstr(cpu_start_row, cpu_start_col, "CPU USAGE", curses.A_BOLD | curses.color_pair(1))

        for i, usage in enumerate(cpu_usage):
            stdscr.addstr(cpu_start_row + 2 + i, cpu_start_col + 2, f"CPU {i}: {usage}%")

        total_cpu_usage = psutil.cpu_percent()
        stdscr.addstr(cpu_start_row + 2 + len(cpu_usage) + 1, cpu_start_col + 2, f"CPU TOTAL USE: {total_cpu_usage:.2f}%")




        #------------------
        # Draw the line between CPU and MEM
        barrier_column_cpu_mem = 35
        for i in range(cpu_start_row, cpu_start_row + 2 + len(cpu_usage) + 2):
            stdscr.addstr(i, barrier_column_cpu_mem, "|")

        #------------------
        # Draw the MEM info
        mem_start_row = cpu_start_row
        mem_start_col = barrier_column_cpu_mem + 4
        stdscr.addstr(mem_start_row, mem_start_col, "MEMORY USED", curses.A_BOLD | curses.color_pair(1))
        mem_available_gb = mem_usage.available / (1024 ** 3)
        mem_used_gb = mem_usage.used / (1024 ** 3)
        stdscr.addstr(mem_start_row + 2, mem_start_col, f"MEMORY AVAILABLE: {mem_available_gb:.2f} GB")
        stdscr.addstr(mem_start_row + 3, mem_start_col, f"MEMORY USED: {mem_used_gb:.2f} GB")

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
