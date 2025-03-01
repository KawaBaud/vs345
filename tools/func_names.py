import re

def extract_func_names():
    func_names = []
    
    with open('vocalshifter.hsp', 'r', encoding='shift_jis') as f:
        content = f.read()
        
    pattern = r'(#def(?:c|)func)\s+(\w+)'
    matches = re.finditer(pattern, content)
    for match in matches:
        func_names.append(match.group(1) + ' ' + match.group(2))
        
    with open('func_names.txt', 'w', encoding='utf-8') as f:
        for name in func_names:
            f.write(name + '\n')

if __name__ == '__main__':
    extract_func_names()
