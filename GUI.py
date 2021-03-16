import tkinter as tk

from move_car_auto import car_move_auto

LEFT = 'a'
RIGHT = 'd'
FORWARD = 'w'
BACKWARD = 's'
O_UP = (0, -1)
O_DOWN = (0, 1)
O_LEFT = (-1, 0)
O_RIGHT = (1, 0)
SIZE = 8
START = (0, SIZE - 1)
DIRS = [O_UP, O_LEFT, O_DOWN, O_RIGHT]
TIMES = {LEFT: 1, RIGHT: 1, FORWARD: 1}


class GUI:
    def __init__(self):
        self.last_place = START
        self.orientation = O_UP
        self.move_list = []
        self.root = tk.Tk()
        self.root.title("Kaplan's Killing Machine")
        self.move_label = tk.Label(master=self.root, text="")
        self.move_label.pack()
        self.grid_frame = tk.Frame(master=self.root, background="red")
        self.grid_frame.pack()
        self.send = tk.Button(master=self.root, text="GO!", command=self.send)
        self.send.pack()
        l = SIZE
        for i in range(l):
            for j in range(l):
                button = tk.Button(master=self.grid_frame, text=i * l + j, background="lightgrey")
                y = 5 * int(int(l / 2) == i)
                x = 5 * int(int(l / 2) == j)
                button.grid(column=j, row=i, sticky=tk.NSEW, pady=(y, 0), padx=(x, 0))
                button.config(font=("Courier", 20))
                button.bind("<Button-1>", self.left_click(button))
                button.bind("<Button-3>", self.right_click(button))
                if (j,i) == START:
                    button.config(background="purple")

        self.root.mainloop()

    def send(self):
        # print([(item, TIMES[item]) for item in self.move_list])
        # pass
        ins = [('w', 1)]+[(item, TIMES[item]) for item in self.move_list]
        car_move_auto(ins)

    def left_click(self, button):
        def inner(e):
            bg = button["background"]
            if bg == "lightgrey":
                button.config(background="blue")
            elif bg == "red":
                button.config(background="lightgrey")
            elif bg == "blue":
                button.config(background="green")
            elif bg == "green":
                button.config(background="red")

        return inner

    def right_click(self, button):
        def inner(e):
            x = int(button["text"]) % SIZE
            y = int(button["text"]) // SIZE
            dir = (x - self.last_place[0], y - self.last_place[1])
            if dir[0] ** 2 + dir[1] ** 2 == 1:
                while dir != self.orientation:
                    self.move_list.append(LEFT)
                    ind = DIRS.index(self.orientation)
                    self.orientation = DIRS[(ind + 1) % len(DIRS)]
                    self.last_place = (x, y)
                self.last_place = (x, y)
                if len(self.move_list) >= 3 and self.move_list[-1] == self.move_list[-2] == self.move_list[-3] == LEFT:
                    self.move_list.pop()
                    self.move_list.pop()
                    self.move_list.pop()
                    self.move_list.append(RIGHT)
                    self.move_list.append(FORWARD)
                elif len(self.move_list) >= 2 and self.move_list[-1] == self.move_list[-2] == LEFT:
                    self.move_list.pop()
                    self.move_list.pop()
                    self.move_list.append(BACKWARD)
                    self.orientation = (-self.orientation[0], -self.orientation[1])
                else:
                    self.move_list.append(FORWARD)
                self.move_label["text"] = str(self.move_list)
            return

        return inner


if __name__ == '__main__':
    gui = GUI()
