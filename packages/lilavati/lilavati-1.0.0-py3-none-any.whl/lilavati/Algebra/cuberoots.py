import math

'''note:leelavati's cube_root method is distinguished for 3 type of numbers
1.the length of number exactly divisible by 3(ex length:3,6,9)
2.the length of number when divisible by 3 leaves remainder as one(ex length:4,7,10)
3.the length of number when divisible by 3 leaves remainder as two(ex length:5,8,11)

2.for the number whose length is 3n+1  the most significant digit(left-most digit) is a single digit subtract the single digit with the
highest number which has a perfect cube root and let that difference be d and the cube root of that number be x and concatenate it in variable called cube_of_num.

3.In next step concatenate the Most Significant digit with the next digit i.e x+next.digit and subtract it with 3*(x^2)*y where y is a variable
which will decide the appropriate digit to be used when 3*(x^2)*y is subtracted from x+next.digit(let that difference be d1) we don't get a negative number(i.e d1 is not negative) and
also y, that we obtain should be such that 3*x*(y^2) should be less than d1 concatenated with next digit

4.After obtaining 3*x*(y^2) concatenate it with the next-digit and subtract that number with y^3  the obtained difference should 
be positive and let it be d2 and now let d=d2,x=y and repeat the process 3 and 4 to obtain the answer.

5.note after every 4th step concatenate y obtained in cube_of_num variable 

6.note for the number whose length is 3n the first 3 digits are considered as MSB and for numbers having length 3n+2 the first 2 numbers are MSB and then same process is follows as step 2 3 and 4'''
def cube_root(num):
    try:
        num=str(num)
        if '.' in num or '-' in num:
            num=float(num)
            if num-math.floor(num)==0:
                if num<0:
                    num=abs(int(num))
                    pos_num=cube_root(num)
                    return -1*pos_num
                else:
                    num=int(num)
                    return cube_root(num)
            else:       
                raise ValueError("Decimal number is not supported")
        
        num=int(num)
        cube_of_num=""
        duplicate=num
        len_of_num=len(str(num))
        if len_of_num%3==1:
            for i in range (len_of_num):
                digit=int(duplicate/math.pow(10,len_of_num-i-1))
                if(i==0):
                    j=1
                    while(j*j*j<=digit):
                        j+=1
                    j-=1
                    duplicate=duplicate-(j*j*j)*math.pow(10,len_of_num-i-1)
                    cube_of_num+=str(j)
                    continue
                
                elif(i%3==1):
                    k=1
                    while(3*(int(cube_of_num)*int(cube_of_num))*k<=digit):
                        k+=1
                        
                    while True:
                        k-=1
                        second_term_number=3*((int(cube_of_num))**2)*k
                        duplicate1=duplicate-second_term_number*math.pow(10,len_of_num-i-1)
                        digit1=int(duplicate1/math.pow(10,len_of_num-i-2))
                        break
                    
                    while((3*(int(cube_of_num))*(k**2))>digit1):
                        k-=1
                        second_term_number=3*((int(cube_of_num))**2)*k
                        duplicate1=duplicate-second_term_number*math.pow(10,len_of_num-i-1)
                        digit1=int(duplicate1/math.pow(10,len_of_num-i-2))
                        
                    duplicate=duplicate1
                    
                elif(i%3==2):
                    third_term_number=3*(int(cube_of_num))*(k**2)
                    duplicate=duplicate-third_term_number*math.pow(10,len_of_num-i-1)
                    
                else:
                    duplicate=duplicate-(k*k*k)*math.pow(10,len_of_num-i-1)
                    cube_of_num+=str(k)
                    continue
        
        elif(len_of_num%3==0):
            for i in range (len_of_num-2):
                digit=int(duplicate/math.pow(10,len_of_num-i-3))
                if(i==0):
                    j=1
                    while(j*j*j<=digit):
                        j+=1
                    j-=1
                    duplicate=duplicate-(j*j*j)*math.pow(10,len_of_num-i-3)
                    cube_of_num+=str(j)
                    continue
                
                elif(i%3==1):
                    k=1
                    while(3*(int(cube_of_num)*int(cube_of_num))*k<=digit):
                        k+=1
                        
                    while True:
                        k-=1
                        second_term_number=3*((int(cube_of_num))**2)*k
                        duplicate1=duplicate-second_term_number*math.pow(10,len_of_num-i-3)
                        digit1=int(duplicate1/math.pow(10,len_of_num-i-4))
                        break
                    
                    while((3*(int(cube_of_num))*(k**2))>digit1):
                        k-=1
                        second_term_number=3*((int(cube_of_num))**2)*k
                        duplicate1=duplicate-second_term_number*math.pow(10,len_of_num-i-3)
                        digit1=int(duplicate1/math.pow(10,len_of_num-i-4))
                        
                    duplicate=duplicate1
                    
                elif(i%3==2):
                    third_term_number=3*(int(cube_of_num))*(k**2)
                    duplicate=duplicate-third_term_number*math.pow(10,len_of_num-i-3)
                    
                else:
                    duplicate=duplicate-(k*k*k)*math.pow(10,len_of_num-i-3)
                    cube_of_num+=str(k)
                    continue
                
        else:
            for i in range (len_of_num-1):
                digit=int(duplicate/math.pow(10,len_of_num-i-2))
                if(i==0):
                    j=1
                    while(j*j*j<=digit):
                        j+=1
                    j-=1
                    duplicate=duplicate-(j*j*j)*math.pow(10,len_of_num-i-2)
                    cube_of_num+=str(j)
                    continue
                
                elif(i%3==1):
                    k=1
                    while(3*(int(cube_of_num)*int(cube_of_num))*k<=digit):
                        k+=1
                        
                    while True:
                        k-=1
                        second_term_number=3*((int(cube_of_num))**2)*k
                        duplicate1=duplicate-second_term_number*math.pow(10,len_of_num-i-2)
                        digit1=int(duplicate1/math.pow(10,len_of_num-i-3))
                        break
                    
                    while((3*(int(cube_of_num))*(k**2))>digit1):
                        k-=1
                        second_term_number=3*((int(cube_of_num))**2)*k
                        duplicate1=duplicate-second_term_number*math.pow(10,len_of_num-i-2)
                        digit1=int(duplicate1/math.pow(10,len_of_num-i-3))
                        
                    duplicate=duplicate1
                    
                elif(i%3==2):
                    third_term_number=3*(int(cube_of_num))*(k**2)
                    duplicate=duplicate-third_term_number*math.pow(10,len_of_num-i-2)
                    
                else:
                    duplicate=duplicate-(k*k*k)*math.pow(10,len_of_num-i-2)
                    cube_of_num+=str(k)
                    continue
                
        return float(cube_of_num)
    
    except ValueError as e:
        return f"Error: {e}"



                
                    