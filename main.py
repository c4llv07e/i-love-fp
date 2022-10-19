#!/usr/bin/env python

import pygame
import sys
import math

from itertools import repeat
from functools import partial

sign = partial(math.copysign, 1)

stateid_is_running = 0
stateid_rects = 1
stateid_screen = 2

insert_into_tuple = lambda tpl, ind, val: \
    tpl[:ind] + (val,) + tpl[ind + 1:]

startup_state = lambda screen: \
        (True, [(pygame.Rect(0, 0, 40, 40), pygame.Vector2(1, 1)) \
               ,(pygame.Rect(280, 230, 40, 40), pygame.Vector2(1, 1)) \
               ,(pygame.Rect(480, 30, 20, 40), pygame.Vector2(1, 1)) \
                ], screen)

state_is_running = lambda state: \
        state[stateid_is_running]

state_rects = lambda state: \
        state[stateid_rects]

state_screen = lambda state: \
        state[stateid_screen]

handle_rect = lambda state, rect: \
        (pygame.Rect( \
            rect[0].x + rect[1].x, \
            rect[0].y + rect[1].y, \
        rect[0].w, rect[0].h), \
        pygame.Vector2( \
            (-rect[1].x if state_screen(state).get_size()[0] <= (rect[0].x + rect[1].x + rect[0].w) \
                        or rect[0].x + rect[1].x <= 0 else rect[1].x), \
            (-rect[1].y if state_screen(state).get_size()[1] <= (rect[0].y + rect[1].y + rect[0].h) \
                        or rect[0].y + rect[1].y <= 0 else rect[1].y), \
            ))

draw_rect = lambda state, rect: \
        pygame.draw.rect(state_screen(state), (0, 255, 255), rect[0]) == None and \
        None

draw_state = lambda state: \
        list(map(partial(draw_rect, state), state_rects(state))) != None and \
        None

handle_rects = lambda state: \
        insert_into_tuple(state, stateid_rects, list(map(partial(handle_rect, state), state_rects(state))))

handle_events = lambda state: \
        (lambda events: \
            (lambda events_types: \
                insert_into_tuple(state, stateid_is_running, \
                    (False if pygame.QUIT in events_types else state_is_running(state))) \
            )([event.type for event in events]) \
        )([event for event in pygame.event.get()])

main_end = lambda state: \
        sys.exit(0)

main_loop = lambda state: \
        (main_end(state) if not state_is_running(state) else \
            state_screen(state).fill((0, 0, 0)) \
            and draw_state(state) == None \
            and pygame.display.flip() == None \
            and handle_rects(handle_events(state)) \
            )

main = lambda: \
    pygame.init() != None \
    and (lambda screen: \
        (lambda state: \
            pygame.display.set_caption("functional game on python with pygame") == None \
            and [(state := main_loop(state)) for _ in repeat(())] \
        )(startup_state(screen))
    )(pygame.display.set_mode((600, 400)))

__name__ == "__main__" and main()
