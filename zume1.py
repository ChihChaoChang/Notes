a = "ABC"
b = "1234"
M = len(a)
N = len(b)
length = min(M,N)
ans = ""
if M ==0:
    print (b)
if N == 0:
    print (a)
i = 0
for i in range(length):
    ans += a[i] + b[i]
if M >N:
    ans+= a[i+1:]
elif M< N:
    ans += b[i+1:]
print (ans)
