
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



        stdscr.addstr(2, 0, "CPU USAGE", curses.A_BOLD|curses.color_pair(1))
        for i, usage in enumerate(cpu_usage):
            stdscr.addstr(4 + i, 2, f"CPU {i}: {usage}%")
        total_cpu_usage = sum(cpu_usage)/len(cpu_usage)
        stdscr.addstr(4 + len(cpu_usage) + 1, 2, f"AVERAGE CPU TOTAL USE: {total_cpu_usage:.2f}%")

        stdscr.refresh()

        if stdscr.getch() == ord('q'):
            break

def main():
    curses.wrapper(draw_screen)

if __name__ == "__main__":
    main()    