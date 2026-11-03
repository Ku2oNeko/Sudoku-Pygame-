import pygame

#เลขศูนย์ในโจทย์ถือเป็นช่องว่างให้ผู้เล่นแก้
test_puzzle = [[5, 3, 0,  0, 7, 0,  0, 0, 0],
    [6, 0, 0,  1, 9, 5,  0, 0, 0],
    [0, 9, 8,  0, 0, 0,  0, 6, 0],
    [8, 0, 0,  0, 6, 0,  0, 0, 3],
    [4, 0, 0,  8, 0, 3,  0, 0, 1],
    [7, 0, 0,  0, 2, 0,  0, 0, 6],
    [0, 6, 0,  0, 0, 0,  2, 8, 0],
    [0, 0, 0,  4, 1, 9,  0, 0, 5],
    [0, 0, 0,  0, 8, 0,  0, 7, 9],]

test_key = [[5, 3, 4,  6, 7, 8,  9, 1, 2],
    [6, 7, 2,  1, 9, 5,  3, 4, 8],
    [1, 9, 8,  3, 4, 2,  5, 6, 7],
    [8, 5, 9,  7, 6, 1,  4, 2, 3],
    [4, 2, 6,  8, 5, 3,  7, 9, 1],
    [7, 1, 3,  9, 2, 4,  8, 5, 6],
    [9, 6, 1,  5, 3, 7,  2, 8, 4],
    [2, 8, 7,  4, 1, 9,  6, 3, 5],
    [3, 4, 5,  2, 8, 6,  1, 7, 9],]


#puzzle = {'Easy':[], 'Normal':[], 'Hard':[]}

#คลาสของแต่ละช่อง
class Cell:
    def __init__(self, row, col, key, digit, color):
        self.row = row
        self.col = col
        self.key = key
        self.digit = digit
        self.color = color
        self.IsSelecting = False #สถานะเลือกอยู่หรือไม่ True=เลือกอยู่ / False=ไม่ได้เลือก
        self.sensor = pygame.Rect((23+(self.col-1)*\
        53+((self.col - 1) // 3) * 3,53+(self.row-1)*53+((self.row - 1) // 3) * 3,cell_size,cell_size))
        
        '''X_domain_func = 23+(self.col-1)*53+((self.col - 1) // 3) * 3
        Y_domain_func = 53+(self.row-1)*53+((self.row - 1) // 3) * 3
        self.domain = ((X_domain_func,X_domain_func+50), (Y_domain_func,Y_domain_func+50))'''

        if digit != 0: #เลขศูนย์ในโจทย์ถือเป็นช่องว่างให้ผู้เล่นแก้
            self.isinit = True #True=เป็นเลขที่โจทย์ให้มา
        else:
            self.isinit = False #False=ไม่เป็นเลขที่โจทย์ให้มา

    def input_digit(self):
        pass
    
    def is_key(self):
        pass

    def select(self):
        if self.IsSelecting == False:
            self.IsSelecting = True
            self.color = (200,200,200)
        else:
            self.IsSelecting = False
            self.color = default_color
        pass

    def draw(self, screen):
        #pygame.draw.rect(screen,(255,255,255),(cellX,cellY,cell_size,cell_size))
        pygame.draw.rect(screen, self.color,(23+(self.col-1)*\
53+((self.col - 1) // 3) * 3,53+(self.row-1)*53+((self.row - 1) // 3) * 3,cell_size,cell_size))
        
        
        
    '''def __str__(self):
        return self.row, self.col, self.key, self.digit
        pass'''

ObjList = []
ObjBunch = []
default_color = (255,255,255)
run = True
cell_size = 50

for y in range(1,10):
    ObjRow = []
    for x in range(1,10):
        ObjRow.append(Cell(y,x,test_key[y-1][x-1],test_puzzle[y-1][x-1],default_color))
    ObjList.append(ObjRow)

for item in ObjList:
    ObjBunch += item

#เริ่มเกม
pygame.init()

#สร้างจอ
screen = pygame.display.set_mode((800,600))

#ชื่อ window tab
pygame.display.set_caption("Sudoku")

#ไอคอน
'''
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)'''

#เปิดจอเกมค้างไว้
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            for cell in ObjBunch:
                if cell.sensor.collidepoint(event.pos):
                    for selected_cell in ObjBunch:
                        if selected_cell.IsSelecting == True:
                            selected_cell.select()
                    cell.select()
                    print((cell.row,cell.col))
    #พื้นหลัง
    screen.fill((255,255,255))
    
    #ตาราง
    pygame.draw.rect(screen,(0,0,0),(20,50,486,486))
    for r in ObjList:
        for cell in r:
            cell.draw(screen)

    
    pygame.display.update()
