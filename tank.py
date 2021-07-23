# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import random
  
import enemy_base
import enemyAttack


(w, h) = (1000, 800)   # 画面サイズ
(x, y) = (w/2, h/2)
speed = 1  # 戦車の移動速度
size = 20  # 戦車の大きさ
block_size = 40  # ブロックの大きさ
hit = [4]  # 物に当たっているかの判定
bullet = []  # 弾丸の位置を記録する配列
bullet_way = []  # 弾丸の向きを記録する配列
bullet_speed = 7  # 弾丸の速さ
block = []  # ブロックの位置を記録する配列
e_size=30
situation = 0

for i in range(20):
        block.append(0)
        block.append(i)
for i in range(25):
    block.append(i)
    block.append(0)
for i in range(25):
    block.append(24)
    block.append(i)
for i in range(25):
    block.append(i)
    block.append(19)

    hit = []
    bullet = []
    for i in range(4):
        hit.append(1)

field_block = [7, 7, 8, 8, 7, 8, 8, 7, 9, 8, 9, 7, 10, 8, 10, 7,
               20, 17, 20, 16, 20, 15, 20, 14 , 20, 20, 20, 19, 20, 18, 7, 24,7, 23, 7, 22, 7, 21, 7, 20, 7, 19, 7, 18, 7, 17, 7, 16, 18, 1, 18, 2, 18, 3, 18, 4, 18, 5, 18, 6, 18, 7]  # フィールド上にあるブロックの位置
# field_blockに書いたフィールド内にあるブロックの位置情報をblockにコピーする
for i in range(int(len(field_block)/2)):
    block.append(field_block[2*i])
    block.append(field_block[2*i+1])


# ブロックの当たり判定を行う関数
def block_hit(x, y, a, b):  # (戦車の座標,ブロックの座標(block_sizeで割ったもの))
    left = 1
    right = 1
    up = 1
    down = 1
    if(((x < a*block_size+block_size) & (a*block_size < x+size)) & ((y < b*block_size+block_size) & (b*block_size < y+size))):
        if((a*block_size+block_size < x+size)):
            left = 0
            x = a*block_size+block_size

        elif((x < a*block_size)):
            right = 0
            x = a*block_size-size
        elif(b*block_size+block_size < y+size):
            up = 0
            y = b*block_size+block_size
        elif(y < b*block_size):
            down = 0
            y = b*block_size-size
    hit = [left, right, up, down, x, y]  # 返り値として左右と上下の当たり判定(0，1)と戦車の位置を返す
    return hit


# ブロックの中に入り込まないようにするための関数

def block_hit3(x, y):  # 角のすり抜けバグ防止用関数
    if ((x+size > 1000-block_size) & (y+size > 1000-block_size)):
        x = 1000-block_size-size
        y = 1000-block_size-size
    if ((x < block_size) & (y < block_size)):
        x = block_size
        y = block_size
    if ((x+size > 1000-block_size) & (y < block_size)):
        x = 1000-block_size-size
        y = block_size
    if ((x < block_size) & (y+size > 1000-block_size)):
        x = block_size
        y = 1000-block_size-size
    return [x, y]


def block_draw(x, y):  # ブロックの描写
    edge = 40
    screen = pygame.display.get_surface()
    pygame.draw.rect(screen, (0, 200, 0), (x*edge, y*edge, block_size, block_size), width=0)
    return None


def shot(x, y):  # 弾丸を描く関数
    screen = pygame.display.get_surface()
    pygame.draw.circle(screen, (210, 10, 10), (x, y), 10, width=0)
    return (x+1, y+1)


def enemy_shot(x, y):  # 弾丸を描く関数
    screen = pygame.display.get_surface()
    pygame.draw.circle(screen, (10, 10, 10), (x, y), 10, width=0)
    return (x+1, y+1)
  
def hp_(a): #HPゲージを描画する関数
    screen = pygame.display.get_surface()
    b=100-a
    pygame.draw.line(screen, (0) , (700+200-b*2,20) ,(700+200,20),width=20)
    pygame.draw.line(screen, (255,255,0) , (700,20) ,(700+a*2,20),width=20)
    pygame.draw.line(screen, (0) , (700,10) ,(700+200,10),width=1)
    pygame.draw.line(screen, (0) , (700,30) ,(700+200,30),width=1)
    pygame.draw.line(screen, (0) , (700,10) ,(700,30),width=1)
    pygame.draw.line(screen, (0) , (700+200,10) ,(700+200,30),width=1)
    

            
e_hp=[100,100,100,100]   #敵四体のHP         
            
def bullet_hit_enemy(bullet): #弾が敵に当たった時の処理 HPを減らして弾を消す
  situation=1
  e_x=enemy_base.x
  e_y=enemy_base.y
  b=-1
  for i in range(int(len(bullet)/2)):
    for j in range(int(len(e_x))):
      if ((bullet[2*i] >e_x[j]) & (bullet[2*i] <e_x[j]+e_size) & (bullet[2*i+1] > e_y[j]) & (bullet[2*i+1] < e_y[j]+e_size)):
        e_hp[j]-=10
        if(e_hp[j]<0):
          b=j
        else:
          b=-1
    if b!=-1:
      del enemy_base.x[b]   
      del enemy_base.y[b]
      b=-1
  if(len(enemy_base.x)==0):
    print(  "You win")
    situation = 3
  return situation
    #pygame.quit()
    #sys.exit()
    

    
  


def main():
    (x, y) = (w/2, h/2)
    pygame.init()       # pygame初期化
    pygame.display.set_mode((w, h), 0, 32)  # 画面設定
    screen = pygame.display.get_surface()
    key = 0
    last_key = 0
    count = 0
    t = 0
    t_stop = 0
    speed = 0
    stop_speed = 0
    power_left = 1  
    power_right = 1
    power_up = 1
    power_down = 1
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(loops=-1, start=0.0)
    hit=[1,1,1,1,x,y]
    
    situation = 0 #（0ならタイトル画面　1ならプレイ画面）

    while (1):

        #タイトル画面（
        if situation == 0:
            font1 = pygame.font.SysFont(None,150)
            font2 = pygame.font.SysFont(None,75)
            text1 = font1.render("2D TANK GAME",True,(0,255,0))
            text2 = font2.render("PRESS SPACE",True,(255,0,0))
            screen.fill((0,0,0)) 
            screen.blit(text1,(120,300))
            screen.blit(text2,(300,600))
            pygame.display.update()
            if pygame.key.get_pressed()[K_SPACE]:  #スペースキーが押されたらプレイ画面に移動
                situation = 1
                pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:          # 閉じるボタンが押されたとき
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:       # キーを押したとき
                    if event.key == K_ESCAPE:   # Escキーが押されたとき
                        pygame.quit()
                        sys.exit()

        if situation == 1: #追加
            enemy_base.control(screen, x, y, block)  # 敵の行動管理関数(screen,プレイヤーの座標)

            # 戦車の移動処理の開始
            pressed_key = pygame.key.get_pressed()
            if speed == 0:
                if pressed_key[K_a]:
                    power_left = 1
                if pressed_key[K_d]:
                    power_right = 1
                if pressed_key[K_w]:
                    power_up = 1
                if pressed_key[K_s]:
                    power_down = 1

            if(pressed_key[K_a] or pressed_key[K_s] or pressed_key[K_d] or pressed_key[K_w]):       # キーを押したとき
                t += 0.1  # 時間の計測を始める
                t_stop = 0

            else:  # 戦車が動いていてかつ速度があるときに慣性を使うためにt_stopの計測を始める。
                if speed > 0:
                    t_stop += 0.01
                else:  # 速度が０でキーも押されてないときに初期化
                    t = 0
                    speed = 0
                    power_left = 1
                    power_right = 1
                    power_up = 1
                    power_down = 1

            speed = 20*t*t+1*t-18*t_stop*t_stop  # 移動速度の計算
            if(speed > 7):  # 最高速度の設定
                speed = 7

            # 速度がどの横行に向いているのかを計算して、なめらかな方向転換を実現
            # 処理開始
            if pressed_key[K_a]:
                power_left += 0.1
                last_key = 2
            elif(power_left > 1):
                power_left -= 0.1
            if pressed_key[K_d]:
                power_right += 0.1
                last_key = 3
            elif(power_right > 1):
                power_right -= 0.1
            if pressed_key[K_w]:
                power_up += 0.1
                last_key = 0
            elif(power_up > 1):
                power_up -= 0.1
            if pressed_key[K_s]:
                power_down += 0.1
                last_key = 1
            elif(power_down > 1):
                power_down -= 0.1
            # 処理終了

            x -= speed*hit[0]*power_left / \
                (power_left+power_right+power_up+power_down)  # 実際の位置の計算
            x += speed*hit[1]*power_right / \
                (power_left+power_right+power_up+power_down)
            y -= speed*hit[2]*power_up/(power_left+power_right+power_up+power_down)
            y += speed*hit[3]*power_down / \
                (power_left+power_right+power_up+power_down)
            # 戦車の移動処理の終了

            # 弾丸系の処理開始
            if pressed_key[K_SPACE]:
                key = 1
            elif key == 1:
                count += 1
                key = 0
                bullet.append(x+size/2)
                bullet.append(y+size/2)
                bullet_way.append(last_key)
            if(count > 0):
                for i in range(int(len(bullet)/2)):  # count
                    shot(bullet[2*i], bullet[2*i+1])  # 弾丸の描写
                    # 弾丸の位置の移動
                    if(bullet_way[i] == 0):
                        bullet[2*i+1] -= bullet_speed
                    elif(bullet_way[i] == 1):
                        bullet[2*i+1] += bullet_speed
                    elif(bullet_way[i] == 2):
                        bullet[2*i] -= bullet_speed
                    elif(bullet_way[i] == 3):
                        bullet[2*i] += bullet_speed

                deleted_bullet = []
                for j in range(int(len(block)/2)):  # 弾丸の当たり判定処理
                    for i in range(int(len(bullet)/2)):
                        if ((bullet[2*i] > block[2*j]*block_size) & (bullet[2*i] < block[2*j]*block_size+block_size) & (bullet[2*i+1] > block[2*j+1]*block_size) & (bullet[2*i+1] < block[2*j+1]*block_size+block_size)):
                            deleted_bullet.append(i)
                for i in range(len(deleted_bullet)):  # 重くならないように消えた弾丸のデータは削除
                    del bullet[2*i]
                    del bullet[2*i]
                    del bullet_way[i]
            # 弾丸系の処理終了

            block_length = int(len(block)/2)

            for i in range(block_length):
                # ブロックの当たり判定
                hit = block_hit(x, y, block[2*i], block[2*i+1])
                x = hit[4]
                y = hit[5]
                if(hit[0] == 0):
                    x = block_hit3(x, y)[0]
                    break
                if(hit[1] == 0):
                    x = block_hit3(x, y)[0]
                    break
            for i in range(block_length):
                hit = block_hit(x, y, block[2*i], block[2*i+1])  # ブロックの当たり判定
                if(hit[2] == 0):
                    y = block_hit3(x, y)[1]
                    break
                if(hit[3] == 0):
                    y = block_hit3(x, y)[1]
                    break
            for i in range(block_length):  # ブロックの描写
                block_draw(block[2*i], block[2*i+1])
            
            situation=enemyAttack.hp_drow()
            if(situation!=2):   
                situation=bullet_hit_enemy(bullet) 
            

            pygame.display.update()     # 画面更新
            pygame.time.wait(10)        # 更新時間間隔
            screen.fill(color=(222, 184, 135))  # 画面の背景色
            pygame.draw.rect(screen, (255, 0, 0),(x, y, size, size), width=0)  # 戦車の描画

            # 終了用のイベント処理
            for event in pygame.event.get():
                if event.type == QUIT:          # 閉じるボタンが押されたとき
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:       # キーを押したとき
                    if event.key == K_ESCAPE:   # Escキーが押されたとき
                        pygame.quit()
                        sys.exit()
                
        if situation == 2: #ゲームオーバー
            font3 = pygame.font.SysFont(None,200)
            text3 = font3.render("GAME OVER",True,(255,0,0))
            screen.fill((0,0,0))
            screen.blit(text3,(80,300))
            pygame.mixer.music.pause()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:          # 閉じるボタンが押されたとき
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:       # キーを押したとき
                    if event.key == K_ESCAPE:   # Escキーが押されたとき
                        pygame.quit()
                        sys.exit()
                # if event.type == KEYDOWN:       # キーを押したとき
                    # if event.key == K_SPACE:   # SPACEキーが押されたとき
                        # pygame.quit()
                        # sys.exit()
                    
        if situation == 3:
            font4 = pygame.font.SysFont(None,160)
            text4 = font4.render("GAME CLEAR!!",True,(0,0,255))
            screen.fill((0,0,0))
            screen.blit(text4,(80,300))
            pygame.display.update()
            pygame.mixer.music.pause()
            for event in pygame.event.get():
                if event.type == QUIT:          # 閉じるボタンが押されたとき
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:       # キーを押したとき
                    if event.key == K_ESCAPE:   # Escキーが押されたとき
                        pygame.quit()
                        sys.exit()
                # if event.type == KEYDOWN:       # キーを押したとき        #画面切り替え時間違えて押しちゃうから無効にしたほうがいいかも？
                    # if event.key == K_SPACE:   # SPACEキーが押されたとき
                        # pygame.quit()
                        # sys.exit()

if __name__ == "__main__":
    main()
