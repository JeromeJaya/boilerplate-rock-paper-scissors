import random

def player(prev_play, opponent_history=[], my_history=[], fallback_count=[0]):
    if prev_play:
        opponent_history.append(prev_play)
    if hasattr(player, "last_move"):
        my_history.append(player.last_move)
    else:
        my_history.append(random.choice(['R', 'P', 'S']))

    def counter_move(move):
        return {'R': 'P', 'P': 'S', 'S': 'R'}[move]

    def freq_predict(history):
        freq = {'R': 0, 'P': 0, 'S': 0}
        weights = [1.5 ** i for i in range(len(history))]  # weight recent moves more
        for i, move in enumerate(history):
            freq[move] += weights[-(i+1)]
        return max(freq, key=freq.get)

    def pattern_predict(history):
        for length in range(5, 1, -1):
            if len(history) >= length:
                recent_pattern = "".join(history[-length:])
                counts = {'R': 0, 'P': 0, 'S': 0}
                for i in range(len(history) - length):
                    if "".join(history[i:i+length]) == recent_pattern:
                        counts[history[i+length]] += 1
                total = sum(counts.values())
                if total > 0:
                    max_count = max(counts.values())
                    confidence = max_count / total
                    if confidence >= 0.35:
                        return max(counts, key=counts.get)
        return None

    def detect_cycle(history):
        n = len(history)
        for cycle_length in range(2, 5):
            if n >= cycle_length * 2:
                cycle = history[-cycle_length:]
                if all(history[i:i+cycle_length] == cycle for i in range(n - cycle_length * 2, n - cycle_length, cycle_length)):
                    return cycle[0]
        return None

    # Strategy switching: fallback phase to add randomness if stuck
    if fallback_count[0] > 0:
        fallback_count -= 1
        move = random.choice(['R', 'P', 'S'])
        player.last_move = move
        return move

    predicted = detect_cycle(opponent_history)
    if predicted is None:
        predicted = pattern_predict(opponent_history)
    if predicted is None:
        predicted = freq_predict(opponent_history)

    confidence_check = True
    # Optionally lower confidence threshold dynamically or fallback
    # If confidence low for 3 rounds, enter fallback phase
    # Implement this logic if needed (not shown here for brevity)

    move = counter_move(predicted)
    player.last_move = move
    return move
#hi