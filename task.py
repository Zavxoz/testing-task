import shutil


def draw_canvas(wc, hc):
    with open("output.txt", "a") as f:
        f.write("-"*(wc+2)+"\n"+("|"+" "*wc+"|\n")*hc+"-"*(wc+2)+"\n")


def horizontal_line(start, length, nline, wc):
    with open("output.txt", "r+") as f:
        f.seek((wc+3)*(nline-1))
        tmp = f.readlines()
        tmp[0] = tmp[0][:start]+'x'*length+tmp[0][start+length:len(tmp[0])]
        f.seek((wc+3)*(nline-1))
        f.truncate()
        f.writelines(tmp)


def vertical_line(pl, nline, offset, wc):
    with open("output.txt", "r+") as f:
        f.seek((wc+3)*(nline-1))
        tmp = f.readlines()
        i = 0
        for i in range(offset+1):
            tmp[i] = tmp[i][0:pl]+'x'+tmp[i][pl+1:len(tmp[i])]
        f.seek((wc+3)*(nline-1))
        f.truncate()
        f.writelines(tmp)


def diagonal_line(x1, y1, x2, y2, nline):pass

def redraw(wc, hc):
    with open("output.txt", "a+b") as f:
        f.seek((wc+3)*(-hc-2), 2)
        f.writelines(f.readlines())


def origin_char(x, wc, nline):
    with open("output.txt", "r") as f:
        f.seek((wc+3)*nline+x+1)
        return f.read(1)


def fill(nline, wc, y, x, character, original, hc):
    with open("output.txt", "r+") as f:
        f.seek((nline-y-1)*(wc+3))
        tmp = f.readlines()
        for el in range(hc+2):
            tmp[el] = list(tmp[el])
        tmp = fill_operation(x, y, character, original, wc, hc, tmp)
        f.seek((nline-y-1)*(wc+3))
        f.truncate()
        for i in range(hc+2):
            tmp[i] = ''.join(tmp[i])
        f.writelines(tmp)


def fill_operation(x, y, character, original, wc, hc, lines):
    current = lines[y][x]
    if current == original:
        lines[y][x] = character
        if x - 1 > 0:
            fill_operation(x - 1, y, character, original, wc, hc, lines)
        if y - 1 > 0:
            fill_operation(x, y - 1, character, original, wc, hc, lines)
        if x + 1 <= wc:
            fill_operation(x + 1, y, character, original, wc, hc, lines)
        if y + 1 <= hc:
            fill_operation(x, y + 1, character, original, wc, hc, lines)
    return lines


def main():
    with open("input.txt", "r") as commands:
        with open("output.txt", "w+") as output:
            count = 0
            for line in commands.readlines():
                if line.endswith('\n'):
                    line = line[:-1]
                tmp = line.split(' ')
                for el in tmp:
                    if el.isalpha() and el.isdigit():
                        print("wrong line")
                        continue
                if tmp[0] not in ['C', 'L', 'B', 'R']:
                    print("wrong input file")
                    break
                elif tmp[0] == 'C':
                    if count > 0 and len(output.readline()) != 0:
                        shutil.copy(r'output.txt', 'output'+str(count)+'.txt')
                        output.seek(0)
                        output.truncate()
                    count = count+1
                    wc = int(tmp[1])
                    hc = int(tmp[2])
                    if hc <= 0 or wc <=0:
                        print("wrong arguments in line", line)
                        continue
                    draw_canvas(wc, hc)
                    continue
                elif tmp[0] == 'L':
                    if count == 0:
                        print("Please, create a canva")
                        continue
                    redraw(wc, hc)
                    del tmp[0]
                    tmp = [int(item) for item in tmp]
                    if abs(tmp[3]-tmp[1]) > hc or abs(tmp[3]-tmp[1]) > wc:
                        print("Wrong coordinates in line", line)
                        continue
                    output.seek(0)
                    nline = abs(len(output.readlines())-hc-1+tmp[1])
                    if tmp[1] == tmp[3]:
                        horizontal_line(tmp[0], abs(tmp[2]-tmp[0])+1, nline, wc)
                    elif tmp[0] == tmp[2]:
                        vertical_line(tmp[0], nline, abs(tmp[3]-tmp[1]), wc)
                    else:
                        if tmp[0] < tmp[2]:
                            diagonal_line(tmp[0], tmp[1], tmp[2], tmp[3], nline)
                        else:
                            diagonal_line(tmp[2], tmp[3], tmp[0], tmp[1], nline)
                    continue
                elif tmp[0] == 'R':
                    if count == 0:
                        print("Please, create a canva")
                        continue
                    redraw(wc, hc)
                    del tmp[0]
                    tmp = [int(item) for item in tmp]
                    output.seek(0)
                    nline1 = abs(len(output.readlines())-hc-1+tmp[1])
                    nline2 = nline1+tmp[3]-tmp[1]
                    for i in range(4):
                        if tmp[i] < 1 or tmp[i] > wc:
                            print("wrong arguments of command", line)
                            continue
                    vertical_line(tmp[0], nline1, abs(tmp[3]-tmp[1]), wc)
                    vertical_line(tmp[2], nline1, abs(tmp[3]-tmp[1]), wc)
                    horizontal_line(tmp[0], abs(tmp[2]-tmp[0]), nline1, wc)
                    horizontal_line(tmp[0], abs(tmp[2]-tmp[0]), nline2, wc)
                    continue
                elif tmp[0] == "B":
                    if count == 0:
                        print("Please, create a canva")
                        continue
                    redraw(wc, hc)
                    x = int(tmp[1])
                    y = int(tmp[2])
                    if 0>x>wc or 0>y>hc:
                        print("wrong arguments in line ", line)
                        continue
                    output.seek(0)
                    nline = abs(len(output.readlines())-hc-1+y)
                    fill(nline, wc, y, x, tmp[3], origin_char(x, wc, nline), hc)
                    continue


if __name__ == "__main__":
    main()
