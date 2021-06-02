import sys
input = sys.stdin.readline

def step(adj,PR,outdeg):
    new_PR = [0.]*len(PR)
    for children,points,deg in zip(adj,PR,outdeg):
        cut = points/deg
        for child in children:
            new_PR[child] += cut
    return new_PR

def main():
    N,E,M = map(int,input().split())
    P,I = map(int,input().split())
    input()
    adj = [list(map(int,input().split())) for i in range(N)]
    outdeg = [len(i) for i in adj]
    PR = [1.]*N

    for i in range(1000):
        new_PR = step(adj,PR,outdeg)
        error = sum(abs(i-j) for i,j in zip(new_PR,PR))
        PR = new_PR
        if error < 1e-7:
            break
    vaccinated = sorted([(rank,i) for i,rank in enumerate(PR)], reverse=True)[:M]
    vaccinated = [i[1] for i in vaccinated]

    print(N,E,M)
    print(P,I)
    print(' '.join(str(j) for j in vaccinated))
    for i in adj:
        print(' '.join(str(j) for j in i))

main()

