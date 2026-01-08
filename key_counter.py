import tkinter as tk
from tkinter import ttk
from pynput.keyboard import Listener, Key
import threading

class KeyCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Key Counter")
        self.root.geometry("420x630")
        self.root.resizable(False, False)
        
        # 배경색 설정 
        self.root.configure(bg="#F8F9FA")
        
        # 변수 초기화
        self.target_key = None
        self.count = 0
        self.is_counting = False
        self.listener = None
        self.key_pressed = False
        
        # 색상 테마
        self.colors = {
            'bg': '#F8F9FA',
            'card': '#FFFFFF',
            'primary': '#4A90E2',
            'primary_hover': '#357ABD',
            'success': '#52C41A',
            'danger': '#FF4D4F',
            'text_primary': '#1A1A1A',
            'text_secondary': '#666666',
            'border': '#E8E8E8',
            'count_bg': '#F0F7FF'
        }
        
        # UI 구성
        self.setup_ui()
        
    def setup_ui(self):
        # 메인 컨테이너
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # 헤더 섹션
        header_frame = tk.Frame(main_container, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 12))
        
        # 타이틀
        title_label = tk.Label(header_frame, 
                              text="Key Counter",
                              font=("Segoe UI", 20, "bold"),
                              fg=self.colors['text_primary'],
                              bg=self.colors['bg'])
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame,
                                 text="실시간 키 연타 횟수 측정",
                                 font=("Segoe UI", 9),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['bg'])
        subtitle_label.pack(pady=(2, 0))
        
        # 키 선택 카드
        key_card = tk.Frame(main_container, bg=self.colors['card'], 
                           relief=tk.FLAT, bd=0)
        key_card.pack(fill=tk.X, pady=(0, 10))
        self._add_shadow(key_card)
        
        key_inner = tk.Frame(key_card, bg=self.colors['card'])
        key_inner.pack(padx=15, pady=12)
        
        key_label = tk.Label(key_inner,
                           text="측정할 키 선택",
                           font=("Segoe UI", 10, "bold"),
                           fg=self.colors['text_primary'],
                           bg=self.colors['card'])
        key_label.pack(anchor=tk.W)
        
        self.key_button = tk.Button(key_inner,
                                    text="키를 선택하려면 클릭하세요",
                                    font=("Segoe UI", 10, "bold"),
                                    bg=self.colors['primary'],
                                    fg="white",
                                    activebackground=self.colors['primary_hover'],
                                    activeforeground="white",
                                    relief=tk.FLAT,
                                    cursor="hand2",
                                    padx=15,
                                    pady=8,
                                    command=self.set_target_key)
        self.key_button.pack(fill=tk.X, pady=(6, 6))
        
        self.selected_key_label = tk.Label(key_inner,
                                          text="선택된 키: 없음",
                                          font=("Segoe UI", 9, "bold"),
                                          fg=self.colors['text_secondary'],
                                          bg=self.colors['card'])
        self.selected_key_label.pack()
        
        # 카운트 디스플레이 카드
        count_card = tk.Frame(main_container, bg=self.colors['count_bg'],
                            relief=tk.FLAT, bd=0)
        count_card.pack(fill=tk.X, pady=(0, 10))
        self._add_shadow(count_card)
        
        count_inner = tk.Frame(count_card, bg=self.colors['count_bg'])
        count_inner.pack(padx=15, pady=20)
        
        count_title = tk.Label(count_inner,
                             text="연타 횟수",
                             font=("Segoe UI", 10, "bold"),
                             fg=self.colors['text_secondary'],
                             bg=self.colors['count_bg'])
        count_title.pack()
        
        self.count_label = tk.Label(count_inner,
                                   text="0",
                                   font=("Segoe UI", 44, "bold"),
                                   fg=self.colors['primary'],
                                   bg=self.colors['count_bg'])
        self.count_label.pack(pady=(2, 2))
        
        count_unit = tk.Label(count_inner,
                            text="회",
                            font=("Segoe UI", 11, "bold"),
                            fg=self.colors['text_secondary'],
                            bg=self.colors['count_bg'])
        count_unit.pack()
        
        # 컨트롤 버튼 섹션
        control_frame = tk.Frame(main_container, bg=self.colors['bg'])
        control_frame.pack(fill=tk.X, pady=(0, 8))
        
        button_container = tk.Frame(control_frame, bg=self.colors['bg'])
        button_container.pack()
        
        self.start_button = tk.Button(button_container,
                                      text="▶  시작",
                                      font=("Segoe UI", 11, "bold"),
                                      bg=self.colors['success'],
                                      fg="white",
                                      activebackground="#45A317",
                                      activeforeground="white",
                                      relief=tk.FLAT,
                                      cursor="hand2",
                                      padx=20,
                                      pady=10,
                                      width=8,
                                      command=self.start_counting)
        self.start_button.pack(side=tk.LEFT, padx=3)
        
        self.stop_button = tk.Button(button_container,
                                     text="⏸  정지",
                                     font=("Segoe UI", 11, "bold"),
                                     bg=self.colors['danger'],
                                     fg="white",
                                     activebackground="#D93D3F",
                                     activeforeground="white",
                                     relief=tk.FLAT,
                                     cursor="hand2",
                                     padx=20,
                                     pady=10,
                                     width=8,
                                     state=tk.DISABLED,
                                     command=self.stop_counting)
        self.stop_button.pack(side=tk.LEFT, padx=3)
        
        # 리셋 버튼
        self.reset_button = tk.Button(control_frame,
                                      text="초기화",
                                      font=("Segoe UI", 10, "bold"),
                                      bg=self.colors['card'],
                                      fg=self.colors['text_primary'],
                                      activebackground="#F0F0F0",
                                      activeforeground=self.colors['text_primary'],
                                      relief=tk.FLAT,
                                      cursor="hand2",
                                      padx=15,
                                      pady=8,
                                      command=self.reset_count)
        self.reset_button.pack(pady=(6, 0))
        
        # 상태 표시
        status_frame = tk.Frame(main_container, bg=self.colors['card'],
                              relief=tk.FLAT, bd=0)
        status_frame.pack(fill=tk.X)
        
        self.status_label = tk.Label(status_frame,
                                    text="● 대기 중",
                                    font=("Segoe UI", 9, "bold"),
                                    fg=self.colors['text_secondary'],
                                    bg=self.colors['card'],
                                    pady=8)
        self.status_label.pack()
        
        # 안내 문구
        help_label = tk.Label(status_frame,
                            text="카운트가 작동하지 않으면 관리자 권한으로 실행해보세요",
                            font=("Segoe UI", 10, "bold"),
                            fg="#777777",
                            bg=self.colors['card'])
        help_label.pack(pady=(0, 6))
    
    def _add_shadow(self, widget):
        """위젯에 그림자 효과"""
        widget.config(highlightbackground=self.colors['border'],
                     highlightthickness=1)
        
    def set_target_key(self):
        """타겟 키 설정"""
        self.key_button.config(text="키를 눌러주세요...", bg="#FFA940")
        self.status_label.config(text="● 키 입력 대기 중...", fg="#FFA940")
        
        # 임시 리스너로 키 입력 받기
        def on_press(key):
            self.target_key = key
            try:
                key_name = key.char if hasattr(key, 'char') else key.name
            except:
                key_name = str(key).replace('Key.', '')
            
            self.selected_key_label.config(text=f"선택된 키: {key_name}",
                                          fg=self.colors['success'])
            self.key_button.config(text="키를 선택하려면 클릭하세요",
                                  bg=self.colors['primary'])
            self.status_label.config(text=f"● '{key_name}' 키 선택 완료",
                                   fg=self.colors['success'])
            return False  # 리스너 종료
        
        temp_listener = Listener(on_press=on_press)
        temp_listener.start()
        
    def start_counting(self):
        """카운팅 시작"""
        if self.target_key is None:
            self.status_label.config(text="⚠️ 먼저 키를 선택해주세요!",
                                   fg=self.colors['danger'])
            return
        
        self.is_counting = True
        self.start_button.config(state=tk.DISABLED, bg="#D0D0D0")
        self.stop_button.config(state=tk.NORMAL, bg=self.colors['danger'])
        self.key_button.config(state=tk.DISABLED, bg="#D0D0D0")
        self.status_label.config(text="● 측정 중 (백그라운드 작동)",
                               fg=self.colors['success'])
        
        # 키가 눌려있는 상태를 추적
        self.key_pressed = False
        
        # 전역 키보드 리스너 시작
        def on_press(key):
            if self.is_counting and key == self.target_key and not self.key_pressed:
                self.key_pressed = True
                self.count += 1
                self.root.after(0, self.update_count_display)
        
        def on_release(key):
            if key == self.target_key:
                self.key_pressed = False
        
        self.listener = Listener(on_press=on_press, on_release=on_release)
        self.listener.start()
        
    def stop_counting(self):
        """카운팅 정지"""
        self.is_counting = False
        self.key_pressed = False
        self.start_button.config(state=tk.NORMAL, bg=self.colors['success'])
        self.stop_button.config(state=tk.DISABLED, bg="#D0D0D0")
        self.key_button.config(state=tk.NORMAL, bg=self.colors['primary'])
        self.status_label.config(text="● 정지됨", fg=self.colors['text_secondary'])
        
        if self.listener:
            self.listener.stop()
            self.listener = None
            
    def reset_count(self):
        """카운트 초기화"""
        self.count = 0
        self.update_count_display()
        self.status_label.config(text="● 카운트 초기화 완료",
                               fg=self.colors['primary'])
        
    def update_count_display(self):
        """카운트 표시 업데이트"""
        self.count_label.config(text=f"{self.count}")
        
    def on_closing(self):
        """프로그램 종료 시"""
        if self.listener:
            self.listener.stop()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = KeyCounterApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()