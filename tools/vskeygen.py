import random
import tkinter as tk
from tkinter import scrolledtext

def to_s32(value):
    value = value & 0xFFFFFFFF
    if value & 0x80000000:
        return value - 0x100000000
    return value

def getlicencecodeparts(magic_number, random_seed):
    if magic_number != 0x5601:
        print("Oops! Wrong magic number for VocalShifter.")
        return [0, 0]

    state_a, state_b, state_c = 0x5601, 0x5601, 0
    result_code1, result_code2 = 0, 0

    for _ in range(32):
        masked_term = to_s32((state_a & random_seed) | (state_c & ~state_a))
        sum_temp = to_s32(to_s32(result_code2) + to_s32(masked_term) + 0x5D2D273C)
        
        rotated_right = (sum_temp >> 0x1D) & 0xFFFFFFFF
        rotated_left = to_s32(0x8 * sum_temp)
        
        state_a = to_s32(to_s32(state_a) + to_s32(rotated_right + rotated_left))
        
        xor_result = to_s32(state_b ^ state_c ^ result_code2)
        transform_a = to_s32(to_s32(random_seed) + to_s32(xor_result) - 0x4498517B)
        
        masked_term2 = to_s32((random_seed & result_code2) | (state_c & ~result_code2))
        combined_sum = to_s32(to_s32(masked_term2) + to_s32(state_b) - 0x2930C43F)
        
        shift_left = to_s32((combined_sum << 0xA) & 0xFFFFFFFF)
        shift_right = (combined_sum >> 0x16) & 0xFFFFFFFF
        next_input = to_s32(to_s32(random_seed) + to_s32(shift_left + shift_right))
        
        transform_b = to_s32(to_s32(state_b) ^ to_s32(result_code2 | ~random_seed))
        state_b = state_a
        
        transform_left = to_s32((transform_a << 0x11) & 0xFFFFFFFF)
        transform_right = (transform_a >> 0xF) & 0xFFFFFFFF
        result_code1 = to_s32(to_s32(state_c) + to_s32(transform_right + transform_left))
        
        transform_c = to_s32(to_s32(transform_b) + to_s32(state_c) - 0x5426DFEB)
        random_seed = next_input
        
        final_left = to_s32((transform_c << 0x18) & 0xFFFFFFFF)
        final_right = (transform_c >> 0x8) & 0xFFFFFFFF
        result_code2 = to_s32(to_s32(result_code2) + to_s32(final_left + final_right))
        
        state_c = result_code1

    return [result_code1, result_code2]

def convertlicencecode(magic_number, random_seed, code3, code4):
    xored_code1 = to_s32(magic_number ^ 0x1248)
    xored_code2 = to_s32(random_seed ^ 0x8421)
    xored_code3 = to_s32(code3 ^ 0x1248)
    xored_code4 = to_s32(code4 ^ 0x8421)

    final_code1 = to_s32((0x55AA & xored_code2) + (0xAA55 & xored_code4))
    final_code2 = to_s32((0x55AA & xored_code3) + (0xAA55 & xored_code1))
    final_code3 = to_s32((0x55AA & xored_code4) + (0xAA55 & xored_code2))
    final_code4 = to_s32((0x55AA & xored_code1) + (0xAA55 & xored_code3))
    
    return [final_code1 & 0xFFFF, final_code2 & 0xFFFF, final_code3 & 0xFFFF, final_code4 & 0xFFFF]

def generatelicencecode():
    magic_number = 0x5601
    random_seed = random.randint(0, 0xFFFF)

    last_2_parts = getlicencecodeparts(magic_number, random_seed)
    code3, code4 = last_2_parts[0], last_2_parts[1]

    converted_codes = convertlicencecode(magic_number, random_seed, code3, code4)
    final_code1, final_code2, final_code3, final_code4 = converted_codes[0], converted_codes[1], converted_codes[2], converted_codes[3]

    return f"{final_code4:04X}-{final_code1:04X}-{final_code2:04X}-{final_code3:04X}"

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
