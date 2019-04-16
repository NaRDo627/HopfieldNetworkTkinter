from tkinter import *
import copy

NODE = 11


class HopfieldNetwork:
    input = []
    weight = []
    node_count = 0
    try_count = 5

    def __init__(self, row_count, column_count):
        self.node_count = row_count * column_count
        self.input = [0] * self.node_count
        self.weight = [[0] * (self.node_count * self.node_count) for j in range(self.node_count * self.node_count)]

    def learn_hopfield(self, filename, input_list):
        # 1. 패턴을 학습하며 가중치를 조정한다.
        pattern_list = self.learn_weight(filename)
        if pattern_list is None:
            return None
        if not self.copy_input(input_list):
            return None

        # 2. 반복문을 돌면서 일치하는 패턴이 있으면 리턴한다.
        for step in range(0, self.try_count):
            print(step)
            # 3. 출력값을 조정한다.
            output_list = self.transfer_input_to_output()

            if self.check_match(pattern_list, output_list):
                return output_list
            self.copy_input(output_list)
        return None

    def copy_input(self, input_list):
        if len(input_list) != self.node_count:
            return False
        self.input = copy.deepcopy(input_list)
        return True

    def learn_weight(self, filename):
        try:
            # 클래스를 파일로 학습시킨다
            pattern_list = []
            f = open(filename, 'r')
            while True:
                line = f.readline().replace(" ", "").replace("\n", "").replace("\r", "")
                if line is None or len(line) == 0:
                    break

                # 패턴 라인 맨 앞이 x라면 읽지 않음 (테스트용 코드)
                if line[0] == 'x':
                    continue

                data = list(line)

                # 양극화
                for i in range(0, len(data)):
                    if data[i] == "0":
                        data[i] = -1
                    else:
                        data[i] = 1

                pattern_list.append(data)
            f.close()

            # weight 행렬 연산
            for pattern in pattern_list:
                for i in range(0, self.node_count):
                    for j in range(0, self.node_count):
                        if i == j:
                            self.weight[i][j] = 0
                            continue
                        self.weight[i][j] += int(pattern[i]) * int(pattern[j])

            return pattern_list

        except:
            return None

    def transfer_input_to_output(self):
        # 전이 함수에 대입
        output_list = [0] * self.node_count
        for i in range(0, self.node_count):
            tmp = self.input[i]
            for j in range(0, self.node_count):
                tmp += (self.input[j] * self.weight[i][j])

            # 계단함수 적용
            if tmp > 0:
                tmp = 1
            elif tmp < 0:
                tmp = -1

            output_list[i] = tmp

        return output_list

    def check_match(self, pattern_list, output_list):
        for pattern in pattern_list:
            if pattern == output_list:
                return True
        return False


def main():
    def toggle_color(event):
        background = "black" if event.widget['bg'] == 'white' else "white"
        event.widget.configure(background=background)

    def on_click_clear():
        canvas.delete(ALL)
        msg.config(text="")
        for button_obj in button_list:
            button_obj.config(bg="white")

    def on_click_input():
        canvas.delete(ALL)
        msg.config(text="")
        hopfield = HopfieldNetwork(NODE, NODE)

        input_list = [0]*NODE*NODE
        for i in range(0, len(button_list)):
            if button_list[i]['bg'] == 'white':
                input_list[i] = -1
            else:
                input_list[i] = 1
        input_flat = input_list
       # input_flat = list(itertools.chain.from_iterable(Input))
        while True:
            try:
                index = input_flat.index(0)
            except:
                break

            input_flat[index] = -1
        output_list = hopfield.learn_hopfield("./pattern.txt", input_flat)
        print(output_list)
        if output_list is None:
            msg.config(text="No pattern matched", fg="red")
            return

        length = 30
        for i in range(0, len(output_list)):
            offset = i * length
            x1 = (offset % 330) + (i % 11) * 5
            y1 = int(offset / 330) * (length + 5)
            x2 = x1 + length
            y2 = y1 + length

            if output_list[i] == 1:
                color = "#000000"
            else:
                color = "#ffffff"

            canvas.create_polygon(x1, y1, x2, y1, x2, y2, x1, y2, outline=color, fill=color)
        msg.config(text="Pattern found!", fg="blue")
        #canvas.pack()

    root = Tk()
    root.title('Hopfield Network Example - 201333543 박현국')
    root.geometry('1050x600+10+10')
    root.resizable(False, False)
    dummy = Label(root, text="\t\n")
    dummy.grid(row=0, column=0)

    button_list = []
    for i in range(0, NODE):
        for j in range(0, NODE):
            button = Button(root, background="white", height=1, width=1)
            button.grid(row=i+1, column=j+1)
            button.bind("<Button-1>", toggle_color)
            button_list.append(button)

    dummy2 = Label(root, text="   ")
    dummy2.grid(row=int(NODE / 2), column=NODE+1)
    input_button = Button(root, text="입력", command=on_click_input)
    input_button.grid(row=int(NODE / 2), column=NODE + 2)
    arrow = Label(root, text="=======>", font=("Courier", 15))
    arrow.grid(row=int(NODE / 2)+1, column=NODE + 2)
    clear_button = Button(root, text="초기화", command=on_click_clear)
    clear_button.grid(row=int(NODE / 2)+2, column=NODE + 2)
    canvas = Canvas(root, width=380, height=380)
    canvas.place(x=590, y=45)
    msg = Label(root, text="", fg="red")
    msg.place(x=450, y=500)
    root.mainloop()


if __name__ == '__main__':
    main()
