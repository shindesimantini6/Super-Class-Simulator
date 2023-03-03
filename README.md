# Super-Class-Simulator

This repositiory presents a fantastic supermarket customer simulation analysis based on Monte Carlo Markov Chain simulation analysis.

The simulations add Customers to the simulation based on a Poissonian randomness. These Customers start at entrance and then are moved along the supermarket and through different locations namely., 'fruit', 'drinks', 'dairy', 'spices', 'checkout'. The probabilites of the movement between these sections is calculated based on real data. As the Customer approaches 'checkout' the code removes this Customer. 

./Images/markov.png

# Supermarket Simulation
## TO DO: ADD gif

# Requirements

 - Python 3.8 and above
 - Pandas
 - opencv
 - Faker
 - Random
 - Numpy

# Usage

- Run the final_shopper.py. 
    Along with the Customer simulations a CSV file will be created to store all the Customer simulations with the timestamp, Customer id, Customer name, Customer location and total number of Customers inside the store at a given minute. 
- Run eda_supermarket for exploratory data analysis

# Collaborators

- Victor
- Crista
- Simantini