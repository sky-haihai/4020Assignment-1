locker=True
try:
  print(x)
  locker=False
  print('reached')
except:
  locker=True
    
print(locker)