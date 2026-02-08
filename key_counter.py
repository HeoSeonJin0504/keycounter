import tkinter as tk
from tkinter import ttk
from pynput.keyboard import Listener, Key
import threading
import time

class KeyCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Key Counter")
        self.root.geometry("480x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#F8F9FA")
        
        # 변수 초기화
        self.target_key = None
        self.count = 0
        self.is_counting = False
        self.listener = None
        self.key_pressed = False
        
        # 연타 기록 관련 변수
        self.first_key_time = None
        self.last_event_time = None
        self.recording = False
        
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
        
        self.setup_ui()
        
    def setup_ui(self):
        """UI 구성"""
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # 키 선택 영역
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
        
        # 카운트 디스플레이 영역
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
        
        count_display_frame = tk.Frame(count_inner, bg=self.colors['count_bg'])
        count_display_frame.pack(pady=(5, 0))
        
        self.count_label = tk.Label(count_display_frame,
                                   text="0",
                                   font=("Segoe UI", 40, "bold"),
                                   fg=self.colors['primary'],
                                   bg=self.colors['count_bg'])
        self.count_label.pack(side=tk.LEFT)
        
        count_unit = tk.Label(count_display_frame,
                            text=" 회",
                            font=("Segoe UI", 16, "bold"),
                            fg=self.colors['text_secondary'],
                            bg=self.colors['count_bg'])
        count_unit.pack(side=tk.LEFT, anchor='s', pady=(0, 8))
        
        help_label = tk.Label(count_inner,
                            text="기록이 안되면 관리자 권한으로 실행하세요",
                            font=("Segoe UI", 8, "bold"),
                            fg="#999999",
                            bg=self.colors['count_bg'])
        help_label.pack(pady=(5, 0))
        
        # 컨트롤 버튼
        control_frame = tk.Frame(main_container, bg=self.colors['bg'])
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        button_container = tk.Frame(control_frame, bg=self.colors['bg'])
        button_container.pack()
        
        self.start_button = tk.Button(button_container,
                                      text="▶  시작",
                                      font=("Segoe UI", 10, "bold"),
                                      bg=self.colors['success'],
                                      fg="white",
                                      activebackground="#45A317",
                                      activeforeground="white",
                                      relief=tk.FLAT,
                                      cursor="hand2",
                                      padx=15,
                                      pady=8,
                                      width=8,
                                      command=self.start_counting)
        self.start_button.pack(side=tk.LEFT, padx=3)
        
        self.stop_button = tk.Button(button_container,
                                     text="⏸  정지",
                                     font=("Segoe UI", 10, "bold"),
                                     bg=self.colors['danger'],
                                     fg="white",
                                     activebackground="#D93D3F",
                                     activeforeground="white",
                                     relief=tk.FLAT,
                                     cursor="hand2",
                                     padx=15,
                                     pady=8,
                                     width=8,
                                     state=tk.DISABLED,
                                     command=self.stop_counting)
        self.stop_button.pack(side=tk.LEFT, padx=3)
        
        self.reset_button = tk.Button(button_container,
                                      text="초기화",
                                      font=("Segoe UI", 10, "bold"),
                                      bg=self.colors['card'],
                                      fg=self.colors['text_primary'],
                                      activebackground="#F0F0F0",
                                      activeforeground=self.colors['text_primary'],
                                      relief=tk.SOLID,
                                      borderwidth=1,
                                      cursor="hand2",
                                      padx=15,
                                      pady=8,
                                      width=8,
                                      command=self.reset_count)
        self.reset_button.pack(side=tk.LEFT, padx=3)
        
        # 연타 기록 테이블 (Treeview)
        record_card = tk.Frame(main_container, bg=self.colors['card'],
                              relief=tk.FLAT, bd=0)
        record_card.pack(fill=tk.BOTH, expand=True, pady=(0, 0))
        self._add_shadow(record_card)
        
        record_inner = tk.Frame(record_card, bg=self.colors['card'])
        record_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)
        
        record_label = tk.Label(record_inner,
                               text="연타 기록",
                               font=("Segoe UI", 10, "bold"),
                               fg=self.colors['text_primary'],
                               bg=self.colors['card'])
        record_label.pack(anchor=tk.W, pady=(0, 8))
        
        # Treeview 스타일
        style = ttk.Style()
        style.theme_use('default')
        
        style.configure("Treeview.Heading",
                       background="#F0F7FF",
                       foreground=self.colors['text_secondary'],
                       font=("Segoe UI", 9, "bold"),
                       borderwidth=0,
                       relief="flat")
        
        style.configure("Treeview",
                       background="#FFFFFF",
                       foreground=self.colors['text_primary'],
                       fieldbackground="#FFFFFF",
                       font=("Segoe UI", 9),
                       borderwidth=0,
                       rowheight=25)
        
        style.map("Treeview",
                 background=[('selected', '#E3F2FD')],
                 foreground=[('selected', self.colors['text_primary'])])
        
        tree_frame = tk.Frame(record_inner, bg=self.colors['card'])
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('key', 'event', 'elapsed', 'interval')
        self.tree = ttk.Treeview(tree_frame,
                                columns=columns,
                                show='headings',
                                height=10,
                                selectmode='none')
        
        self.tree.heading('key', text='키')
        self.tree.heading('event', text='이벤트')
        self.tree.heading('elapsed', text='경과시간')
        self.tree.heading('interval', text='간격')
        
        self.tree.column('key', width=100, anchor='w')
        self.tree.column('event', width=80, anchor='center')
        self.tree.column('elapsed', width=100, anchor='center')
        self.tree.column('interval', width=80, anchor='center')
        
        scrollbar = ttk.Scrollbar(tree_frame,
                                 orient="vertical",
                                 command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 교차 행 색상
        self.tree.tag_configure('oddrow', background='#FFFFFF')
        self.tree.tag_configure('evenrow', background='#F9FAFB')
    
    def _add_shadow(self, widget):
        """위젯에 테두리 효과 추가"""
        widget.config(highlightbackground=self.colors['border'],
                     highlightthickness=1)
        
    def set_target_key(self):
        """측정할 키를 선택"""
        self.key_button.config(text="키를 눌러주세요...", bg="#FFA940")
        
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
            return False
        
        temp_listener = Listener(on_press=on_press)
        temp_listener.start()
        
    def start_counting(self):
        """연타 측정 시작"""
        if self.target_key is None:
            self.key_button.config(bg=self.colors['danger'])
            self.root.after(500, lambda: self.key_button.config(bg=self.colors['primary']))
            return
        
        self.is_counting = True
        self.recording = False
        self.start_button.config(state=tk.DISABLED, bg="#D0D0D0")
        self.stop_button.config(state=tk.NORMAL, bg=self.colors['danger'])
        self.key_button.config(state=tk.DISABLED, bg="#D0D0D0")
        
        self.key_pressed = False
        
        # 전역 키보드 리스너 시작
        def on_press(key):
            if self.is_counting and key == self.target_key and not self.key_pressed:
                self.key_pressed = True
                
                current_time = time.time()
                
                # 첫 키 입력 시 기록 시작
                if not self.recording:
                    self.recording = True
                    self.first_key_time = current_time
                    self.last_event_time = current_time
                
                elapsed_ms = int((current_time - self.first_key_time) * 1000)
                
                if self.last_event_time:
                    interval_ms = int((current_time - self.last_event_time) * 1000)
                else:
                    interval_ms = 0
                
                self.last_event_time = current_time
                
                try:
                    key_name = key.char.upper() if hasattr(key, 'char') else key.name.upper()
                except:
                    key_name = str(key).replace('Key.', '').upper()
                
                self.root.after(0, lambda: self.add_record_entry(key_name, "DOWN", elapsed_ms, interval_ms))
                
                self.count += 1
                self.root.after(0, self.update_count_display)
        
        def on_release(key):
            if key == self.target_key and self.key_pressed:
                self.key_pressed = False
                
                if self.recording:
                    current_time = time.time()
                    elapsed_ms = int((current_time - self.first_key_time) * 1000)
                    
                    if self.last_event_time:
                        interval_ms = int((current_time - self.last_event_time) * 1000)
                    else:
                        interval_ms = 0
                    
                    self.last_event_time = current_time
                    
                    try:
                        key_name = key.char.upper() if hasattr(key, 'char') else key.name.upper()
                    except:
                        key_name = str(key).replace('Key.', '').upper()
                    
                    self.root.after(0, lambda: self.add_record_entry(key_name, "UP", elapsed_ms, interval_ms))
        
        self.listener = Listener(on_press=on_press, on_release=on_release)
        self.listener.start()
        
    def stop_counting(self):
        """연타 측정 정지"""
        self.is_counting = False
        self.key_pressed = False
        self.recording = False
        self.start_button.config(state=tk.NORMAL, bg=self.colors['success'])
        self.stop_button.config(state=tk.DISABLED, bg="#D0D0D0")
        self.key_button.config(state=tk.NORMAL, bg=self.colors['primary'])
        
        if self.listener:
            self.listener.stop()
            self.listener = None
            
    def reset_count(self):
        """카운트 및 기록 초기화"""
        if self.is_counting:
            self.stop_counting()
        
        self.count = 0
        self.first_key_time = None
        self.last_event_time = None
        self.recording = False
        self.key_pressed = False
        self.update_count_display()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def add_record_entry(self, key_name, event, elapsed_ms, interval_ms):
        """실시간으로 기록 항목 추가"""
        interval_text = f"+{interval_ms}ms" if interval_ms > 0 else "-"
        
        row_count = len(self.tree.get_children())
        tag = 'evenrow' if row_count % 2 == 0 else 'oddrow'
        
        self.tree.insert('', tk.END,
                        values=(key_name, event, f"{elapsed_ms}ms", interval_text),
                        tags=(tag,))
        
        # 자동 스크롤
        children = self.tree.get_children()
        if children:
            self.tree.see(children[-1])
        
    def update_count_display(self):
        """카운트 표시 업데이트"""
        self.count_label.config(text=f"{self.count}")
        
    def on_closing(self):
        """프로그램 종료 시 리스너 정리"""
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
