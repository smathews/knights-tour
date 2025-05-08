import curses

moves = [
    (1,-2),
    (-2,1),
    (-1,2),
    (2,-1),
    (-2,-1),
    (2,1),
    (-1,-2),
    (1,2),
]

size = (8,8)
tour = [[1,1,-1]] # x, y, next move idx (ordered)
count = 0

def main(screen):
    # No cursor
    curses.curs_set(0)

    screen.clear()
    win = curses.newwin(size[1] + 2, (size[0] * 2) + 3, 2, 3)

    def visited(pos):
        for p in tour:
            if p[:2] == pos[:2]:
                return True
        return False

    def out_of_bound(pos):
        x, y = pos[:2]
        max_x, max_y = size
        if x < 1 or x > max_x:
            return True
        if y < 1 or y > max_y:
            return True
        return False

    def get_next_pos(pos):
        x,y = pos[:2]
        dx,dy = moves[pos[2]]
        return [x+dx, y+dy, -1]

    def render(tour, win):
        win.clear()
        win.box()
        for pos in tour:
            n = str(pos[2])
            if n == "-1":
                n = "N"
            win.addch(size[1] - pos[1] + 1, (pos[0] * 2), ord(n))
        win.refresh()

    global count
    while len(tour) < (size[0] * size[1]):
        tour[-1][2] +=1
        if tour[-1][2] == len(moves):
            # give up
            tour.pop()
            continue
        n = get_next_pos(tour[-1])
        if not (out_of_bound(n) or visited(n)):
            # add our move
            tour.append(n)
            # print some output
            count += 1
            if count & (2**10 - 1) == 0:
                screen.addstr(0,0,"Move number: %s" % count)
                screen.refresh()
                render(tour, win)

if __name__ == '__main__':
    curses.wrapper(main)
    print("Solved in %s moves" % count)
    print(tour)
