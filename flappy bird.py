import pygame,sys,random
#tạo riêng một hàm cho sàn 
def draw_floor():
    screen.blit(floor,(floor_x_pos,500))
    screen.blit(floor,(floor_x_pos+324,500)) 
#tạo hàm cho các ống    
def create_pipe():
    #tạo vị trí và chiều cao ngẫu nhiên của ống 
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop= (400,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop= (400,random_pipe_pos-750))
    return bottom_pipe,top_pipe
#tạo hàm các ống di chuyển
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -=5
    return pipes 
#tạo hàm các ống , lật ngược các ống trên    
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom>= 576:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe =pygame.transform.flip(pipe_surface,False,True) 
            screen.blit(flip_pipe,pipe) 
#tạo hàm xử lí va chạm             
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe): 
            hit_sound.play()
            return False
    if bird_rect.top <=-75 or bird_rect.bottom>=500:
            return False                
    return True 
#tạo hàm xoay chim
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)  
    return new_bird  
#tạo hàm cho cánh chim                 
def bird_animation():
    new_bird =bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect
#tạo hệ thống tính điểm    
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)) ,True,(255,255,255))    # 3 số 255 quy ước màu trắng
        score_rect = score_surface.get_rect(center = (200,20))  # tọa độ score
        screen.blit (score_surface,score_rect)
    if game_state == 'game_over':  
        score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))    
        score_rect = score_surface.get_rect(center = (200,20))  
        screen.blit (score_surface,score_rect)  

        high_score_surface = game_font.render(f'High Score: {int(high_score)}' ,True,(255,255,255))  
        high_score_rect = high_score_surface.get_rect(center = (150,480))  
        screen.blit (high_score_surface,high_score_rect)
def update_score(score,high_score):
    if score > high_score :
        high_score= score
    return high_score  
#chỉnh âm thanh thích hợp cho pygame      
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer= 512)
pygame.init()
screen = pygame.display.set_mode((324,576))
clock =pygame.time.Clock()
game_font= pygame.font.Font('04B_19.ttf',40)

#tạo các biến cho trò chơi
#tạo trọng lực để bay
gravity=0.25
bird_movement=0
game_active = True
score =0
high_score =0 
#chèn background
#.convert chuyển file ảnh giúp pygame load nhanh hơn
bg=pygame.image.load('assets/background-night.png').convert()
bg=pygame.transform.scale2x(bg) 
#chèn sàn
floor=pygame.image.load('assets/floor.png').convert()
floor=pygame.transform.scale2x(floor)
#dịch chuyển sàn sang bên trái
floor_x_pos=0
#tạo chim
#convert_alpha loại bỏ hình cn đen khi dùng zotoroom
bird_down=pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid=pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up=pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list= [bird_down,bird_mid,bird_up]  #0,1,2
bird_index = 0
bird= bird_list[bird_index]
#bird = pygame.image.load('assets/yeallowbird-midflap.png')
#bird = pygame.transform.scale2x(bird)
#tạo hình chữ nhật xung quanh con chim
bird_rect=bird.get_rect(center = (100,288))
#tạo timer cho chim đập cánh
birdflap = pygame.USEREVENT +1
pygame.time.set_timer(birdflap,200) #200mili giây
#tạo ống
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list =[]
#tạo timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1200) # sau 1.2s tạo ống mới
pipe_height = [300,350,400]
#tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(162,250))
#chèn âm thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')    #âm thanh vỗ cánh
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')      #âm thanh khi va cột
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')  #âm thanh khi ghi điểm
score_sound_countdown = 100 #đếm ngược 
#while loop của trò chơi
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement =-7  
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active==False:
                game_active=True
                pipe_list.clear()
                bird_rect.center = (100,288)
                bird_movement    = 0
                score = 0
        if event.type == spawnpipe :
            pipe_list.extend(create_pipe()) 
        if event.type == birdflap:
            if bird_index <2:
                bird_index +=1
            else :
                bird_index =0
            bird , bird_rect = bird_animation()                
    #tọa độ
    screen.blit(bg,(0,0))
    if game_active :
        #chim di chuyển trọng lực tăng
        bird_movement  += gravity
        #tạo chuyển động lên xuống cho con chim
        rotated_bird =rotate_bird(bird)
        screen.blit(rotated_bird ,(bird_rect))
        #ra màn hình kết thúc khi chim va chạm ống
        game_active=check_collision(pipe_list)
        #lấy ống tạo ra trong pipe_list di chuyển rồi tạo ra list mới
        pipe_list =move_pipe(pipe_list)
        draw_pipe(pipe_list) 
        #làm con chim di chuyển xuống dưới
        bird_rect.centery += bird_movement
        #sàn di chuyển sang trái 
        # + điểm bay càng lâu càng nhiều điểm
        score +=0.01
        score_display('main game')
        score_sound_countdown -= 1
        #tạo âm thanh ghi điểm 
        if score_sound_countdown <=0 :
            score_sound.play()
            score_sound_countdown = 100 
    else :
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score (score, high_score)
        score_display('game_over')        
    floor_x_pos -=1
    draw_floor()
    # sàn 1 sàn 2 luân phiên chạy liên tục
    if floor_x_pos <=-324:    
        floor_x_pos =0   
    pygame.display.update() 
    #fps  
    clock.tick(120)     
