"""
/*********************************************************************
* Copyright (c) {December 2023} {Samares-Engineering} authors:[Mirna Ojeda, Sebastien Dube,Jean-Marie Gauthier, Yash Kethan]
*
* This program and the accompanying materials are made
* available under the terms of the Eclipse Public License 2.0
* which is available at https://www.eclipse.org/legal/epl-2.0/
*
* SPDX-License-Identifier: EPL-2.0
**********************************************************************/
"""
class Swap_random:
    @staticmethod
    def rand(cm,size):
        args=random.sample(range(size), size)  #generates random list from 0-size
        args1=args
        argCount=len(args)
        new = cm
        empty=np.empty([argCount,argCount],dtype=int)
        for n in range(argCount):
            u=args1[n]
            for x in range(argCount):
                v=args1[x]
                empty[n,x]=new[u,v]   #generates new matrix by interchanging rows and columns wrt args arrangement
        return empty,args
    
class Interactions_bw_modules:
    @staticmethod
    def interaction(a):
    #   Creates all interactions between modules
        mods=a # number of modules
        add=np.zeros(mods)                       # variable to hold numbers from 0 to mods-1
        for i in range(mods):
            add[i]=i
        #comb=int(np.sum(add))
        result=list(itertools.product(add,add))  # Make combinations of 2 elements from add
        result=np.asarray(result)
        lent=len(result)
        j=[]                                     # Variable to hold all unwanted positions in add
        for i in range(lent):
            if result[i,0]>=result[i,1]:
                j.append(i)
        interactions=np.delete(result,j,0)       # delete row j from result
        interactions=interactions.astype(int)
        lent=len(interactions)
        return interactions,lent
class Coupling_Generalised:
    @staticmethod
    def coup(cm,mods,M):

        interactions, lent = Interactions_bw_modules.interaction(mods)  # Gives the interactions, for ex if no. of modules =3 M0M1,M0M2,M1M2
        DoM=np.zeros(mods)
        DiM=np.zeros(mods)
        r = np.zeros((mods,mods))
        w= np.zeros((mods,mods))
        para = np.empty([mods * 4])  # Number of coupling parameters 4 x no. of modules
        i=1
        l=0
        for j in range(lent):
            for k in M[interactions[j,0]]:
                for l in M[interactions[j,1]]:
                    if cm[k,l]==1:
                        DoM[interactions[j,0]]=DoM[interactions[j,0]]+1
                        DiM[interactions[j,1]]=DiM[interactions[j,1]]+1
                        w[interactions[j,0],interactions[j,1]]=1
                        r[interactions[j,1],interactions[j,0]]=1
                    else:
                        pass
                    if cm[l,k]==1:
                        DiM[interactions[j,0]]=DiM[interactions[j,0]]+1
                        DoM[interactions[j,1]]=DoM[interactions[j,1]]+1
                        r[interactions[j,0],interactions[j,1]]=1
                        w[interactions[j,1],interactions[j,0]]=1
                    else:
                        pass

        r=np.sum(r,1)
        w=np.sum(w,1)

        return DoM,DiM,w,r
    
    @staticmethod
    # Calculates the coupling coefficient
    def calc(a,mods):
        a=np.asarray(a)
        c=np.zeros(mods)
        for i in range(mods):
            if (a[0,i]==0 and a[1,i]==0 and a[2,i]==0 and a[3,i]==0):
                c[i]=0
            else:
                c[i]=1-(1/(a[0,i]+a[1,i]+a[2,i]+a[3,i]))
        c=np.sum(c)
        #print(c)
        return c

class GeneticAlgorithm:
    @staticmethod
    def mods_shuffling(siz):
        uniques = siz
        rows_unique = 1 # len (uniques )
        columns_uniques = len(siz)
        void = np.zeros(columns_uniques, dtype=int)

        for j in range(columns_uniques):
            if j == 0:
                void[j] = siz[j]
            else:
                void[j] = void[j - 1] + siz[j]

        M = []
        new = np.zeros( columns_uniques , dtype=object )
        count = 0
        for j in range(columns_uniques):
            if j == 0:
                M.append([*range(void[j])])
            else:
                M.append([*range(void[j - 1], void[j])])
        new= M
        new= tuple(map(tuple,new))
        return tuple(M)

    @staticmethod
    # Swaps the N2 according to new order
    def swap(cm, args):
        args = np.asarray(args, dtype=int)
        argCount = len(args)
        new = cm
        empty = np.empty([argCount, argCount], dtype=int)
        for n in range(argCount):
            u = args[n]
            for x in range(argCount):
                v = args[x]
                empty[n, x] = new[u, v]
        return empty
    @staticmethod
    # Creates initial population
    def init_population(mods, nfuncs, pop_size, fix_func_id, fix_module,not_fixed_components): 
        S= np.array(not_fixed_components)
        U = list(map(str, S))  # Convert to string for choices
        initial_population = np.zeros((pop_size, nfuncs), dtype=int)
        for i in range(pop_size):
            while True:
                candidate = np.array(random.choices(U, k=nfuncs))
                candidate[fix_func_id] = fix_module
                
                unique_modules = np.unique(candidate)
                
                # Check if all modules are represented
                if len(unique_modules) == mods:
                    initial_population[i] = candidate
                    break
       
        return initial_population


    @staticmethod
    # Returns the order of functions from a chromosome
    def order(Gene, mods):
        M = []
        N = []
        for i in range(1, mods + 1):  # Finds the correct order of the N Matrix
            M.append(np.where(Gene == i)[0])
        for j in list(M):
            if len(j) > 1:
                for i in range(len(j)):
                    N.append(j[i])
            else:
                N.append(j[0])
        #print('\n Order \n',N)
        return N  # Returns the order of the Chromosome [0,5,6,3,2,1,4]
    
    @staticmethod
    #  Returns module configuration
    def module_config(Gene, mods):
        R = []
        for i in range(mods):
            s = np.where(Gene == i + 1)
            if (True):
                R.append(len(s[0]))

        return R
    
    @staticmethod
    # Fitness function for GA
    def fitness_coupling(pop_size, mods, nfuncs, population, n2_data):
        Order = np.zeros((pop_size, nfuncs))
        mods_temp = np.zeros((pop_size, mods))
        mods_config = np.zeros((pop_size, mods), dtype=object)
        coupling_parameters = np.zeros((pop_size), dtype=object)
        coupling_coefficient = np.zeros((pop_size), dtype=object)
        Total_flows=np.zeros((pop_size), dtype=object)
        for i in range(pop_size):
            Order[i] = GeneticAlgorithm.order(population[i], mods)
            mods_temp[i] = GeneticAlgorithm.module_config(population[i], mods)
            mods_config[i] = GeneticAlgorithm.mods_shuffling(mods_temp[i])
            swapped_data_n2 = GeneticAlgorithm.swap(n2_data, Order[i])
            coupling_parameters[i] = Coupling_Generalised.coup(swapped_data_n2, mods, mods_config[i])
            coupling_coefficient[i] = round(Coupling_Generalised.calc(coupling_parameters[i], mods), 3)

            Total_flows[i]=np.sum(coupling_parameters[i][0])
        #print(coupling_coefficient) 
        return coupling_coefficient,Total_flows
    
    @staticmethod
    # Selection for GA
    def select_mating_pool(population, coupling_values_list, survivor_percentage):
        num_parents = int((survivor_percentage / 100) * population.shape[0])

        if num_parents == 0:
            num_parents = 1

        survivor_list = np.zeros((num_parents, population.shape[1]))

        for parent_num in range(num_parents):
            max_fitness_idx = np.where(coupling_values_list == np.min(coupling_values_list))
            # print(max_fitness_idx)
            max_fitness_idx = max_fitness_idx[0][0]
            # print(max_fitness_idx)
            survivor_list[parent_num, :] = population[max_fitness_idx, :]

            coupling_values_list[max_fitness_idx] = 99999999999

        return survivor_list
    @staticmethod
    # Crossover for GA
    def crossover(survivors_list, parent_percentage):
        parent_size = int((parent_percentage / 100) * survivors_list.shape[0])
        # print("Number of parents", parent_size)
        # Initialisation of a new child
        new_child = np.empty((parent_size, survivors_list.shape[1]))

        # The point at which crossover takes place between two parents. Usually, it is at the center.
        cross_index = np.arange(0, survivors_list.shape[1])

        for k in range(parent_size):
            crossover_point = random.choice(cross_index)
            list_of_indices = np.arange(0, survivors_list.shape[0])

            # Index of first parent to mate
            parent1_idx = random.choice(list_of_indices)
            # Remove index to avoid duplicate parent
            list_of_indices = list_of_indices[list_of_indices != parent1_idx]
            # Index of second parent to mate
            parent2_idx = random.choice(list_of_indices)

            # The new offspring will have its first half of its genes taken from the first parent.
            new_child[k, 0:crossover_point] = survivors_list[parent1_idx, 0:crossover_point]
            # The new offspring will have its second half of its genes taken from the second parent.
            new_child[k, crossover_point:] = survivors_list[parent2_idx, crossover_point:]
        # offspring[:,3]=1
        return new_child
    
    @staticmethod
    # Mutation for GA
    def mutation(new_child_people, nb_modules, not_fixed_functions_indices, population_mutation_percentage,
                     gene_mutation_percentage):
            module_nos = np.array(nb_modules)

            number_of_people_to_mutate = int((population_mutation_percentage / 100) * new_child_people.shape[0])
            number_of_gene_to_mutate = int((gene_mutation_percentage / 100) * new_child_people.shape[1])
            # Choose randomly some people index to mutate
            child_indices_list = np.arange(0, new_child_people.shape[0])
            index_list_of_child_to_mutate = []
            for i in range(number_of_people_to_mutate):
                idx_child = random.choice(child_indices_list)
                index_list_of_child_to_mutate.append(idx_child)
                child_indices_list = child_indices_list[child_indices_list != idx_child]
                
            # Choose randomly some gene index to mutate except the gene that are fixed
            index_list_of_gene_to_mutate = []
            for i in range(number_of_gene_to_mutate):
                # Check if not_fixed_functions_indices is not empty
                if not_fixed_functions_indices.size > 0:
                    idx_gene = random.choice(not_fixed_functions_indices)
                    not_fixed_functions_indices = not_fixed_functions_indices[not_fixed_functions_indices != idx_gene]
                    index_list_of_gene_to_mutate.append(idx_gene)
                else:
                    print("Warning: not_fixed_functions_indices is empty. Breaking the loop.")
                    break
            
            # Perform mutation on the chosen child
            for idx in range(number_of_people_to_mutate):
                child_to_mutate = new_child_people[index_list_of_child_to_mutate[idx]]
                for j in range(number_of_gene_to_mutate):
                    random_module_value = random.choice(module_nos)
                    child_to_mutate[index_list_of_gene_to_mutate[j]] = random_module_value
    
                new_child_people[index_list_of_child_to_mutate[idx]] = child_to_mutate
            return new_child_people

    @staticmethod
    # A check that is performed at the end of every iteration to delete recurring chromosomes
    def check(parents, offspring, mods):
        index_parents = []
        index_offspring = []
        parents_size = parents.shape[0]
        offspring_size = offspring.shape[0]
        module_nos = np.arange(1, mods + 1)
        #module_nos =[1,2,3,4,5]
        for i in range(parents_size):
            for j in list(module_nos):
                check = np.sum((parents[i] == j))
                if (check == 0):  # or parents[i,(3,8)]!=1,2):
                    index_parents.append(i)
                    break
        parents = np.delete(parents, index_parents, 0)
        # print(index_parents)
        for i in range(offspring_size):
            for j in list(module_nos):
                check = np.sum((offspring[i] == j))
                if (check == 0):  # or offspring[i,(3,8)]!=1,2):
                    index_offspring.append(i)
                    break
        offspring = np.delete(offspring, index_offspring, 0)
        # print(index_offspring)
        return parents, offspring

    @staticmethod
    # The end to end timing latency function
    def end_to_end(survivors):
        y = [0, 0, 0, 0]
        z = 0
        w = [0, 0, 0, 0]
        for o in range(survivors.shape[0]):
            index = [3,13,15,8,10]   # The function numbers encountered by end to end flows
            min = [0, 0, 0,0,0]  # Minimum time required by each function to execute
            max = [100,100,100,100,100]  # Maximum time required by each function to execute
            trans = [0, 10]         # Transition time between modules
            ft = []
            x = len(index)
            for u in list(index):
                ft.append(survivors[o,u-1]) # Module number array, representing module numbers of each index position allotted by GA


            for i in range(x):  # x is inex length of source function to sink function , example 1,2,4,5,8
                l = ft[i]
                if (i != (x - 1)):
                    t = ft[i + 1]
                y[o] = y[o] + z + min[i]   # Returns minimum end to end time
                w[o] = w[o] + z + max[i]   # Returns maximum end to end time
                if (l != t):
                    z = trans[1]
                else:
                    z = trans[0]
        return y,w,index
