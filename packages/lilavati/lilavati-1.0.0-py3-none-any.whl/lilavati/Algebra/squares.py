import math

def square(num):
    try:
        # Convert the input to a string
        num = str(num)

        # Check if the input is a decimal number
        
        if '.' in num or '-' in num:
            num=math.fabs(float(num))
            if num-math.floor(num)!=0:
                count=0
                while num%1 !=0:
                    num*=10
                    count+=1
                number_square=square(num);
                return number_square*math.pow(10,-(count*2))
            
            else:
                number=int(num)
                return square(number)
            
        
        num_square = 0
        length_num = len(num) 
        num_array = [None] * length_num 

        for i in range(length_num):
            # Multiply each digit with its place value and store in an array
            
            num_array[i] = (int(num[i])) * math.pow(10, length_num - i - 1)

        ''' once all the digits multiplied with it's placevalue is stored in an array according to leelavati method following
            steps take place
        1.squaring of each element present in the array and adding them to variable called num_square
        2.addition of 2*last_digit*next_digit to num_square'''
        
        for i in num_array:
            num_square += i ** 2
        
        for i in range(len(num_array) - 1):
            for j in range(i + 1, len(num_array), 1):
                num_square += 2 * num_array[i] * num_array[j]

        return num_square
    
    except ValueError as e:
        return f"Error: {e}"

