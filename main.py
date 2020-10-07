"""Solver for Rubik's cube.

Cube must be arranged so that the white face is front and the top face is red.
"""
import copy
import time
from typing import List
import cProfile

import k_best
import state

INITIAL_STATE = state.State(
  front='OWBOWWWBB',
  up='GRRWROWBO',
  left='ORBBBWWBR',
  right='YYGGGGYGG',
  back='YYWRYYYGG',
  down='BRROOORYO')
INITIAL_STATE = state.State(front='GWBWWWWBW', back='YBYYYYYYY', up='RRRYRRRBR',
                            down='OOOOOGOOO', left='BRWBBRBWB',
                            right='WGGGGGGOG')
INITIAL_STATE = state.State(front='BWWWWWWWW', back='WYGYYYYYY', up='RRRRRRRGR',
                            down='OBOOOOOOO', left='YBYBBRBGB',
                            right='GGBOGGGBG')
INITIAL_STATE = state.State(front='WWGWWWWWW', back='BYWYYYYYY', up='RRRRRRRBR',
                            down='OGOOOOOOO', left='GBBBBRBBB',
                            right='YGYOGGGGG')
INITIAL_STATE = state.State(front='RWWWWWBWW', back='YYWYYYYYY', up='RRRRRRYRB',
                            down='WOOOOOOOO', left='GBBBBBBBO',
                            right='RGGGGGGGG')
INITIAL_STATE = state.State(front='RWOWWWBWW', back='YYYYYYYYY', up='RRRRRRWRB',
                            down='ROOOOOOOO', left='BBGBBBBBW',
                            right='WGGGGGGGG')

recurse_calls = 0

seen_states = set()
hits = 0
misses = 0


def recurse(cur_state: state.State, init_state: state.State, depth: int,
            path: List[int], best: k_best.KBest) -> None:
  global recurse_calls, seen_states, hits, misses
  recurse_calls += 1
  # encoded_state = cur_state.encode()
  # if encoded_state in seen_states:
  #   hits += 1
  # else:
  #   misses += 1
  #   seen_states.add(encoded_state)

  cost = cur_state.cube_cost()
  if cost < best.worst_cost and cur_state != init_state:
    best.maybe_add(list(path), copy.deepcopy(cur_state),
                   cur_state.cube_cost())

  if depth == 0:
    return

  for plane in range(6):
    if (len(path) >= 3 and path[-1] == path[-2] and path[-1] == path[-3] and
        path[-1] == plane):
      continue  # Four consecutive identical ops is a no-op.
    if len(path) >= 10 and plane not in path[-10:] and len(set(path[-10:])) == 5:
      continue  ############ DANGEROUS HEURISTIC ############
    path.append(plane)
    cur_state.rotate(plane)
    recurse(cur_state, init_state, depth - 1, path, best)
    del path[-1]
    cur_state.rotate(plane)
    cur_state.rotate(plane)
    cur_state.rotate(plane)
  if len(path) > 1 and path[-1] != path[-2]:
    # add two more of the last op
    plane = path[-1]
    path.append(plane)
    path.append(plane)
    cur_state.rotate(plane)
    cur_state.rotate(plane)
    recurse(cur_state, init_state, depth - 1, path, best)
    del path[-1]
    del path[-1]
    cur_state.rotate(plane)
    cur_state.rotate(plane)


def main():
  print(INITIAL_STATE)
  print(f'Initial cost: Cube={INITIAL_STATE.cube_cost()}, '
        f'Naive={INITIAL_STATE.naive_cost()}')

  MAX_DEPTH_1 = 9
  MAX_DEPTH_2 = 8
  BEAM_SIZE = 20

  # Encoded states which have run through the crawler already.
  already_crawled = set()

  best = k_best.KBest(BEAM_SIZE)
  start_time = time.time()
  cur_state = copy.deepcopy(INITIAL_STATE)
  recurse(cur_state, INITIAL_STATE, MAX_DEPTH_1, [], best)
  print('Finished expansion crawl in %.2f sec. Best so far: %d' % (
    time.time() - start_time, best.best_cost))

  for ncrawl in range(5):
    new_bests = []
    for item in best.items:
      new_bests.append(k_best.KBest(BEAM_SIZE))
      new_bests[-1].maybe_add(list(item.path), copy.deepcopy(item.state),
                              item.cost)
      if item.encoded_state in already_crawled:
        print('Skipped level %d crawl #%d: cost %d' % (
          ncrawl, len(new_bests), item.cost))
      else:
        recurse(item.state, INITIAL_STATE, MAX_DEPTH_2, item.path,
                new_bests[-1])
        already_crawled.add(item.encoded_state)
        print(
          'Finished level %d crawl #%d, elapsed: %.2f sec, best here: %d' % (
            ncrawl, len(new_bests), time.time() - start_time,
            new_bests[-1].best_cost))
    best = k_best.merge_kbests(new_bests, BEAM_SIZE)
    print('End of level %d: Best costs %s' % (
      ncrawl, [item.cost for item in best.items]))

  end_time = time.time() + 1e-3

  for item in best.items:
    print('Cost %2d: Path=%s' % (
      item.cost, ' '.join(state.ROTATIONS[i] for i in item.path)))

  end_state = copy.deepcopy(INITIAL_STATE)
  for rot in best.items[0].path:
    end_state.rotate(rot)
    end_state.validate()
  print(f'end_state cube cost: {end_state.cube_cost()}')
  print(f'end_state naive cost: {end_state.naive_cost()}')
  print(f'best_cost: {best.best_cost}')

  print('%d recurse calls in %.2f sec (%.0f calls/sec)' % (
    recurse_calls, end_time - start_time,
    recurse_calls / (end_time - start_time)))

  print(end_state)
  print(repr(end_state))


if __name__ == '__main__':
  # cProfile.run('main()')
  main()
