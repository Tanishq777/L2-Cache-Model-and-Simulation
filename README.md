# L2-Cache-Model-and-Simulation

In this Project I made a model of CPU and Memory with and without Cache Memory to check the running time and improvements, and did experiment with various cache sizes and associativities to check what trade-offs i am getting in terms of miss-rates in the Computing Model.

# Data Generated :

Miss_Rate, Cache_Size(in kB), Associativity

0.514318, 32, 2

0.513184, 32, 4

0.504395, 32, 8

0.480862, 64, 2

0.472356, 64, 4

0.473207, 64, 8

0.456762, 256, 2

0.456479, 256, 4

0.456195, 256, 8

0.456195, 1024, 2

0.456195, 1024, 4

0.456195, 1024, 8


# Plot: 

![Q2_Graph](https://user-images.githubusercontent.com/52687608/138125543-71e09b6b-eeb3-45e2-a631-7b1caaf8435c.png)

# Observation:

As we increase the size of L2 cache then the number of Cache misses decreases as it has more space (size) than before to store more data and also in the same space (size), if we increase the associativity then also cache miss decrease as more associativity means more number of data can be placed in same modulo (which is used to find address of storing data) then before, So, increasing Associativity of Cache or increasing Size of L2 Cache both decrease 
the cache miss rate.

