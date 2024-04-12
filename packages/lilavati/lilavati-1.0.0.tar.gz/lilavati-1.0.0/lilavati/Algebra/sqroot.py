import math

'''note:leelavati's method is distinguished for two type for numbers one which has odd number of digits and
other for even number of digits leelavati's method involves 3 steps which is used repeatedly until the answer is not found
1.find the length of the number and classify it as number with odd number of digits or even number of digits.

2.for the number whose length is odd number the most significant digit is a single digit subtract the single digit with
highest number which has a perfect square root and let that difference be d and the square root of that number be x and concatenate it in variable root_num_double.

3.In next step take concatenate the MSB digit with the next digit i.e x+next.digit and subtract it with 2*x*y where y is a variable
which will decide the appropriate digit to be used when 2*x*y is subtracted from x+next.digit(let that difference be d1) we don't get a negative number
also y that we obtain should be such that (y*y) should be less than d1 concatenated wit next digit

4.let d=d1 and x=y repeat process 3 and 4 to obtain the answer.

5.After every fourth step concatenate y in root_num_double.

6.note for the number whose length is even number the first 2 digits are considered as MSB and the same process is follows as step 2 3 and 4'''





def square_root(num):
    try:
        num=str(num)
        if '.' in num or '-' in num:
            num=float(num)
            if num-math.fabs(math.floor(num))==0:
                num=int(num)
                return square_root(num)
            elif num<0:
                raise ValueError("negative number not supported")
            
        
        num=int(num)
        duplicate=num
        length_num=len(str(num))
        root_num_double=""  #to store the final answer in string form
        
        
        if length_num%2==1:
            for i in range (length_num):
                
                '''distinguished in 3 steps 
                    1.to obtain the MSB
                    2.follow the process of subtraction using 2*x*y and the other digits
                    3.follow the process of subtraction using y*y and the other digits'''
                digit=int(duplicate/math.pow(10,length_num-i-1))
                #to obtain MSB and perform suitable operations on it
                
                if(i==0):
                    j=1
                    while (j*j<=digit):
                        j+=1
                    
                    j-=1
                    duplicate=duplicate-(j*j)*math.pow(10,length_num-i-1)
                    root_num_double+=str(j)
                    continue
                
                #follow step 2
                elif(i%2==1):
                    k=1
                    while(2*(int(root_num_double))*k<=digit):
                        if(digit-2*(int(root_num_double))*k>=0):
                            k+=1
                            continue
                    while True:
                        k-=1
                        Even_number=2*(int(root_num_double))*k
                        duplicate1=duplicate-Even_number*math.pow(10,length_num-i-1)
                        digit1=int(duplicate1/math.pow(10,length_num-i-2))
                        break
                        
                    while((k*k)>digit1):
                        k-=1
                        Even_number=2*(int(root_num_double))*k
                        duplicate1=duplicate-Even_number*math.pow(10,length_num-i-1)
                        digit1=int(duplicate1/math.pow(10,length_num-i-2))
                        
                    duplicate=duplicate1
                
                #follow step 3
                else:
                    duplicate=duplicate-(k*k)*math.pow(10,length_num-i-1)
                    root_num_double+=str(k)
                    continue
        
        #algo for the number whose length in even
        else:
            for i in range (length_num-1):
                digit=int(duplicate/math.pow(10,length_num-i-2))
                #print(digit)
                if(i==0):
                    digit1=int(duplicate/math.pow(10,length_num-i-2))
                    j=1
                    while (j*j<=digit1):
                        j+=1
                    
                    j-=1
                    duplicate=duplicate-(j*j)*math.pow(10,length_num-i-2)
                    #print(duplicate)
                    root_num_double+=str(j)
                    continue
                
                
                elif(i%2==1):
                    k=1
                    while(2*(int(root_num_double))*k<=digit):
                        if(digit-2*(int(root_num_double))*k>=0):
                            k+=1
                            continue
                    while True:
                        k-=1
                        Even_number=2*(int(root_num_double))*k
                        duplicate1=duplicate-Even_number*math.pow(10,length_num-i-2)
                        digit1=int(duplicate1/math.pow(10,length_num-i-3))
                        #print(k)
                        break
                        
                    while((k*k)>digit1):
                        k-=1
                        Even_number=2*(int(root_num_double))*k
                        duplicate1=duplicate-Even_number*math.pow(10,length_num-i-2)
                        digit1=int(duplicate1/math.pow(10,length_num-i-3))
                        
                    duplicate=duplicate1
                
                else:
                    #print(k)
                    duplicate=duplicate-(k*k)*math.pow(10,length_num-i-2)
                    root_num_double+=str(k)
                    continue
        
                
        return float(root_num_double)

    except ValueError as e:
        return f"Error: {e}"
    


'''note: algorithm only for int type number not for any data type'''   
