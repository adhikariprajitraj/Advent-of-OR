import random

def manhattan_distance(pos1, pos2):
    """Calculates the L1 distance between two points on the grid."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def sign(x):
    """Returns the sign of a number (-1, 0, or 1)."""
    if x > 0: return 1
    if x < 0: return -1
    return 0

def simulate_spider_fly_game(spider_start_pos, fly_start_pos):
    spider_pos = list(spider_start_pos)
    fly_pos = list(fly_start_pos)
    turn = 0
    
    initial_distance = manhattan_distance(spider_pos, fly_pos)
    print(f"--- START ---")
    print(f"Spider start: {spider_pos}")
    print(f"Fly start:    {fly_pos}")
    print(f"Initial Manhattan Distance: {initial_distance}\n")

    while spider_pos != fly_pos:
        turn += 1
        print(f"--- TURN {turn} ---")

        # ================= FLY'S TURN (1 Move) =================
        # The fly tries to escape by moving to a random neighbor.
        possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        fly_move = random.choice(possible_moves)
        
        fly_pos[0] += fly_move[0]
        fly_pos[1] += fly_move[1]
        
        dist_after_fly = manhattan_distance(spider_pos, fly_pos)
        print(f"[Fly] moves {fly_move} to {fly_pos}. Distance: {dist_after_fly}")
        
        if spider_pos == fly_pos:
            print("Fly accidentally landed on the spider!")
            break

        # ================= SPIDER'S TURN (2 Moves) =================
        # The spider assesses the situation based on the fly's new position.
        sx, sy = spider_pos
        fx, fy = fly_pos
        dx = fx - sx
        dy = fy - sy
        
        # Determine the total move based on the optimal strategy
        total_spider_move = [0, 0]
        move_description = ""

        if dx != 0 and dy != 0:
            # CASE A: Diagonal.
            # Strategy: Move 1 step in x and 1 step in y towards the quadrant.
            # This utilizes both moves to reduce distance in both dimensions.
            total_spider_move[0] = sign(dx)
            total_spider_move[1] = sign(dy)
            move_description = f"diagonal towards quadrant ({sign(dx)}, {sign(dy)})"
        else:
            # CASE B: On the same axis (row or column).
            # Strategy: Move 2 steps directly along that axis towards the fly.
            # We use min(2, abs(dist)) to avoid overshooting if dist is 1.
            if dx != 0:
                move_amount = sign(dx) * min(2, abs(dx))
                total_spider_move[0] = move_amount
                move_description = f"{abs(move_amount)} steps along X-axis"
            elif dy != 0:
                move_amount = sign(dy) * min(2, abs(dy))
                total_spider_move[1] = move_amount
                move_description = f"{abs(move_amount)} steps along Y-axis"
        
        # Apply the spider's moves
        spider_pos[0] += total_spider_move[0]
        spider_pos[1] += total_spider_move[1]
        
        final_dist = manhattan_distance(spider_pos, fly_pos)
        print(f"[Spider] executes strategy: moves {move_description}.")
        print(f"         New position: {spider_pos}. New Distance: {final_dist}\n")

    print("--- GAME OVER ---")
    print(f"The spider caught the fly in {turn} turns!")
    if turn <= initial_distance:
        print(f"Verification successful: Turns ({turn}) <= Initial Distance ({initial_distance}).")

# ================= Run the Simulation =================
# You can change these starting positions to test different scenarios.
start_spider = (0, 0)
# Place the fly far away diagonally to test the main strategy.
start_fly = (6, 7) 

simulate_spider_fly_game(start_spider, start_fly)