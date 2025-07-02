import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
STONE_INTERBVAL =30 #フレームの更新ごとに石が増えないように。（1秒に1つ石が増える）
GAME_OVER_DISPLAY_TIME = 60
START_SCENE = "start"
PLAY_SCENE = "play"

#　参考：https://www.youtube.com/watch?v=0g0L5iGKv9g&t=404s

class Stone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    #下の石の処理と同じ
    def update(self):
        if self.y < SCREEN_HEIGHT:
            self.y += 1

    #下の石の表示に関する処理と同じ
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, 8, 8, pyxel.COLOR_BLACK) 

        

class App:
    def __init__(self): # init関数とrun関数の間に処理や定義を書く 
        pyxel.init(160, 120, title="Nゲーム") #ゲーム画面の幅・高さ・タイトル
        pyxel.mouse(True)
        pyxel.load("my_resource.pyxres")
        pyxel.playm(0, loop=True)
        self.current_scene =  START_SCENE
        pyxel.run(self.update, self.draw) #run関数で自動的で
    
    def reset_play_scene(self):
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT * 4 // 5
        self.stones = [] #ストーンオブジェクトを複数持っているストーンズというリストをインスタンス変数として定義
        self.is_collision = False #雪が当たった状態 初期は当たっていないのでfalse
        self.game_over_display_timer = GAME_OVER_DISPLAY_TIME #ゲームオーバーになったときに2秒後に画面遷移
        

    def update_start_scene(self): # スタート画面のフレーム更新時の処理を書くメソッド
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.reset_play_scene()
            self.current_scene = PLAY_SCENE

    def update_play_scene(self): 
        #ゲームオーバー時

        if self.is_collision:
            if self.game_over_display_timer > 0:
                self.game_over_display_timer -= 1
            else:
               self.current_scene = START_SCENE
            return

        # プレイヤーの移動    
        if pyxel.btn(pyxel.KEY_RIGHT) and self.player_x < SCREEN_WIDTH -12: #btn；押され続けている　btnp:押した瞬間
            self.player_x += 1
        elif pyxel.btn(pyxel.KEY_LEFT) and self.player_x > -4:
            self.player_x -= 1
        
        #石の追加と初期位置
        if pyxel.frame_count % STONE_INTERBVAL == 0:
            self.stones.append(Stone(pyxel.rndi(0, SCREEN_WIDTH -8),0))
        
        #雪の落下　for文でリストストーンを回して取り出したstoneオブジェクトのupdateメソッドを呼び出す
        for stone in self.stones.copy():
            stone.update()

            #衝突        
            if (self.player_x <= stone.x <= self.player_x +8 and
                self.player_y <= stone.y <= self.player_y +8):
                self.is_collision = True

            #　画面外に出た石を削除
            if stone.y >= SCREEN_HEIGHT:
                self.stones.remove(stone)  


    def update(self): #フレーム。pythonでは一秒間に30回FPS。ユーザーからの操作を受け取る。
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        if self.current_scene == START_SCENE:
            self.update_start_scene()
        elif self.current_scene == PLAY_SCENE:
            self.update_play_scene()

    def draw_start_scene(self):
        pyxel.blt(0, 0, 0, 32, 0, 160, 120)
        pyxel.text(SCREEN_WIDTH //3, SCREEN_WIDTH //10,
                   "Click to Start", pyxel.COLOR_PINK)
     
    def draw_play_scene(self):
        pyxel.cls(pyxel.COLOR_DARK_BLUE) #背景 
        
        #リストからストーンオブジェクトを一つずつ取り出してdrowメソッドを呼び出す
        for stone in self.stones:
            stone.draw()
        
        #プレイヤーwを表示させる
        pyxel.blt(self.player_x, self.player_y, 0, 16, 0, 16, 16, pyxel.COLOR_BLACK) 

        if self.is_collision:
            pyxel.text(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2, 
                       "GAME OVER", pyxel.COLOR_YELLOW)

    def draw(self):
        if self.current_scene == START_SCENE:
            self.draw_start_scene()
        elif self.current_scene == PLAY_SCENE:
            self.draw_play_scene()
        
        

App()