n = int(input())
ans = n
while n > 9:
  n = n // 10 + n % 10
ans = ans * 10 + (10 - n)
print(ans)