import random

def simulate_games(change):
    # Represent doors: 1 = prize, 0 = no prize
    doors = [1, 0, 0]
    wins = 0.0
    number_of_simulations = 10000

    for _ in range(number_of_simulations):
        random.shuffle(doors)  # Shuffle doors
        user_index = random.randint(0, 2)  # User chooses a door
        car_index = doors.index(1)  # Find the prize door

        # Simulate Monty opening a door
        available_indexes = [0, 1, 2]
        available_indexes.remove(user_index)  # Monty can't open the user's door
        if car_index != user_index:
            available_indexes.remove(car_index)  # Monty won't open the prize door
        monty_opens = random.choice(available_indexes)

        if change:
            # User switches to the remaining door
            remaining_door = [i for i in [0, 1, 2] if i not in [user_index, monty_opens]][0]
            user_index = remaining_door

        # Check if the user wins
        if doors[user_index] == 1:
            wins += 1

    # Calculate win and lose percentages
    win_percent = wins / number_of_simulations * 100
    lose_percent = 100 - win_percent
    return {'win': win_percent, 'lose': lose_percent}