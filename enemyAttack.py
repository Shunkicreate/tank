# -*- coding: utf-8 -*-
#これ単品では動きません。enemy_base.pyからimportしてください

#このファイルの関数を実行する上で必要なモジュール
import pygame
from pygame.locals import *
import sys
import math
import tank
import enemy_base
import time

e_bullet = []
bullet_wayx = []
bullet_wayy = []
bullet_number = 0
bvx = [0] * 10 #循環参照となるのでリストの個数は定数で指定(敵の数は最大10)
bvy = [0] * 10
bullet_speed = 3
size=20
e_size=30
hp=[100]



def do(px,py,ex,ey,n):#射撃(プレイヤーの座標、敵の座標,処理を行う敵の番号)
    e_bullet.append(enemy_base.x[n]+enemy_base.size[n]/2)
    e_bullet.append(enemy_base.y[n]+enemy_base.size[n]/2)
    enemy_base.p_betweentwo(px,py,n,ex,ey,bvx,bvy)
    bullet_wayx.append(bvx[n])
    bullet_wayy.append(bvy[n])
    
def e_bullet_draw():
    for k in range(int(len(e_bullet)/2)):
        tank.enemy_shot(e_bullet[2*k],e_bullet[2*k+1]) #弾の描写
        e_bullet[2*k]+=bullet_wayx[k]*bullet_speed
        e_bullet[2*k+1]+=bullet_wayy[k]*bullet_speed
    
        
def e_bullet_hit_block():#弾とブロックが当たった時の当たり判定
    b=[]
    for j in range(int(len(tank.block)/2)):
        for i in range(int(len(e_bullet)/2)):
            if ((e_bullet[2*i]>tank.block[2*j]*tank.block_size)&(e_bullet[2*i]<tank.block[2*j]*tank.block_size+tank.block_size)&(e_bullet[2*i+1]>tank.block[2*j+1]*tank.block_size)&(e_bullet[2*i+1]<tank.block[2*j+1]*tank.block_size+tank.block_size)):
                b.append(i)
    for i in range (len(b)):
        del e_bullet[i*2]
        del e_bullet[i*2]
        del bullet_wayx[i]
        del bullet_wayy[i]
    
def e_bullet_hit_player(px,py):#弾がプレイヤーに当たった時の処理 HPを減らしてゼロになったら終了する
    b=[]
    for i in range(int(len(e_bullet)/2)):
        if((e_bullet[2*i]>px)&(e_bullet[2*i]<px+size)&(e_bullet[2*i+1]>py)&(e_bullet[2*i+1]<py+size)):
            b.append(i)
            hp[0]-=5
    for i in range (len(b)):
        del e_bullet[i*2]
        del e_bullet[i*2]
        del bullet_wayx[i]
        del bullet_wayy[i]
        
def hit_enemy(px,py,x,y): #プレイヤーと敵が当たった時の処理
    for i in range(len(x)):
        if(((x[i]<px+size) & (x[i]+e_size > px)) & ((y[i] < py+size) & (y[i]+e_size> py))):
            hp[0]-=3
            
def hp_drow(): #HPゲージの描画
    tank.hp_(hp[0])
    situation = 1
    if(hp[0]<=0):
        situation = 2
        print("You lose")
    return situation
    #pygame.quit()
    #sys.exit()

 