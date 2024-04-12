'''leelavati follows a particular method to find a cube of a number it involves 4 steps
    1.initially separate the number into 2 parts one is the least significant digit part and other digits as one number
    ex:if we are finding cube for number 125 separate it as 12 and 5
    2.here comes 4 steps to find the cube of the number(example to find cube for 125)
        2.1.cube the number separated from LSG i.e 12 and multiply with 1000 let it be x=1728*1000 
        2.2.now find 3*(x*x)*LSB*100--> 3*(12*12)*5*100
        2.3 find 3*(x)*(LSB*LSB)*10-->3*(12)*(5*5)*10
        2.4 find cube of LSB
    3.now add all the numbers obtained in 2.1,2.2,2.3,2.4 hence you will get the required number '''

import math
def cube(num):
    try:
        num=str(num)
        if '.' in num or '-' in num:
            num=float(num)
            if num-math.floor(num)!=0:
                count=0
                while num%1 !=0:
                    num*=10
                    count+=1
                if num<0:
                    pos_num=abs(num)
                    number_cube=cube(pos_num)
                    return -1*number_cube*math.pow(10,-(count*3))
                number_square=cube(num);
                return number_square*math.pow(10,-(count*3))
            
            else:
                if num<0:
                    num=abs(int(num))
                    pos_num = cube(num)
                    return -1*pos_num
                else:
                    num=int(num)
                    return cube(num)
            
        
        num=int(num)
        num_length = len(str(num))
        cube_num = 0
        
        # Check if the input is a single digit
        if num_length == 1:
            return num * num * num
        else:
            arr = [None] * 2
            arr[0] = int(num / 10)
            arr[1] = num % 10
            for i in range(4):
                if i == 0:
                    cube_num += cube(arr[0]) * 1000
                elif i == 1:
                    cube_num += 3 * (arr[0] ** 2) * arr[1] * 100
                elif i == 2:
                    cube_num += 3 * (arr[0]) * (arr[1] ** 2) * 10
                else:
                    cube_num += cube(arr[1])
        if num<0:
            return -1*cube_num
        else:
            return cube_num
    
    except ValueError as e:
        return f"Error: {e}"

'''note:algorithm only for int type number not for any other data type'''

