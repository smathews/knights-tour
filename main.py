import curses, itertools, sys

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
start = [1,1,-1]
best_count = 0
best_iteration = moves
bset_tour = []

def main(screen):
    # No cursor
    curses.curs_set(0)

    screen.clear()
    win = curses.newwin(size[1] + 2, (size[0] * 2) + 3, 2, 3)

    def visited(pos, tour):
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

    def get_next_pos(pos, moves):
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

    global best_count
    global best_iteration
    global best_tour

    # Search for best iteration or use default
    if len(sys.argv) > 1:
        iterations = list(itertools.permutations(moves))
    else:
        iterations = [moves]

    for i in range(len(iterations)):
        x = iterations[i]
        count = 0
        tour = [start.copy()]
        screen.clear()
        while len(tour) < (size[0] * size[1]):
            tour[-1][2] +=1
            if tour[-1][2] == len(moves):
                # give up
                tour.pop()
                continue
            n = get_next_pos(tour[-1], x)
            if not (out_of_bound(n) or visited(n, tour)):
                # add our move
                tour.append(n)
                # print some output
                count += 1
                if count & (2**8 - 1) == 0:
                    if best_count > 0 and count > best_count:
                        break
                    screen.addstr(1,0,"Iteration (remaining %s) %s" % (len(iterations)-i, list(x)))
                    screen.addstr(0,0,"Move number (best %s): %s" % (best_count, count))
                    screen.refresh()
                    render(tour, win)
        if best_count == 0 or count < best_count:
            best_iteration = x
            best_count = count
            best_tour = tour

if __name__ == '__main__':
    curses.wrapper(main)
    print("Solved in %s moves" % best_count)
    print("With iteration: %s" % list(best_iteration))
    print(best_tour)
