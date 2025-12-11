#Q2:Count Even and Odd Numbers Take a list of numbers as input (comma-separated).
# Count how many are even and how many are odd.Print results.Example Input:10, 21, 4, 7, 8
def count_even_odd(number_list):
    even_count = 0
    odd_count = 0
    for number in number_list:
        if number % 2 ==0:
            even_count +=1
        else:
            odd_count +=1
    return even_count, odd_count
#input from user
num = input("enter the list of numbers")
num_list = [int(x.strip()) for x in num.split(',')]
even,odd = count_even_odd(num_list)
print("count of even numbers: ",even)
print("count of odd numbers: ",odd)

 