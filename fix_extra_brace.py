import re

file_path = r"C:\Users\86187\.qclaw\workspace\growth-bank-site\deploy\index.html"

with open(file_path, 'r', encoding='utf8') as f:
    content = f.read()

# 找到多余的大括号位置
# 在 handleCompleteSuggested 函数结束后，有一个多余的 }
marker = '''renderAll();
}

}
document.getElementById("completeSuggested")'''

if marker in content:
    content = content.replace(marker, '''renderAll();
}

document.getElementById("completeSuggested")''')
    print("SUCCESS: Removed extra brace after handleCompleteSuggested")
else:
    print("ERROR: Could not find the pattern with extra brace")
    # 尝试找附近的上下文
    idx = content.find('handleCompleteSuggested');
    if idx > 0:
        print("Context around handleCompleteSuggested:")
        print(content[idx+500:idx+700])

with open(file_path, 'w', encoding='utf8') as f:
    f.write(content)

print("File saved")
