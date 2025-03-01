import random
import tkinter as tk
from tkinter import scrolledtext

def to_s32(value):
    value = value & 0xFFFFFFFF
    if value & 0x80000000:
        return value - 0x100000000
    return value

def getvscode(code1, code2):
    if code1 != 0x5601:
        print("Oops! Wrong magic number for VocalShifter.")
        return [0, 0]

    code1_a, code1_b, code1_c = 0x5601, 0x5601, 0
    code3, code4 = 0, 0

    for _ in range(32):
        inner_term = to_s32((code1_a & code2) | (code1_c & ~code1_a))
        temp = to_s32(to_s32(code4) + to_s32(inner_term) + 0x5D2D273C)
        
        right_shift = (temp >> 0x1D) & 0xFFFFFFFF
        multiply = to_s32(0x8 * temp)
        
        code1_a = to_s32(to_s32(code1_a) + to_s32(right_shift + multiply))
        
        xor_term = to_s32(code1_b ^ code1_c ^ code4)
        temp_code_a = to_s32(to_s32(code2) + to_s32(xor_term) - 0x4498517B)
        
        inner_term2 = to_s32((code2 & code4) | (code1_c & ~code4))
        combined = to_s32(to_s32(inner_term2) + to_s32(code1_b) - 0x2930C43F)
        
        left_shift = to_s32((combined << 0xA) & 0xFFFFFFFF)
        right_shift2 = (combined >> 0x16) & 0xFFFFFFFF
        code2_a = to_s32(to_s32(code2) + to_s32(left_shift + right_shift2))
        
        temp_code_b = to_s32(to_s32(code1_b) ^ to_s32(code4 | ~code2))
        code1_b = code1_a
        
        left_shift2 = to_s32((temp_code_a << 0x11) & 0xFFFFFFFF)
        right_shift3 = (temp_code_a >> 0xF) & 0xFFFFFFFF
        code3 = to_s32(to_s32(code1_c) + to_s32(right_shift3 + left_shift2))
        
        temp_code_c = to_s32(to_s32(temp_code_b) + to_s32(code1_c) - 0x5426DFEB)
        code2 = code2_a
        
        left_shift3 = to_s32((temp_code_c << 0x18) & 0xFFFFFFFF)
        right_shift4 = (temp_code_c >> 0x8) & 0xFFFFFFFF
        code4 = to_s32(to_s32(code4) + to_s32(left_shift3 + right_shift4))
        
        code1_c = code3

    return [code3, code4]

def convertlicencecode(code1, code2, code3, code4):
    code1_a = to_s32(code1 ^ 0x1248)
    code2_a = to_s32(code2 ^ 0x8421)
    code3_a = to_s32(code3 ^ 0x1248)
    code4_a = to_s32(code4 ^ 0x8421)

    code1 = to_s32((0x55AA & code2_a) + (0xAA55 & code4_a))
    code2 = to_s32((0x55AA & code3_a) + (0xAA55 & code1_a))
    code3 = to_s32((0x55AA & code4_a) + (0xAA55 & code2_a))
    code4 = to_s32((0x55AA & code1_a) + (0xAA55 & code3_a))
    
    return [code1 & 0xFFFF, code2 & 0xFFFF, code3 & 0xFFFF, code4 & 0xFFFF]

def generatelicencecode():
    code1 = 0x5601
    code2 = random.randint(0, 0xFFFF)

    fetched_code = getvscode(code1, code2)
    code3, code4 = fetched_code[0], fetched_code[1]

    codes_b = convertlicencecode(code1, code2, code3, code4)
    code1_b, code2_b, code3_b, code4_b = codes_b[0], codes_b[1], codes_b[2], codes_b[3]

    return f"{code4_b:04X}-{code1_b:04X}-{code2_b:04X}-{code3_b:04X}"

def generate():
    try:
        amount = int(entry.get())
        if amount <= 0:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Enter positive number:")
            return
                
        result_text.delete(1.0, tk.END)
        for _ in range(amount):
            key = generatelicencecode()
            result_text.insert(tk.END, key + "\n")
    except ValueError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Input cannot be decimal number!")

root = tk.Tk()
root.title("vskeygen")
root.geometry("320x240")
root.resizable(False, False)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill=tk.BOTH, expand=True)

label = tk.Label(frame, text="How many licence keys to generate?", font=("Arial", 10))
label.pack(pady=(0, 5))

entry = tk.Entry(frame, width=20, justify='center')
entry.pack(pady=(0, 20))
entry.focus()

generate_button = tk.Button(frame, text="Generate", width=15, height=1)
generate_button.config(command=generate)
generate_button.pack(pady=(0, 20))

result_text = scrolledtext.ScrolledText(frame, height=15, width=35)
result_text.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

exit_button = tk.Button(frame, text="Exit", width=15, height=1)
exit_button.config(command=root.destroy)
exit_button.pack()

root.mainloop()

if __name__ == "__main__":
    generate()
