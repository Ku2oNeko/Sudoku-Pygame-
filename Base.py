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
        self.key = key #เลขเฉลย
        self.digit = digit #ค่าเลขที่ผู้เล่นป้อน
        self.color = color
        self.IsSelecting = False #สถานะเลือกอยู่หรือไม่ True=เลือกอยู่ / False=ไม่ได้เลือก
        
        self.sensor = pygame.Rect((23+(self.col-1)*53+((self.col - 1) // 3) * 3,
53+(self.row-1)*53+((self.row - 1) // 3) * 3,cell_size,cell_size)) #ตัวกล่องล่องหนตรวจจับการคลิกแต่ละช่อง

        if digit != 0: #เลขศูนย์ในโจทย์ถือเป็นช่องว่างให้ผู้เล่นแก้
            self.isinit = True #True=เป็นเลขที่โจทย์ให้มา
            self.iscorrect = True
        else:
            self.isinit = False #False=ไม่เป็นเลขที่โจทย์ให้มา
            self.iscorrect = False
        

    def input_digit(self,digit):
        self.digit = digit
        pass
    
    def check(self):
        global attempt
        if self.digit == self.key:
            self.iscorrect = True
            self.color = (150,255,150)
        else:
            attempt -= 1
            self.color = (255,150,150)
        pass

    def select(self):
        if self.IsSelecting == False:
            self.IsSelecting = True
            self.color = (200,200,255)
        else:
            self.IsSelecting = False
            self.color = default_color
            if self.isinit == False and self.iscorrect == True:
                self.color = (150,255,150)
        pass

    def draw(self, screen):
        #pygame.draw.rect(screen,(255,255,255),(cellX,cellY,cell_size,cell_size))
        pygame.draw.rect(screen, self.color,(23+(self.col-1)*53+((self.col - 1) // 3) * 3,
53+(self.row-1)*53+((self.row - 1) // 3) * 3,cell_size,cell_size)) #พื้นหลังช่องสีขาว

        if self.digit !=0 and self.digit != None and self.isinit == False:
            digit_text = digit_font.render(str(self.digit), True, (50,50,255))
            screen.blit(digit_text, ((23+(self.col-1)*\
            53+((self.col - 1) // 3) * 3 + 14,53+(self.row-1)*53+((self.row - 1) // 3) * 3 + 8)))

    def init_digit(self,digit):
        
        digit_text = digit_font.render(str(digit), True, (0,0,0))
        screen.blit(digit_text, ((23+(self.col-1)*\
53+((self.col - 1) // 3) * 3 + 14,53+(self.row-1)*53+((self.row - 1) // 3) * 3 + 8)))
        pass
        
        
    '''def __str__(self):
        return self.row, self.col, self.key, self.digit
        pass'''

ObjList = [] #โจทย์ในรูปของ Listที่บรรจุ แถวของListที่บรรจุ Object ของช่องอีกที [[row1],[row2], ..., [row9]]
                # rowN = [CellN1, CellN2, Cell N3, ..., Cell N9]
ObjBunch = [] # #โจทย์ในรูปของ Object ช่องเดี่ยวๆ [Cell_11, Cell_12, Cell_13, ..., Cell_99] 
default_color = (230,230,230)
run = True
cell_size = 50
target = None #ช่องที่กำลังเลือกอยู่
digit_font_size = 40
center_font_size = 100
attempt_font_size = 50
attempt = 3
done = None

#สร้างโจทย์ในรูปของ Listที่บรรจุ แถวของListที่บรรจุ Object ของช่องอีกที [[row1],[row2], ..., [row9]]
for y in range(1,10):
    ObjRow = []
    for x in range(1,10):
        ObjRow.append(Cell(y,x,test_key[y-1][x-1],test_puzzle[y-1][x-1],default_color))
    ObjList.append(ObjRow)

##สร้างโจทย์ในรูปของ Object ช่องเดี่ยวๆ [Cell_11, Cell_12, Cell_13, ..., Cell_99] 
for item in ObjList:
    ObjBunch += item

#เริ่มเกม
pygame.init()

digit_font = pygame.font.Font('freesansbold.ttf', digit_font_size)
center_font = pygame.font.Font('freesansbold.ttf', center_font_size)
attempt_font = pygame.font.Font('freesansbold.ttf', attempt_font_size)


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

    #Event
    for event in pygame.event.get():
        #Event ปิดโปรแกรมเกม
        if event.type == pygame.QUIT:
            run = False
        
        #Event กดเลือกช่องในตาราง
        if event.type == pygame.MOUSEBUTTONUP:
            for cell in ObjBunch:
                if cell.sensor.collidepoint(event.pos):
                    target = cell
                    for selected_cell in ObjBunch:
                        if selected_cell.IsSelecting == True:
                            selected_cell.select()
                    cell.select()
                    print((cell.row,cell.col), cell.digit)

        #Event ใส่และลบเลข
        if event.type == pygame.KEYDOWN:
            if target != None and target.isinit == False and target.iscorrect == False:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    digit = 1
                    target.input_digit(digit)
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    digit = 2
                    target.input_digit(digit)
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    digit = 3
                    target.input_digit(digit)
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    digit = 4
                    target.input_digit(digit)
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    digit = 5
                    target.input_digit(digit)
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    digit = 6
                    target.input_digit(digit)
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    digit = 7
                    target.input_digit(digit)
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    digit = 8
                    target.input_digit(digit)
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    digit = 9
                    target.input_digit(digit)
                if event.key == pygame.K_BACKSPACE \
                or event.key == pygame.K_DELETE \
                or event.key == pygame.K_KP_MINUS:
                    digit = 0
                    target.input_digit(digit)
                if event.key == pygame.K_RETURN:
                    target.check()
                    
                
    #พื้นหลัง
    screen.fill((100,100,100))
    
    #ตาราง-----------------------------------------
    pygame.draw.rect(screen,(0,0,0),(20,50,486,486))
    for r in ObjList:
        for cell in r:
            cell.draw(screen)

    #เลขที่โจทย์ให้มา
    for Obj in ObjBunch:
        if Obj.isinit == True:
            Obj.init_digit(Obj.digit)

    #----------------------------------------------

    #ระบบ GameOver และจำนวนชีวิต
    if attempt > 0:
        attempt_text = attempt_font.render('Lives: '+ f'{attempt}', True, (0,0,0))
        screen.blit(attempt_text, (570,100))

    if attempt <= 0:
        center_text = center_font.render('GAMEOVER', True, (255,0,0))
        pygame.draw.rect(screen, (0,0,0), (0,0,800,600))
        screen.blit(center_text, (110,220)) 

    # ระบบตรวจการชนะ
    corrected_count = 0
    for c_cell in ObjBunch:
        if c_cell.iscorrect == True:
            corrected_count += 1

    if corrected_count == 81:
        center_text = center_font.render('CLEARED', True, (0,255,0))
        screen.blit(center_text, (400,300)) 

    pygame.display.update()
