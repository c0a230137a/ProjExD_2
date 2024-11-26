import os
import random
import sys
import pygame as pg



WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, 5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (5, 0),
    }
def check_bound(obj_rct):
    """
    引数：Rectオブジェクト
    戻り値：横方向・縦方向の真理値タプル（True：画面内／False：画面外）
    """
    x_within = (0 <= obj_rct.left) and (obj_rct.right <= WIDTH)
    y_within = (0 <= obj_rct.top) and (obj_rct.bottom <= HEIGHT)
    return x_within, y_within


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr =0
    # Create bomb surface
    bb_img = pg.Surface((20, 20)) #爆弾用の空SurFace
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い円を描画
    bb_img.set_colorkey((0, 0, 0))  # 黒を透明に設定
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # ランダムな位置に配置

    vx, vy = 5, 5
        


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        kk_rct.move_ip(sum_mv)
        #練習3
        yoko, tate = check_bound(kk_rct)
        if not yoko:  # 横方向が画面外の場合
            kk_rct.left = max(0, kk_rct.left)
            kk_rct.right = min(WIDTH, kk_rct.right)
        if not tate:  # 縦方向が画面外の場合
            kk_rct.top = max(0, kk_rct.top)
            kk_rct.bottom = min(HEIGHT, kk_rct.bottom)

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向が画面外の場合
            vx = -vx
        if not tate:  # 縦方向が画面外の場合
            vy = -vy
        
        # 衝突判定
        if kk_rct.colliderect(bb_rct):  # 衝突していたら
            print("衝突しました！ゲームを終了します。")
            return  # main関数を終了

        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
