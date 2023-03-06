import numpy as np
import tqdm

#hyperparams
lr = 1
population = 80000
darwin = 0.5
epochs = 1
num_towers = 10
#

def rand_army_plan():
    rand = np.random.rand(num_towers)
    rand_army_plan = rand * 100 / sum(rand)
    return rand_army_plan

def mutate(one_dim_list):
    norm_mutation = (np.random.rand(num_towers)-0.5)*lr*2
    mutated_but_not_100 = one_dim_list + norm_mutation
    mutated_but_not_100[mutated_but_not_100 <= 0] = 0
    mutated_army_plan = mutated_but_not_100 * 100 / np.sum(mutated_but_not_100)
    return mutated_army_plan

def is_valid_plan(one_dim_list) -> bool:
    if np.sum(one_dim_list) == 100 and  len(one_dim_list == num_towers):
        return True
    return False

def longest_run(one_dim_list) -> int:
    count = 0
    longest_run = 0
    for item in one_dim_list:
        if item > 0:
            count += 1
        else:
            if count > longest_run:
                longest_run = count
    return longest_run

def game_points(army_plan_A, army_plan_B):
    assert(len(army_plan_A) == len(army_plan_B) == num_towers)
    # print(army_plan_A)
    # print(" vs ")
    # print(army_plan_B)
    #basic wins
    A_wins = np.array([(army_plan_A[i] > army_plan_B[i]) * (i+1) for i in range(len(army_plan_A))])
    # B_wins = np.array([(army_plan_A[i] < army_plan_B[i]) * (i+1) for i in range(len(army_plan_B))])
    # print(f"A: {A_wins}")
    # print(f"B: {B_wins}")
    #streaks
    A_streaks_points = longest_run(A_wins) * 2
    # B_streaks_points = longest_run(B_wins) * 2
    # print(f"A: {np.sum(A_wins)} + {A_streaks_points}")
    # print(f"B: {np.sum(B_wins)} + {B_streaks_points}")
    #points all together
    A_points = np.sum(A_wins) + A_streaks_points
    # B_points = np.sum(B_wins) + B_streaks_points
    return A_points #, B_points

def main():
    #generate random generation
    current_gen = np.array([rand_army_plan() for i in range(population)])
    #fill out round robin
    for epoch in range(epochs):
        # np.append(current_gen, [0,0,0,10,0,0,21,22,23,24])
        # print(f"Epoch: {epoch}")
        score_list = np.zeros(len(current_gen))
        index = 0
        for army_plan_A in tqdm.tqdm(current_gen): #seems ripe for optimisation
            this_score = 0
            for army_plan_B in current_gen: #including against itself ;( will try to fix later
                this_score += game_points(army_plan_A, army_plan_B)

            score_list[index] = this_score #sadly np array not hashable
            index += 1

        
        #print(score_list)
        #conserve the most successful
        sorted_indices = np.argsort(score_list)
        leaderboard = current_gen[sorted_indices]

        

        survivors = leaderboard[int(-1*darwin*len(current_gen)):-1]
        for survivor in survivors:
            is_valid_plan(survivor)

        # print(score_list[sorted_indices])
        # print(survivors)
        # print(score_list[sorted_indices]/len(survivors))

        if epoch == epochs:
            break

        #generate new generation

        new_gen = []
        repop_ratio = population/len(survivors) #to aim to population, no need to hit it
        for lucky_survivor in survivors:
            for i in range(int(repop_ratio)):
                new_gen.append(mutate(lucky_survivor))
        

        current_gen = np.array(new_gen)

    print("Well done survivors")

    print(f"Optimal strategy? {survivors[-1]}")
    print(f"Sanity sum {np.sum(survivors[-1])}")

    current_gen.tofile("bestgen.csv",sep=",")

    new_gen = np.fromfile("bestgen.csv",sep=",").reshape(-1,10)
    assert np.all(np.equal(current_gen, new_gen))

    return 0

if __name__ == "__main__":
    main()