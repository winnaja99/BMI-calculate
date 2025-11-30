import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import datetime
import os

# --- การตั้งค่าสีและตัวแปร ---
BG_COLOR = "#E1F5FE"   # พื้นหลังสีฟ้าอ่อน
BTN_COLOR = "#29B6F6"  # ปุ่มสีฟ้าสดใส
TEXT_COLOR = "black"

# ตัวแปรสำหรับเก็บค่าล่าสุด (เพื่อใช้ตอนกดบันทึก)
last_bmi = None
last_weight = None
last_height = None
last_category = None

# --- ฟังก์ชันการทำงาน ---

def calculate_bmi():
    """คำนวณ BMI"""
    global last_bmi, last_weight, last_height, last_category
    
    try:
        w = entry_weight.get()
        h = entry_height.get()

        if not w or not h:
            messagebox.showwarning("แจ้งเตือน", "กรุณากรอกข้อมูลให้ครบ")
            return

        weight = float(w)
        height_cm = float(h)

        if weight <= 0 or height_cm <= 0:
            messagebox.showerror("Error", "ตัวเลขต้องมากกว่า 0")
            return

        # คำนวณ
        height_m = height_cm / 100
        bmi = weight / (height_m ** 2)

        # แปลผล
        if bmi < 18.5:
            category = "ผอม"
            c_code = "#1976D2" # น้ำเงิน
        elif 18.5 <= bmi < 23:
            category = "ปกติ"
            c_code = "#388E3C" # เขียว
        elif 23 <= bmi < 25:
            category = "ท้วม"
            c_code = "#FBC02D" # เหลืองเข้ม
        elif 25 <= bmi < 30:
            category = "อ้วน"
            c_code = "#F57C00" # ส้ม
        else:
            category = "อ้วนมาก"
            c_code = "#D32F2F" # แดง

        # แสดงผล
        lbl_result.config(text=f"BMI: {bmi:.2f}", fg=c_code)
        lbl_category.config(text=f"เกณฑ์: {category}", fg=c_code)

        # เก็บค่าใส่ตัวแปร รอการบันทึก
        last_bmi = bmi
        last_weight = weight
        last_height = height_cm
        last_category = category

    except ValueError:
        messagebox.showerror("Error", "กรุณากรอกเป็นตัวเลขเท่านั้น")

def save_data():
    """บันทึกข้อมูลลงไฟล์ txt"""
    if last_bmi is None:
        messagebox.showwarning("แจ้งเตือน", "กรุณากดคำนวณก่อนบันทึก")
        return

    try:
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        # สร้างข้อความที่จะบันทึก
        record = f"{timestamp} | นน:{last_weight} ส:{last_height} | BMI:{last_bmi:.2f} ({last_category})\n"
        
        # บันทึกลงไฟล์ (mode 'a' คือเขียนต่อท้าย)
        with open("bmi_history.txt", "a", encoding="utf-8") as f:
            f.write(record)
        
        messagebox.showinfo("สำเร็จ", "บันทึกข้อมูลเรียบร้อย!")
    except Exception as e:
        messagebox.showerror("Error", f"บันทึกไม่สำเร็จ: {e}")

def show_history():
    """เปิดหน้าต่างดูประวัติ"""
    if not os.path.exists("bmi_history.txt"):
        messagebox.showinfo("ประวัติ", "ยังไม่มีไฟล์ประวัติ (ลองกดบันทึกก่อน)")
        return

    # สร้างหน้าต่างใหม่ (Pop-up)
    top = tk.Toplevel(window)
    top.title("ประวัติการคำนวณ")
    top.geometry("400x350") # ขยายความสูงให้พอดีปุ่มใหม่
    top.config(bg=BG_COLOR)

    tk.Label(top, text="ประวัติที่บันทึกไว้", font=("Arial", 14, "bold"), bg=BG_COLOR).pack(pady=10)

    # กล่องข้อความแบบเลื่อนได้
    txt_area = scrolledtext.ScrolledText(top, width=45, height=10, font=("Arial", 10))
    txt_area.pack(pady=5, padx=10)

    # อ่านไฟล์มาใส่
    with open("bmi_history.txt", "r", encoding="utf-8") as f:
        data = f.read()
        txt_area.insert(tk.INSERT, data)
    
    txt_area.config(state=tk.DISABLED) # ห้ามแก้ไขข้อความ

    # --- ปุ่มย้อนกลับ (Back Button) ---
    btn_back = tk.Button(top, text="< ย้อนกลับหน้าคำนวณ", font=("Arial", 10, "bold"),
                         bg="#78909C", fg="white", width=20, 
                         command=top.destroy) # top.destroy จะปิดหน้าต่าง Pop-up นี้
    btn_back.pack(pady=15)

def exit_program():
    window.destroy()

# --- ส่วนหน้าจอ GUI หลัก ---
window = tk.Tk()
window.title("โปรแกรมคำนวณ BMI")
window.geometry("360x420")
window.config(bg=BG_COLOR)

# หัวข้อ
tk.Label(window, text="BMI Calculator", font=("Arial", 20, "bold"), bg=BG_COLOR, fg="#01579B").pack(pady=15)

# กรอกน้ำหนัก
frame_input = tk.Frame(window, bg=BG_COLOR)
frame_input.pack(pady=5)

tk.Label(frame_input, text="น้ำหนัก (kg):", font=("Arial", 12), bg=BG_COLOR).grid(row=0, column=0, padx=5, pady=5)
entry_weight = tk.Entry(frame_input, font=("Arial", 12), width=10)
entry_weight.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="ส่วนสูง (cm):", font=("Arial", 12), bg=BG_COLOR).grid(row=1, column=0, padx=5, pady=5)
entry_height = tk.Entry(frame_input, font=("Arial", 12), width=10)
entry_height.grid(row=1, column=1, padx=5, pady=5)

# ปุ่มคำนวณ
btn_calc = tk.Button(window, text="คำนวณ BMI", font=("Arial", 12, "bold"), bg=BTN_COLOR, fg="white", width=15, command=calculate_bmi)
btn_calc.pack(pady=10)

# แสดงผล
lbl_result = tk.Label(window, text="BMI: --", font=("Arial", 18, "bold"), bg=BG_COLOR)
lbl_result.pack()
lbl_category = tk.Label(window, text="เกณฑ์: --", font=("Arial", 14), bg=BG_COLOR)
lbl_category.pack(pady=5)

# ปุ่มเสริม (บันทึก / ดูประวัติ)
frame_btns = tk.Frame(window, bg=BG_COLOR)
frame_btns.pack(pady=10)

btn_save = tk.Button(frame_btns, text="บันทึกผล", bg="#66BB6A", fg="white", width=10, command=save_data)
btn_save.grid(row=0, column=0, padx=5)

btn_hist = tk.Button(frame_btns, text="ดูประวัติ", bg="#AB47BC", fg="white", width=10, command=show_history)
btn_hist.grid(row=0, column=1, padx=5)

# ปุ่มออก
tk.Button(window, text="Exit", bg="#FF5722", fg="white", width=8, command=exit_program).pack(pady=10)

window.mainloop()