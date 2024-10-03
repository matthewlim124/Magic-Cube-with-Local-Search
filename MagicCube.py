import random
from itertools import combinations
import math

class MagicCube:
    def __init__(self, size=5, target_magic_number=315):
        self.size = size
        self.target_magic_number = target_magic_number
        self.cube = self.inisialisasi_cube()

    def inisialisasi_cube(self):
        #Inisialisasi kubus 

        #Shuffle number dari 1 sampai 125
        numbers = list(range(1, self.size ** 3 + 1)) 
        random.shuffle(numbers)

        #Placeholder untuk kubus, inisialisasi array multidimension dengan nilai 0 
        cube = [[[0 for _ in range(self.size)] for _ in range(self.size)] for _ in range(self.size)]

        #Masukkin numbers ke cube
        index = 0
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    cube[i][j][k] = numbers[index]
                    index += 1

        return cube

    def objective_function(self):
        
        #Objective function yang mengembalikan jumlah valid stack of 5 cubes yang membentuk magic number
        valid_stacks = 0

        # Cek setiap baris kolom tiap dimensi
        for i in range(self.size):
            for j in range(self.size):
                # column stacks
                if self.is_magic([self.cube[k][i][j] for k in range(self.size)]):  
                    valid_stacks += 1
                # row stacks
                if self.is_magic([self.cube[i][k][j] for k in range(self.size)]):
                    valid_stacks += 1
                # depth stacks
                if self.is_magic([self.cube[i][j][k] for k in range(self.size)]):  
                    valid_stacks += 1

        
        #Cek diagonal sisi tiap dimensi
        for i in range(self.size):
            # Diagonal xy-plane
            if self.is_magic([self.cube[i][j][j] for j in range(self.size)]):
                valid_stacks += 1
            if self.is_magic([self.cube[i][j][self.size - 1 - j] for j in range(self.size)]):
                valid_stacks += 1
            # Diagonal  xz-plane
            if self.is_magic([self.cube[j][i][j] for j in range(self.size)]):
                valid_stacks += 1
            if self.is_magic([self.cube[j][i][self.size - 1 - j] for j in range(self.size)]):
                valid_stacks += 1
            # Diagonal on yz-plane
            if self.is_magic([self.cube[j][j][i] for j in range(self.size)]):
                valid_stacks += 1
            if self.is_magic([self.cube[self.size - 1 - j][j][i] for j in range(self.size)]):
                valid_stacks += 1

        # Cek diagonal ruang
        if self.is_magic([self.cube[i][i][i] for i in range(self.size)]):
            valid_stacks += 1
        if self.is_magic([self.cube[i][i][self.size - 1 - i] for i in range(self.size)]):
            valid_stacks += 1
        if self.is_magic([self.cube[i][self.size - 1 - i][i] for i in range(self.size)]):
            valid_stacks += 1
        if self.is_magic([self.cube[self.size - 1 - i][i][i] for i in range(self.size)]):
            valid_stacks += 1


        return valid_stacks

    def is_magic(self, cubes):
        #Cek kalau kubus magic number ato bukan
        return sum(cubes) == self.target_magic_number

    def generate_all_pairs(self):
        #Generate pasangan untuk nanti membentuk neighbor dalam bentuk koordinat 
        positions = [(x, y, z) for x in range(self.size) for y in range(self.size) for z in range(self.size)]
        return list(combinations(positions, 2)) 

    def swap_elements(self, pos1, pos2):
        #Tuker elemen kubus pada posisi pos1 (x1,y1,z2) dan pos2 (x2,y2,z2)
        x1, y1, z1 = pos1
        x2, y2, z2 = pos2
        self.cube[x1][y1][z1], self.cube[x2][y2][z2] = self.cube[x2][y2][z2], self.cube[x1][y1][z1]

    

    def steepest_ascent_hill_climbing(self):
        #Steepest ascent

        
        current_h = self.objective_function()
        print(f"Initial h(n) value: {current_h}")

        #Simpan pasangan unik 
        pairs = self.generate_all_pairs()


        while True:
            best_pos1, best_pos2 = None, None
            best_h = current_h

        
            
            #Looping untuk mengecek h(n) value tiap neighbor
            for pos1, pos2 in pairs:
                
                
                # Swap 2 nomor pada kubus (membentuk 1 neighbor state)
                self.swap_elements(pos1, pos2)

                # Kalkulasi nilai h(n) neighbor
                neighbor_h = self.objective_function()

                # Jika ketemu neighbor yang lebih bagus dari h(n) sekarang, simpan
                if neighbor_h > best_h:
                    best_h = neighbor_h
                    best_pos1,best_pos2 = pos1, pos2
                    
                    
                #Swap kembali 2 nomor pada kubus agar kembali ke kubus awal untuk dicari neighbor lain
                self.swap_elements(pos1, pos2)

            #Jika selesai looping semua 7750 kombinasi, kubus pindah ke n / state yang paling baik
            if best_pos1 != None and best_pos2 != None and best_h > current_h:
                self.swap_elements(best_pos1, best_pos2)
                current_h = best_h
                print(f"Moving to a new neighbor state with higher h(n): {current_h}")
                
            else:
                # Tidak ada neighbor lagi yang lebih besar
                print(f"Reached local maximum with h(n): {current_h}")
                break
        return current_h


    def hill_climbing_with_sideway_steps(self, max_sideways=100):
        
        current_h = self.objective_function()
        print(f"Initial h(n): {current_h}")
        
        sideway_steps = 0
        pairs = self.generate_all_pairs()

        while True:
            best_h = current_h
            best_pos1, best_pos2 = None, None

            #Placeholder untuk menyimpan neighbor dengan h(n) yang sama
            equal_neighbors = []
            
            
            for pos1, pos2 in pairs:
                
                self.swap_elements(pos1, pos2)

                
                neighbor_h = self.objective_function()

                
                self.swap_elements(pos1, pos2)

                
                if neighbor_h > best_h:
                    best_h = neighbor_h
                    best_pos1, best_pos2 = pos1, pos2
                    sideway_steps = 0  

                #Jika ada neighbor dengan h(n) yang sama, simpan di placeholder
                elif neighbor_h == best_h and sideway_steps < max_sideways:
                    equal_neighbors.append((pos1, pos2))
                

            # Jika ada neighbor yang lebih baik, maka pindah ke situ
            if best_pos1 != None and best_pos2 != None:
                self.swap_elements(best_pos1, best_pos2)
                current_h = best_h
                sideway_steps = 0  
                print(f"Moving to new neighbor state with h(n): {current_h}")

            #Jika ada placeholder tidak kosong (ada state dengan h(n) yang sama), maka pilih posisi random dari placeholder 
            #
            elif equal_neighbors and sideway_steps < max_sideways:
                # Ambil neighbor secara acak dari placeholder dan pindah ke sana
                best_pos1, best_pos2 = random.choice(equal_neighbors)
                self.swap_elements(best_pos1, best_pos2)
                sideway_steps += 1 
                print(f"Taking sideway step {sideway_steps} with h(n): {best_h} with position {best_pos1,best_pos2} swapped")
            else:
                # No better neighbors 
                print(f"Reached local maximum with h(n): {current_h}")
                break

            # Terminasi kalo udah max sidestep
            if sideway_steps >= max_sideways:
                print(f"Terminating after {sideway_steps} sideway steps.")
                print(f"Reached local maximum with h(n): {current_h}")
                break
        


    def random_restart_hill_climbing(self, max_restarts=10):
        
        best_overall_h = 0
        best_overall_state = None

        for restart in range(max_restarts):
            print(f"\nRestart {restart + 1}/{max_restarts}...")
            
            

            
            result_h = self.steepest_ascent_hill_climbing()

            if result_h > best_overall_h:
                best_overall_h = result_h
                best_overall_state = [row[:] for row in self.cube]  # Save the best state

            print(f"Restart {restart + 1}: Local max h(n) = {result_h}, Best overall h(n) = {best_overall_h}")
            self.cube = self.inisialisasi_cube()

        print(f"\nBest overall h(n) after {max_restarts} restarts: {best_overall_h}")
        return best_overall_h, best_overall_state
    
    def stochastic_hill_climbing(self, max_iterations=20000):
        
        current_h = self.objective_function()
        print(f"Initial h(n): {current_h}")

        iterations = 0

        while iterations < max_iterations:
            iterations += 1
            # Randomly pick a neighboring state by swapping two elements
            pos1, pos2 = random.choice(self.generate_all_pairs())
            self.swap_elements(pos1, pos2)

            # Calculate h(n) for the neighboring state
            neighbor_h = self.objective_function()

            if neighbor_h > current_h:
                # If the neighbor improves h(n), move to it
                current_h = neighbor_h
                print(f"Improved h(n) to {current_h} after {iterations} iterations")
            else:
                # Undo the swap if no improvement
                self.swap_elements(pos1, pos2)

            # If there's no improvement over time, we terminate early
            if iterations % 100 == 0:
                print(f"Iteration {iterations}: Current h(n) = {current_h}")

        print(f"Final h(n): {current_h} after {iterations} iterations")
        return current_h
    
    def simulated_annealing(self,  cooling_schedule):
        """Perform Simulated Annealing with a customizable cooling schedule."""
        max_iterations=50000
        initial_temp=1000
        min_temp=0
        current_h = self.objective_function()
        current_temp = initial_temp

        print(f"Initial h(n): {current_h}, Initial Temperature: {current_temp}")

        iterations = 0

        while iterations < max_iterations and current_temp > min_temp:
            iterations += 1

            # Apply the cooling schedule (if provided)
            if cooling_schedule:
                current_temp = cooling_schedule(initial_temp, iterations)
            

            # Randomly pick a neighboring state by swapping two elements
            pos1, pos2 = random.choice(self.generate_all_pairs())
            self.swap_elements(pos1, pos2)

            # Calculate h(n) for the neighboring state
            neighbor_h = self.objective_function()

            # Calculate the change in h(n)
            delta_h = neighbor_h - current_h

            if delta_h > 0:
                # If the neighbor improves h(n), move to it
                current_h = neighbor_h
                print(f"Improved h(n) to {current_h} after {iterations} iterations")
            else:
                # If the neighbor is worse, accept it with a probability based on temperature
                acceptance_probability = math.exp(delta_h / current_temp) if current_temp > 0 else 0
                if random.uniform(0, 1) < acceptance_probability:
                    current_h = neighbor_h
                    print(f"Accepted worse state with h(n): {current_h} after {iterations} iterations (due to probability)")

            # Undo the swap if no move is accepted (we don't move to the worse neighbor)
            if delta_h <= 0 and random.uniform(0, 1) >= acceptance_probability:
                self.swap_elements(pos1, pos2)  # Revert swap

            # Output the temperature for monitoring
            if iterations % 100 == 0:
                print(f"Iteration {iterations}: Current h(n) = {current_h}, Temperature = {current_temp}")

        print(f"Final h(n): {current_h} after {iterations} iterations, Final Temperature: {current_temp}")
        return current_h

    # Cooling schedules

    def exponential_decay_schedule(self, initial_temp, t, alpha=0.99):
        """Exponential decay cooling schedule."""
        return initial_temp * (alpha ** t)

    def linear_decay_schedule(self, initial_temp, t, delta_T=1):
        """Linear decay cooling schedule."""
        return max(0, initial_temp - t * delta_T)

    def logarithmic_decay_schedule(self, initial_temp, t, beta=0.001):
        """Logarithmic decay cooling schedule."""
        return initial_temp / (1 + beta * math.log(1 + t))

    def inverse_decay_schedule(self, initial_temp, t, beta=0.001):
        """Inverse decay cooling schedule."""
        return initial_temp / (1 + beta * t)
