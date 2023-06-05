# RRT



This is an implementation of Rapidly-Exploring Random Tree Algorithm (RRT) on Python 3. The code generates a two dimensional statespace and adds random obstacle.



The repository includes:
* Source code based on RRT Algorithm.
* Example of testing the code 



# Steps to test the code



## Requirements
Python 3.4 and other common packages listed in `requirements.txt`.


## Installation
1. Clone this repository
2. Install dependencies
   ```bash
   pip3 install -r requirements.txt
   ```
3. Run RRT.py from the repository root directory 
   ```bash
   cd RRT
   python RRT.py
   ```
4. Input of starting coordinate values, goal coordinate values and obsatcle coordinate values  must be given in the start, goal, manual_obstacle tuples respectively under the main method
5. The start point, goal point and manual_obstacle will be in blue, green and pink colour respectively 
6. In order to test with multiple obstacles, random obstacles in rectangle and elliptical shapes are added. They are colored grey and orange, respectively.
7. If the path is available after multiple explorations, the path corresponding to the start and goal will be marked in red color. The coordinates of the path and the cost will be printed in the output.


## Sample Output 
### Sample 1
![alt text](https://github.com/kishoreparanthaman/RRT/blob/main/assest/RRT1.gif)
### Sample 2
![alt text](https://github.com/kishoreparanthaman/RRT/blob/main/assest/RRT2.gif)
### Sample 3
![alt text](https://github.com/kishoreparanthaman/RRT/blob/main/assest/RRT3.gif)
### Sample 4
![alt text](https://github.com/kishoreparanthaman/RRT/blob/main/assest/RRT4.gif)
    
