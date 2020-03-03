#!/usr/bin/env python
'''
===============================================================================
Grubcutを使ってイラストの顔パーツを手動で分割します。
USAGE:
    python grabcut_auto.py <画像ファイル名> 
    
README FIRST:
    1.入力ウィンドウと出力ウィンドウが開きます。
    2.入力ウィンドウ上で、抽出したい領域をマウスで矩形に囲みます。
    3.'n'を数回押すことによって前景抽出を行います。
    4.以下のキーを入力し、前景領域と背景領域をマウスによる描写で選択し、'n'を押すことで抽出したい部分を調整することができます。

Key '0' - 明確な背景領域をマウスで描写
Key '1' - 明確な前景領域をマウスで描写
Key '2' - 曖昧な背景領域をマウスで描写
Key '3' - 曖昧な前景領域をマウスで描写
Key 'n' - 前景抽出をアップデートする
Key 'r' - リセット
Key 's' - パーツ名を付けて保存
key 'q' - 終了
===============================================================================
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2 as cv
import sys
import os

class App():

    BLUE = [255,0,0]        # rectangle color
    RED = [0,0,255]         # PR BG
    GREEN = [0,255,0]       # PR FG
    BLACK = [0,0,0]         # sure BG
    WHITE = [255,255,255]   # sure FG

    DRAW_BG = {'color' : BLACK, 'val' : 0}
    DRAW_FG = {'color' : WHITE, 'val' : 1}
    DRAW_PR_FG = {'color' : GREEN, 'val' : 3}
    DRAW_PR_BG = {'color' : RED, 'val' : 2}

    # setting up flags
    rect = (0,0,1,1)
    drawing = False         # flag for drawing curves
    rectangle = False       # flag for drawing rect
    rect_over = False       # flag to check if rect drawn
    rect_or_mask = 100      # flag for selecting rect or mask mode
    value = DRAW_FG         # drawing initialized to FG
    thickness = 3           # brush thickness

    #マウス操作
    def onmouse(self, event, x, y, flags, param):
        # 領域抽出したい範囲をマウスで囲む
        if event == cv.EVENT_RBUTTONDOWN:
            self.rectangle = True
            self.ix, self.iy = x,y

        elif event == cv.EVENT_MOUSEMOVE:
            if self.rectangle == True:
                self.img = self.img2.copy()
                cv.rectangle(self.img, (self.ix, self.iy), (x, y), self.BLUE, 2)
                self.rect = (min(self.ix, x), min(self.iy, y), abs(self.ix - x), abs(self.iy - y))
                self.rect_or_mask = 0

        elif event == cv.EVENT_RBUTTONUP:
            self.rectangle = False
            self.rect_over = True
            cv.rectangle(self.img, (self.ix, self.iy), (x, y), self.BLUE, 2)
            self.rect = (min(self.ix, x), min(self.iy, y), abs(self.ix - x), abs(self.iy - y))
            self.rect_or_mask = 0
            print(" Now press the key 'n' a few times until no further change \n")

        # 前景・背景指定時のマウス操作

        if event == cv.EVENT_LBUTTONDOWN:
            if self.rect_over == False:
                print("first draw rectangle \n")
            else:
                self.drawing = True
                #描写
                cv.circle(self.img, (x,y), self.thickness, self.value['color'], -1)
                cv.circle(self.mask, (x,y), self.thickness, self.value['val'], -1)

        elif event == cv.EVENT_MOUSEMOVE:
            if self.drawing == True:
                #描写
                cv.circle(self.img, (x, y), self.thickness, self.value['color'], -1)
                cv.circle(self.mask, (x, y), self.thickness, self.value['val'], -1)

        elif event == cv.EVENT_LBUTTONUP:
            if self.drawing == True:
                self.drawing = False
                #描写
                cv.circle(self.img, (x, y), self.thickness, self.value['color'], -1)
                cv.circle(self.mask, (x, y), self.thickness, self.value['val'], -1)

    def run(self):
        # コマンド引数で画像ファイル名を指定した場合
        if len(sys.argv) == 2:
            filename = sys.argv[1] # for drawing purposes
            workDir = filename[:filename.rfind(".")]
            if not os.path.exists(workDir):
                os.mkdir(workDir)

        else:
            print("No input image given, so loading default image, lena.jpg \n")
            print("Correct Usage: python grabcut.py <filename> \n")
            filename = 'test.png'


        #画像読み込み
        self.img = cv.imread(cv.samples.findFile(filename))
        self.img2 = self.img.copy()                               # a copy of original image
        self.mask = np.zeros(self.img.shape[:2], dtype = np.uint8) # mask initialized to PR_BG
        self.output = np.zeros(self.img.shape, np.uint8)           # output image to be shown
        self.rect_or_mask = 0
       
        self.rect_over = True
        print(" Now press the key 'n' a few times until no further change \n")
        # 入力ウィンドウと出力ウィンドウの表示
        cv.namedWindow('output', cv.WINDOW_NORMAL)
        cv.namedWindow('input', cv.WINDOW_NORMAL)
        cv.setMouseCallback('input', self.onmouse)
        cv.moveWindow('input', self.img.shape[1]+10,90)

        print(" Instructions: \n")
        print(" Draw a rectangle around the object using right mouse button \n")

        while(1):

            cv.imshow('output', self.output)
            cv.imshow('input', self.img)
            k = cv.waitKey(1)

            # key bindings
            if k == 27:         # esc to exit
                break
            elif k == ord('q'): #終了
                break
            elif k == ord('0'): # BG drawing
                print(" mark background regions with left mouse button \n")
                self.value = self.DRAW_BG
            elif k == ord('1'): # FG drawing
                print(" mark foreground regions with left mouse button \n")
                self.value = self.DRAW_FG
            elif k == ord('2'): # PR_BG drawing
                self.value = self.DRAW_PR_BG
            elif k == ord('3'): # PR_FG drawing
                self.value = self.DRAW_PR_FG
            elif k == ord('s'): # save image
                
                bgr = cv.split(self.output)
                bgra = bgr + [mask2]
                self.output_alpha = cv.merge(bgra)
                
                img_g = cv.cvtColor(self.output_alpha, cv.COLOR_BGR2GRAY)#グレースケールへ変換
                x, y, w, h = cv.boundingRect(img_g)

                print("パーツ名:")
                parts = input()

                #顔パーツ保存
                img_key_name = filename.split(".",1)[0] + "_" + parts + ".png"
                cv.imwrite(img_key_name,self.output_alpha[y:y+h,x:x+w])
                
                cv.imwrite(filename.rstrip('.png') + '_mask.png', mask2)#マスク保存

                #マスク部分を切り取り、画像補填      
                #dst = cv.inpaint(self.img2, mask2, 50, cv.INPAINT_TELEA)
                #cv.imwrite(filename.rstrip('.png') + '_' + 'inpaint.png', dst)
                print(" Result saved as image \n")

            elif k == ord('r'): # reset everything
                print("resetting \n")
                self.rect = (0,0,1,1)
                self.drawing = False
                self.rectangle = False
                self.rect_or_mask = 100
                self.rect_over = False
                self.value = self.DRAW_FG
                self.img = self.img2.copy()
                self.mask = np.zeros(self.img.shape[:2], dtype = np.uint8) # mask initialized to PR_BG
                self.output = np.zeros(self.img.shape, np.uint8)           # output image to be shown
            elif k == ord('n'): # segment the image
                print(""" For finer touchups, mark foreground and background after pressing keys 0-3
                and again press 'n' \n""")
                try:
                    if (self.rect_or_mask == 0):         # grabcut with rect
                        bgdmodel = np.zeros((1, 65), np.float64)
                        fgdmodel = np.zeros((1, 65), np.float64)
                        cv.grabCut(self.img2, self.mask, self.rect, bgdmodel, fgdmodel, 1, cv.GC_INIT_WITH_RECT)
                        self.rect_or_mask = 1
                    elif self.rect_or_mask == 1:         # grabcut with mask
                        bgdmodel = np.zeros((1, 65), np.float64)
                        fgdmodel = np.zeros((1, 65), np.float64)
                        cv.grabCut(self.img2, self.mask, self.rect, bgdmodel, fgdmodel, 1, cv.GC_INIT_WITH_MASK)
                except:
                    import traceback
                    traceback.print_exc()

            mask2 = np.where((self.mask==1) + (self.mask==3), 255, 0).astype('uint8')
            
            self.output = cv.bitwise_and(self.img2, self.img2, mask=mask2)
            
             
        print('Done')

        

if __name__ == '__main__':
    print(__doc__)
    App().run()
    cv.destroyAllWindows()
