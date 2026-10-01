import numpy as np

def crr_price(S0, K, T, r, sigma, N, option_type="call", american=False):
    dt = T/N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1/u
    p = (np.exp(r*dt) - d) / (u - d)

    stock_tree = np.zeros((N + 1, N + 1))

    for i in range(N + 1):
        for j in range(i + 1):
            stock_price = S0 * (u ** j) * (d ** (i - j))
            stock_tree[j, i] = stock_price

    option_tree = np.zeros((N + 1, N + 1))

    if option_type == "call":
        for j in range(N + 1):
            option_tree[j, N] = max(stock_tree[j, N] - K, 0)
    
    elif option_type == "put":
        for j in range(N+1):
            option_tree[j,N]=max(K-stock_tree[j,N], 0)
    
    else:
        raise ValueError("option_type must be either a 'call' or 'put'" )


    

    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            C_down = option_tree[j, i + 1]
            C_up = option_tree[j + 1, i + 1]

            continuation_value = np.exp(-r * dt) * (p * C_up + (1 - p) * C_down)

            if option_type=="call":
                exercise_value = max(stock_tree[j, i] - K, 0)
            elif option_type=="put":
                exercise_value = max(K-stock_tree[j,i], 0)

            if american:
                option_tree[j, i] = max(exercise_value, continuation_value)
            else:
                option_tree[j, i] = continuation_value

    return option_tree[0,0]