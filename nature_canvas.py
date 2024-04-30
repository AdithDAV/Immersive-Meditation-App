import tkinter as tk
import socket
import threading
import math

class NatureCanvas:
    def __init__(self, root):
        self.root = root
        self.root.title("Nature Canvas")
        self.canvas = tk.Canvas(root, width=600, height=600, bg='white')
        self.canvas.pack()
        self.canvas.create_line(300, 0, 300, 600, fill='gray')
        self.canvas.create_line(0, 300, 600, 300, fill='gray')

        # Main user rectangle
        self.user = self.canvas.create_rectangle(290, 290, 310, 310, fill='blue')

        # Directional indicator (initially pointing north)
        self.indicator = self.canvas.create_polygon(300, 280, 290, 290, 310, 290, fill='red')

        self.root.bind('<Left>', self.move_left)
        self.root.bind('<Right>', self.move_right)
        self.root.bind('<Up>', self.move_up)
        self.root.bind('<Down>', self.move_down)

        # Bind keys for direct direction control
        self.root.bind('w', self.set_north)
        self.root.bind('s', self.set_south)
        self.root.bind('d', self.set_east)
        self.root.bind('a', self.set_west)

        self.tree_image = tk.PhotoImage(file='images/tree.png')
        self.pond_image = tk.PhotoImage(file='images/pond.png')
        self.duck_image = tk.PhotoImage(file='images/duck.png')
        self.birds_image = tk.PhotoImage(file='images/birds.png')

        self.tree1 = self.canvas.create_image(50, 50, image=self.tree_image, anchor='nw')
        self.tree2 = self.canvas.create_image(250, 250, image=self.tree_image, anchor='nw')
        self.tree3 = self.canvas.create_image(300, 400, image=self.tree_image, anchor='s')
        self.tree4 = self.canvas.create_image(550, 550, image=self.tree_image, anchor='se')
        self.tree5 = self.canvas.create_image(400, 100, image=self.tree_image, anchor='ne')
       

        self.pond1 = self.canvas.create_image(450, 450, image=self.pond_image, anchor='se')
        self.pond2 = self.canvas.create_image(150, 150, image=self.pond_image, anchor='nw')

        # self.duck = self.canvas.create_oval(100, 450, 10, 10, outline = "black", fill = "white",width = 2)
        self.duck = self.canvas.create_oval(95, 445, 105, 455, fill="black", outline="black")
        self.birds = self.canvas.create_oval(495, 195, 505, 205, fill="black", outline="black")



        # self.duck = self.canvas.create_arc(500, 200, 5, fill='black')


        # self.duck = self.canvas.create_image(100, 450, image=self.duck_image, anchor='sw')

        # self.birds = self.canvas.create_image(500, 200, image=self.birds_image, anchor='ne')

        self.directions = ['north', 'east', 'south', 'west']  # Circular list of directions
        self.direction = 'north'  # Start facing north by default

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 5001))
        self.server_socket.listen(1)
        print("Server listening on port 5001...")
        threading.Thread(target=self.accept_connections).start()

    def set_north(self, event):
        self.current_direction_index = 0
        self.direction = 'north'
        self.update_indicator()
        self.send_position_update()

    def set_south(self, event):
        self.current_direction_index = 2
        self.direction = 'south'
        self.update_indicator()
        self.send_position_update()

    def set_east(self, event):
        self.current_direction_index = 1
        self.direction = 'east'
        self.update_indicator()
        self.send_position_update()

    def set_west(self, event):
        self.current_direction_index = 3
        self.direction = 'west'
        self.update_indicator()
        self.send_position_update()

    def update_indicator(self):
        x1, y1, x2, y2 = self.canvas.coords(self.user)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        if self.direction == 'north':
            points = [cx, y1 - 10, cx - 5, y1, cx + 5, y1]
        elif self.direction == 'south':
            points = [cx, y2 + 10, cx - 5, y2, cx + 5, y2]
        elif self.direction == 'east':
            points = [x2 + 10, cy, x2, cy - 5, x2, cy + 5]
        elif self.direction == 'west':
            points = [x1 - 10, cy, x1, cy - 5, x1, cy + 5]
        self.canvas.coords(self.indicator, points)

    def send_position_update(self):
        x1, y1, x2, y2 = self.canvas.coords(self.user)
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        if hasattr(self, 'client_socket'):
            position_data = f"{x},{y},{self.direction}\n".encode()
            self.client_socket.sendall(position_data)

    def accept_connections(self):
        self.client_socket, addr = self.server_socket.accept()
        print(f"Connected to {addr}")

    def update_position(self, x, y):
        self.canvas.coords(self.user, x-10, y-10, x+10, y+10)
        self.update_indicator()
        self.send_position_update()

    def move_left(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.user)
        self.update_position(x1 - 10, (y1 + y2) / 2)

    def move_right(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.user)
        self.update_position(x2 + 10, (y1 + y2) / 2)

    def move_up(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.user)
        self.update_position((x1 + x2) / 2, y1 - 10)

    def move_down(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.user)
        self.update_position((x1 + x2) / 2, y2 + 10)

if __name__ == "__main__":
    root = tk.Tk()
    app = NatureCanvas(root)
    root.mainloop()
