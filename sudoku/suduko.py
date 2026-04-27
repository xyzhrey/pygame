l=[[5,3,0,0,7,0,0,0,0],
   [6,0,0,1,9,5,0,0,0],
   [0,9,8,0,0,0,0,6,0],
   [8,0,0,0,6,0,0,0,3],
   [4,0,0,8,0,3,0,0,1],
   [7,0,0,0,2,0,0,0,6],
   [0,6,0,0,0,0,2,8,0],
   [0,0,0,4,1,9,0,0,5],
   [0,0,0,0,8,0,0,7,9]]

def possible(x, y, n):
    for i in range(9):
        if l[x][i]==n:
            return False
        if l[i][y]==n:
            return False
        
    x0=(x//3)*3
    y0=(y//3)*3
    for p in range(3):
        for q in range(3):
            if l[x0+p][y0+q]==n:
                return False
            
    return True

def solve():
    global l
    for i in range(9):
        for j in range(9):
            if l[i][j]==0:
                for n in range(1, 10):
                    if possible(i,j,n):
                        l[i][j]=n
                        solve()
                        l[i][j]=0

                return
    for p in range(9):
        print(l[p])
    
solve()