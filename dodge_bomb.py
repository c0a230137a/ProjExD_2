import os
import random
import sys
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
    Rectオブジェクトが画面の中に収まっているかを判定する。
    引数：Rect（こうかとん or 爆弾）
    戻り値：真理値タプル（横方向、縦方向） - 画面内ならTrue、外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    爆弾の拡大サーフェスと加速度のリストを生成する。
    戻り値：
        - サイズに応じた爆弾Surfaceリスト（bb_imgs）
        - 各段階の加速度リスト（bb_accs）
    """
    bb_imgs = []  # 爆弾の画像リスト
    bb_accs = [a for a in range(1, 11)]  # 加速度リスト（1から10まで）
    
    for r in range(1, 11):  # 半径1から10までの爆弾画像を生成
        bb_img = pg.Surface((20 * r, 20 * r), pg.SRCALPHA)  # 透明なSurfaceを作成
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)  # 赤い円を描画
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs

def create_kk_img_dict() -> dict[tuple[int, int], pg.Surface]:
    """
    移動量タプルをキーに、回転させたこうかとん画像を値とした辞書を作成する。
    戻り値：
        dict[tuple[int, int], pg.Surface]: 各移動方向に対応した画像Surfaceの辞書
    """
    kk_base_img = pg.image.load("fig/3.png")  # 基本のこうかとん画像をロード
    kk_img_dict = {}  # 辞書を初期化

    # 移動量タプルのリスト
    directions = [
        (0, 0),  # 停止
        (0, -5),  # 上
        (0, +5),  # 下
        (-5, 0),  # 左
        (+5, 0),  # 右
        (-5, -5),  # 左上
        (+5, -5),  # 右上
        (-5, +5),  # 左下
        (+5, +5),  # 右下
    ]

    for direction in directions:
        if direction == (0, 0):  # 停止時は回転不要
            kk_img_dict[direction] = pg.transform.rotozoom(kk_base_img, 0, 0.9)
        else:
            angle = -pg.math.Vector2(direction).angle_to((1, 0))  # 角度を計算
            rotated_img = pg.transform.rotozoom(kk_base_img, angle, 0.9)
            kk_img_dict[direction] = rotated_img

    return kk_img_dict

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img_dict = create_kk_img_dict()  # 移動量に対応するこうかとん画像の辞書を生成
    kk_img = kk_img_dict[(0, 0)]  # 初期状態では移動なし
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_imgs, bb_accs = init_bb_imgs()  # 爆弾画像と加速度を生成
    bb_rct = bb_imgs[0].get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    vx, vy = +5, -5
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:  # ウィンドウの×ボタンが押された場合
                return

        screen.blit(bg_img, [0, 0])  # 背景画像を描画

        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾が衝突した場合
            print("ゲームオーバー")
            return

        key_lst = pg.key.get_pressed()  # 押されているキーを取得
        sum_mv = [0, 0]  # 合計移動量
        for key, tpl in DELTA.items():  # 押されたキーに応じた移動量を加算
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        kk_img = kk_img_dict[tuple(sum_mv)]  # 合計移動量タプルに応じた画像を取得
        kk_rct.move_ip(sum_mv)  # こうかとんを移動
        if check_bound(kk_rct) != (True, True):  # 画面外に出た場合
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 元の位置に戻す
        screen.blit(kk_img, kk_rct)  # こうかとんを描画

        # 爆弾の移動処理
        idx = min(tmr // 500, 9)  # 爆弾の段階的なサイズ変更（最大9段階）
        bb_rct.move_ip(vx * bb_accs[idx], vy * bb_accs[idx])  # 加速度を適用
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向ではみ出た場合
            vx *= -1  # 横方向の速度を反転
        if not tate:  # 縦方向ではみ出た場合
            vy *= -1  # 縦方向の速度を反転
        screen.blit(bb_imgs[idx], bb_rct)  # 爆弾を描画

        pg.display.update()  # 画面を更新
        tmr += 1  # タイマーを更新
        clock.tick(50)  # フレームレートを50FPSに設定

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()


