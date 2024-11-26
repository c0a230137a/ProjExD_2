import os
import random
import sys
import time
import pygame as pg

# 定数定義
WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとん または 爆弾のRect
    戻り値：真理値タプル（横判定結果、縦判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    爆弾の拡大サーフェスと加速度のリストを返す
    """
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]  # 加速度リスト（1から10まで）
    
    for r in range(1, 11):  # 半径1から10までの爆弾画像を生成
        bb_img = pg.Surface((20 * r, 20 * r), pg.SRCALPHA)
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_imgs.append(bb_img)
    
    return bb_imgs, bb_accs

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    # 爆弾の拡大サーフェスと加速度を生成
    bb_imgs, bb_accs = init_bb_imgs()

    bb_rct = bb_imgs[0].get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    
    vx, vy = +5, -5
    gob_img = pg.Surface((1100, 650))  # 画面全体サイズ(1100x650)のSurfaceを作成
    gob_img.set_alpha(128)  # Surfaceの透明度を128に設定（半透明）
    pg.draw.rect(gob_img, (0, 0, 0), pg.Rect(0, 0, 800, 1600))  # gob_img上に黒色の矩形を描画
     # (0, 0)は矩形の左上座標、(800, 1600)は矩形の幅と高さを指定
    fonto = pg.font.Font(None, 80)  # フォントオブジェクトを作成（デフォルトフォント、サイズ80）
    txt = fonto.render("GameOver", True, (255, 255, 255))# "GameOver"という文字列を描画するためのSurfaceを作成（白色文字)
    cry_kk_img = pg.image.load("fig/8.png")

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾が重なっていたら
            screen.blit(gob_img, (0, 0))
            screen.blit(txt, [420, 280])
            screen.blit(cry_kk_img, (360, 280))
            screen.blit(cry_kk_img, (730, 280))
            pg.display.flip()
            time.sleep(5)
            return

        # 指定された呼び出し形式を適用
        bb_imgs, bb_accs = init_bb_imgs()
        avx = vx * bb_accs[min(tmr // 500, 9)]
        bb_img = bb_imgs[min(tmr // 500, 9)]

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        avy = vy * bb_accs[min(tmr // 500, 9)]  # 加速度変更後に適用
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横にはみ出てる
            vx *= -1
        if not tate: # 縦にはみ出てる
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
