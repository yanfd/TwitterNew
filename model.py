import customtkinter as ctk

class ModernApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 窗口设置
        self._set_window_geometry()
        self.configure(fg_color="white")  # 主背景设为纯白
        
        # ====== 主界面组件 ======
        # 主容器（用于居中布局）
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # 标题标签
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="信息发布系统",
            font=("Microsoft YaHei", 18, "bold"),
            text_color="#2c3e50"
        )
        self.title_label.grid(row=0, column=0, pady=(0, 15), sticky="w")

        # 文本输入框
        self.text_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="请输入内容...",
            border_color="#3498db",
            border_width=1,
            fg_color="white",
            corner_radius=8
        )
        self.text_entry.grid(row=1, column=0, pady=5, sticky="ew")

        # ====== 动态选项区 ======
        # 第一个选项菜单
        self.option1_menu = ctk.CTkOptionMenu(
            self.main_frame,
            values=["选择分类", "新闻", "公告", "其他"],
            fg_color="#f8f9fa",
            button_color="#3498db",
            dropdown_fg_color="#f8f9fa",
            text_color="#2c3e50",
            command=self.toggle_extra_field
        )
        self.option1_menu.grid(row=2, column=0, pady=5, sticky="ew")

        # 第二个选项菜单（初始隐藏）
        self.option2_menu = ctk.CTkOptionMenu(
            self.main_frame,
            values=["选择优先级", "高", "中", "低"],
            fg_color="#f8f9fa",
            button_color="#3498db",
            dropdown_fg_color="#f8f9fa",
            text_color="#2c3e50"
        )
        self.option2_menu.grid(row=3, column=0, pady=5, sticky="ew")
        self.option2_menu.grid_remove()  # 初始隐藏

        # 动态扩展的输入框
        self.extra_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="附加信息...",
            border_color="#e74c3c",
            border_width=1,
            fg_color="white",
            corner_radius=8
        )
        self.extra_entry.grid(row=4, column=0, pady=5, sticky="ew")
        self.extra_entry.grid_remove()  # 初始隐藏

        # ====== 操作按钮 ======
        self.submit_btn = ctk.CTkButton(
            self.main_frame,
            text="确认发布",
            command=self.submit_action,
            fg_color="transparent",
            border_width=2,
            border_color="#3498db",
            text_color="#3498db",
            hover_color="#ebf5fb",
            corner_radius=20  # 圆角按钮
        )
        self.submit_btn.grid(row=5, column=0, pady=15, sticky="ew")

        # 状态标签
        self.status_label = ctk.CTkLabel(
            self,
            text="就绪",
            text_color="#7f8c8d",
            anchor="center"
        )
        self.status_label.pack(side="bottom", fill="x", pady=10)

    def _set_window_geometry(self):
        """设置窗口位置和大小"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 400
        window_height = 450
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 4  # 偏上方
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.resizable(False, False)

    def toggle_extra_field(self, choice):
        """切换显示额外输入框"""
        if choice == "其他":
            self.option2_menu.grid()
            self.extra_entry.grid()
        else:
            self.option2_menu.grid_remove()
            self.extra_entry.grid_remove()

    def submit_action(self):
        """提交操作"""
        main_text = self.text_entry.get()
        category = self.option1_menu.get()
        priority = self.option2_menu.get() if self.option2_menu.winfo_ismapped() else "无"
        extra_info = self.extra_entry.get() if self.extra_entry.winfo_ismapped() else "无"

        # 模拟数据处理
        status_message = (
            f"提交成功！\n"
            f"分类: {category}\n"
            f"优先级: {priority}\n"
            f"附加信息: {extra_info}"
        )
        self.status_label.configure(
            text=status_message,
            text_color="#27ae60"
        )
        self.after(3000, lambda: self.status_label.configure(text="就绪", text_color="#7f8c8d"))

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # 固定为亮色模式
    ctk.set_default_color_theme("blue")
    app = ModernApp()
    app.mainloop()