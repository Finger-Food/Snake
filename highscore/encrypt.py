import random
def read():
    score = ''
    comp = {}
    valid = True
    count = 0
    with open('High Score.txt') as f:
        for line in f:
            count += 1
            line = list(line.strip())
            line = [int(i) for i in line]
            if len(line) != 9:
                continue
            elif sum(line[-3:]) != 8:
                continue
            elif (line[2] - line[5]) != 2:
                continue
            else:
                pos = (line[1] + 7)%10
                curr = (line[3] - 4)%10
                comp[pos] = str(curr)
                
    if count < 50 or count > 100:
        valid = False
    elif len(comp) == 0:
        valid = False
    if valid == False:
        return valid
    else:
        for i in sorted(comp):
            score += comp[i]
        return int(score)
    
def write(score):
    comp = []
    fin = random.randint(50, 100)
    score = list(str(score))
    for i in range(len(score)):
        score[i] = (int(score[i]) + 4)%10
    score_lines = []
    for i in score:
        curr = random.randint(1, fin)
        while curr in score_lines:
            curr = random.randint(1, fin)
        score_lines.append(curr)
    for i in range(fin):
        line = []
        if i + 1 in score_lines:
            line.append(random.randint(0, 9))
            line.append((score_lines.index(i+1)-7)%10)
            line.append(random.randint(2, 9))
            line.append(score[score_lines.index(i+1)])
            line.append(random.randint(0, 9))
            line.append(line[2] - 2)
            line.append(random.randint(0, 8))
            line.append(random.randint(0, 8 - line[6]))
            line.append(8 - sum(line[6:]))
        else:
            for cap in range(random.randint(8, 12)):
                line.append(random.randint(0, 9))
            if len(line) == 9:
                while line[2] == (line[5] + 2):
                    line[5] = random.randint(0, 9)
        line = ''.join([str(i) for i in line])
        comp.append(line)
        
        with open('High Score.txt', 'w') as f:
            for line in comp:
                print(line, file=f)
