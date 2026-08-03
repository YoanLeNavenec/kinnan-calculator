def create_pool():
    # Create a pool of mana
    pool = {
        "white": 0,
        "blue": 0,
        "black": 0,
        "red": 0,
        "green": 0,
        "colorless": 0
    }
    return pool

def add_mana(pool, color, amount):
    # Add mana to the pool
    pool[color] = pool[color] + amount
    return pool

def get_total_multiplier(doublers):
    multiplier = 1
    for doubler in doublers:
        if doubler["active"]:
            multiplier *= doubler["factor"] ** doubler["copies"]
    return multiplier
  
def tap_source(pool, source, multiplier):
  tap = source["amount"] * multiplier
  add_mana(pool, source["color"], tap)
  return pool

def pay_cost(pool, amount):
    for color in ["colorless", "green", "blue"]:
      pay = min(pool[color], amount)
      pool[color] -= pay
      amount -= pay
    return pool

def pay_pips(pool, pips):
  for pip in pips:
    if pool[pip] < 1:
      return None
  for color in pips:
    pool[color] -= 1
  return pool

def can_afford(pool, generic_cost, pips):
  for pip in pips:
    if pool[pip] < 1:
      return False
  
  leftover = 0
  for color in ["colorless", "green", "blue"]:
    available = pool[color]
    if color in pips:
      available -= 1
    leftover += available
    
  return leftover >= generic_cost
