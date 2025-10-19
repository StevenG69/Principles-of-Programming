def apply_pattern_to_list(L, pattern='+-', from_start=True):
    if len(L) < 2:
        return {}

    removed = {}
    pattern_len = len(pattern)
    pattern_index = 0

    if from_start:  # Forward traversal
        filtered = [L[0]]  # Keep the first element
        for i in range(1, len(L)):
            current, next_value = filtered[-1], L[i]
            p = pattern[pattern_index]

            # Check if the pattern is followed
            if (p == '+' and current < next_value) or (p == '-' and current > next_value):
                pattern_index = (pattern_index + 1) % pattern_len
                filtered.append(next_value)
            else:
                removed[i] = next_value

        L[:] = filtered[:]  # Modify the original list in place

    else:  # Backward traversal
        filtered = [L[-1]]  # Start with the last element
        pattern = pattern[::-1]
        for i in range(len(L) - 2, -1, -1):
            current, next_value = filtered[-1], L[i]
            p = pattern[pattern_index]

            # Check if the pattern is followed
            if (p == '+' and next_value > current) or (p == '-' and next_value < current):
                pattern_index = (pattern_index + 1) % pattern_len
                filtered.append(next_value)
            else:
                removed[-(len(L) - i)] = next_value

        L[:] = filtered[::-1]  # Reverse to restore original order

    return removed

L = []
result = apply_pattern_to_list(L)
print("Dict:", result)
print("Updated list:", L)

L = [1]
result = apply_pattern_to_list(L)
print("Dict:", result)
print("Updated list:", L)

L = [1, 2, 1, 2, 1, 2, 3]
result = apply_pattern_to_list(L)
print("Dict:", result)
print("Updated list:", L)

L = [1, 2, 1, 2, 1, 2, 3]
result = apply_pattern_to_list(L, from_start=False)
print("Dict:", result)
print("Updated list:", L)

L = [1, 3, 2, 0, 0, -2, -2, 1, 5, -4]
result = apply_pattern_to_list(L, '++-')
print("Dict:", result)
print("Updated list:", L)

L = [-11, -2, -3, 11, -11, -12, 12, -7, 14, -5, 15, -1, 11, -10, 11]
result = apply_pattern_to_list(L, '---+')
print("Dict:", result)
print("Updated list:", L)

L = [-11, -2, -3, 11, -11, -12, 12, -7, 14, -5, 15, -1, 11, -10, 11]
result = apply_pattern_to_list(L, '---+', False)
print("Dict:", result)
print("Updated list:", L)

L = [0, -4, 4, 4, 2, -2, 1, 3, -3, -4, -4, -2, -3, 0, 1, 2, -4, 3, -1, 1]
result = apply_pattern_to_list(L, '-+')
print("Dict:", result)
print("Updated list:", L)

L = [0, -4, 4, 4, 2, -2, 1, 3, -3, -4, -4, -2, -3, 0, 1, 2, -4, 3, -1, 1]
result = apply_pattern_to_list(L, '-+', False)
print("Dict:", result)
print("Updated list:", L)
