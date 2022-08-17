# Sum of N natural numbers
import timeit

debug = False

if debug:
    # Start Timer here
    start = timeit.default_timer()

    num = 100000
    sum = 0
    # use while loop to iterate un till zero
    while (num > 0):
      sum = sum + num
      num -= 1
    print("The sum is", sum)

    # End timer here
    stop = timeit.default_timer()

    print("Time taken to execute this program: ")
    print(stop - start)

else:

    # Start Timer here
    start = timeit.default_timer()

    num = 100000

    # use while loop to iterate un till zero

    sum = (num*(num+1))/2

    print("The sum is", sum)

    # End timer here
    stop = timeit.default_timer()

    print("Time taken to execute this program: ")
    print(stop - start)
