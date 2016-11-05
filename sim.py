import math
import itertools

T_MAX = 42 * 24 * 60

# TODO
# Right now this only works if either (x1, y1) or (x2, y2) is a grid point (both coordinates are integers)
# (Although in all usages in the code so far, indeed either the start or destination is a grid point)
def dist(x1, y1, x2, y2):
  return abs(x1 - x2) + abs(y1 - y2)

def time_to(x1, y1, x2, y2, speed):
  d = dist(x1, y1, x2, y2)
  return d / speed

def dist_to_edge(x, y):
  return min(x - 1, 10 - x, y - 1, 10 - y)

class Simulator(object):

  def __init__(self):
    # Start near middle of grid
    self.x = 5
    self.y = 5
    # Value of all pokemon caught
    self.v = 0
    # Current time
    self.t = 0.0
    self.speed = 2.0 / 15
    # Pokemon to try to catch
    # List of tuples (poke_x, poke_y, poke_v, poke_remaining_time)
    self.goals = []

  # A new pokemon appears
  def poke(self, poke_x, poke_y, poke_v, poke_t):
    self.sim_until(poke_t)
    self.update_goals(poke_x, poke_y, poke_v)

  # No more pokemon
  def end(self, end_t):
    self.sim_until(end_t)

  # Adds a pokemon to list of goals if the pokemon is in range
  def update_goals(self, poke_x, poke_y, poke_v):
    if time_to(self.x, self.y, poke_x, poke_y, self.speed) <= 15:
      poke = (poke_x, poke_y, poke_v, 15)
      n = len(self.goals)
      best_value = -1
      best_goals = None
      # Brute force search for best way to rearrange list of goals
      self.goals.append(poke)
      for order in itertools.permutations(self.goals):
        value = self.value_goals(list(order))
        if value > best_value:
          best_value = value
          best_goals = order[:]
      self.goals = list(best_goals)
  
  # Value of a list of goals
  def value_goals(self, goals_copy):
    value = 0
    x = self.x
    y = self.y
    # Go to each goal in order
    for i in range(len(goals_copy)):
      poke = goals_copy[i]
      t = time_to(x, y, poke[0], poke[1], self.speed)
      x = poke[0]
      y = poke[1]
      if t <= poke[3]:
        value += poke[2]
      # Subtract the time needed from the remaining time of the other goals
      for j in range(i + 1, len(goals_copy)):
        goals_copy[j] = goals_copy[j][:3] + (goals_copy[j][3] - t,)
    return value

  # Simulate until time t
  def sim_until(self, t):
    # If no pokemon in range, do nothing
    if not self.goals:
      self.t = t
      return
    time_left = t - self.t
    if time_left <= 0:
      self.t = t
      return
    goal = self.goals[0]
    time_needed = time_to(self.x, self.y, goal[0], goal[1], self.speed)

    # Reach next goal if possible
    if time_needed <= time_left:
      self.x = goal[0]
      self.y = goal[1]
      if time_needed <= goal[3]:
        self.v += goal[2]
      self.t += time_needed
      self.goals.pop(0)
      for goal in self.goals:
        goal = goal[:3] + (goal[3] - time_needed,)
      self.goals = [g for g in self.goals if g[3] >= 0]
      time_left -= time_needed
      if time_left > 0:
        self.sim_until(t)
    else:
      # Simulate steps
      time_left = self.sim_until_int(t, time_left, goal)
      if time_left > 0:
        self.sim_until_done(t, time_left, goal)

  # Simulates until reaching one of the grid points, or if time_left reaches 0
  def sim_until_int(self, t, time_left, goal):
    old_time_left = time_left
    up = self.y < goal[1]
    down = self.y > goal[1]
    right = self.x < goal[0]
    left = self.x > goal[0]
    # We're in the middle of a vertical edge
    if self.x % 1 == 0 and self.y % 1 != 0:
      if up:
        time_needed = time_to(self.x, self.y, self.x, math.ceil(self.y), self.speed)
        if time_needed <= time_left:
          self.y = math.ceil(self.y)
          self.t += time_needed
          time_left -= time_needed
        else:
          self.y += time_left * self.speed
          self.t = t
          time_left = 0
      else:
        time_needed = time_to(self.x, self.y, self.x, math.floor(self.y), self.speed)
        if time_needed <= time_left:
          self.y = math.floor(self.y)
          self.t += time_needed
          time_left -= time_needed
        else:
          self.y -= time_left * self.speed
          self.t = t
          time_left = 0
    # We're in the middle of a horizontal edge
    elif self.y % 1 == 0 and self.x % 1 != 0:
      if right:
        time_needed = time_to(self.x, self.y, math.ceil(self.x), self.y, self.speed)
        if time_needed <= time_left:
          self.x = math.ceil(self.x)
          self.t += time_needed
          time_left -= time_needed
        else:
          self.x += time_left * self.speed
          self.t = t
          time_left = 0
      else:
        time_needed = time_to(self.x, self.y, math.floor(self.x), self.y, self.speed)
        if time_needed <= time_left:
          self.x = math.floor(self.x)
          self.t += time_needed
          time_left -= time_needed
        else:
          self.x -= time_left * self.speed
          self.t = t
          time_left = 0
    time_elapsed = old_time_left - time_left
    for goal in self.goals:
      goal = goal[:3] + (goal[3] - time_elapsed,)
    self.goals = [g for g in self.goals if g[3] >= 0]
    return time_left

  # Starting at a point with integer coordinates, simulate until time_left reaches 0
  def sim_until_done(self, t, time_left, goal):
    old_time_left = time_left
    time_per_block = 1 / self.speed
    while time_left > 0:
      up = self.y < goal[1]
      down = self.y > goal[1]
      right = self.x < goal[0]
      left = self.x > goal[0]
      up_dist = dist_to_edge(self.x, self.y + 1)
      down_dist = dist_to_edge(self.x, self.y - 1)
      right_dist = dist_to_edge(self.x + 1, self.y)
      left_dist = dist_to_edge(self.x - 1, self.y)
      # Decide which direction to go next, trying to stay away from edges if possible
      if up:
        if right and right_dist > up_dist:
          self.right(time_left, time_per_block)
        elif left and left_dist > up_dist:
          self.left(time_left, time_per_block)
        else:
          self.up(time_left, time_per_block)
      elif down:
        if right and right_dist > down_dist:
          self.right(time_left, time_per_block)
        elif left and left_dist > down_dist:
          self.left(time_left, time_per_block)
        else:
          self.down(time_left, time_per_block)
      elif right:
        if up and up_dist > right_dist:
          self.up(time_left, time_per_block)
        elif down and down_dist > right_dist:
          self.down(time_left, time_per_block)
        else:
          self.right(time_left, time_per_block)
      else:
        if up and up_dist > left_dist:
          self.up(time_left, time_per_block)
        elif down and down_dist > left_dist:
          self.down(time_left, time_per_block)
        else:
          self.left(time_left, time_per_block)
      self.t += min(time_left, time_per_block)
      time_left -= time_per_block
    self.t = t
    for goal in self.goals:
      goal = goal[:3] + (goal[3] - old_time_left,)
    self.goals = [g for g in self.goals if g[3] >= 0]

  # Move up, down, left, or right one block, or until time_left reaches 0

  def up(self, time_left, time_per_block):
    if time_left >= time_per_block:
      self.y += 1
    else:
      self.y += time_left * self.speed

  def down(self, time_left, time_per_block):
    if time_left >= time_per_block:
      self.y -= 1
    else:
      self.y -= time_left * self.speed

  def right(self, time_left, time_per_block):
    if time_left >= time_per_block:
      self.x += 1
    else:
      self.x += time_left * self.speed

  def left(self, time_left, time_per_block):
    if time_left >= time_per_block:
      self.x -= 1
    else:
      self.x -= time_left * self.speed

if __name__ == "__main__":
  sim = Simulator()
  with open("Providence_Pokemon_1.csv", "r") as f:
    for line in f:
      x, y, v, t = map(int, line.split(","))
      sim.poke(x, y, v, t)
  sim.end(T_MAX)
  print sim.v

















