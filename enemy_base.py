# -*- coding: utf-8 -*-
#これ単品では動きません。tank.pyからimportしてください

#このファイルの関数を実行する上で必要なモジュール
import pygame
from pygame.locals import *
import os
import sys
import random
import math
import tank
# import enemyRoute
# import enemyAvoid
import enemyAttack

#敵の初期パラメータ設定
x = [100,850,100,850] 
y = [200,200,750,750] #敵座標
vx = [0.5,  1, -1,   1]
vy = [0.5,  2,0.6,-0.5] #敵の動き方
gx = [0] * len(x)
gy = [0] * len(x) #目的地の座標
size = [30] * len(x) #大きさ
e_bullets=[]
e_bullet=[]
bullet_wayx=[]
bullet_wayy=[]

root_dir = os.getcwd() #他のファイルを利用するために絶対パスを取得(主に画像読み込み用)

#移動に関する管理を行う変数　enemyRoute,enemyAvoidに適用
domove=[False] * len(x)
WAIT=False
MOVE=True
#敵を攻撃するか判定する変数　enemyAttackに適用
canaim=[False] * len(x)

count=[0] * len(x) #timecount,弾の時間カウント用
limit=[0] * len(x) #timecount,移動の制限時間セット用

def draw(screen):  #敵の描画
    for i in range(len(x)):
        pygame.draw.rect(screen,(0,0,255),(x[i],y[i],size[i],size[i]), width=0) #戦車の描画

def timecount(interval,time,i): #while文内で機能するタイマー関数(時間間隔,利用するリスト,実行する敵の番号)
    if(time[i]==interval):
       time[i]=0
       return True
    else:
        time[i]+=1
        return False

def p_betweentwo(px,py,i,ex,ey,dx,dy): #二つの座標からx軸方向とy軸方向の変化の割合(敵→プレイヤー)を抽出(プレイヤーの座標、敵の番号敵の座標、変化の割合の格納先)
    #プレイヤー=目的地と考えることでルート決定にも使用可
    den = ((px-ex[i])**2+(py-ey[i])**2)**0.5
    dx[i] = (px-ex[i]) / den
    dy[i] = (py-ey[i]) / den


def canshot(px,py,x,y): #次の行動を判断(プレイヤーの座標,敵の座標)
    #射線が通るかをプレイヤーと敵の座標を結んだ直線上の色から判断、現時点では未完成
    # vx = math.cos(float(x))

    return True

def control(screen,px,py,block): #敵の行動管理(screen,プレイヤーの座標)
    
    for i in range(len(x)):
        if(domove[i]==MOVE): #移動の判定 
            x[i]+=vx[i]
            y[i]+=vy[i]
            if((x[i]==gx[i])&(y[i]==gy[i])): #目的地に到着したらWAIT
               domove[i]==WAIT
            if(timecount(2000,limit,i)): #時間内にたどりつけないならWAIT
               domove[i]==WAIT
        else: 
            #enemyRoute
            #enemyAvoid
            domove[i]=MOVE

        canaim[i]=canshot(px,py,x,y)
        if(canaim[i]): #攻撃できるか判定
            if(timecount(200,count,i)):
                enemyAttack.do(px,py,x,y,i)
    
    enemyAttack.e_bullet_hit_block()
    enemyAttack.e_bullet_hit_player(px,py)
    enemyAttack.hit_enemy(px,py,x,y)
    enemyAttack.e_bullet_draw()

    for i in range(int(len(tank.block)/2)):
        for j in range (len(x)):
            hit=tank.block_hit(x[j],y[j],block[2*i], block[2*i+1])
            x[j]=hit[4]
            y[j]=hit[5]
            
            if(hit[0]==0):
                vx[j]=-vx[j]
            if(hit[1]==0):
                vx[j]=-vx[j]
            if(hit[2]==0):
                vy[j]=-vy[j]
            if(hit[3]==0):
                vy[j]=-vy[j]
    draw(screen)     #敵の描写    
        

