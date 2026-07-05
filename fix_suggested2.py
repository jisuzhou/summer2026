import re

file_path = r"C:\Users\86187\.qclaw\workspace\growth-bank-site\deploy\index.html"

with open(file_path, 'r', encoding='utf8') as f:
    content = f.read()

# 找到函数的开始和结束位置
start_idx = content.find('function renderSuggestedTasks(){')
if start_idx == -1:
    print("Function not found")
    exit(1)

# 找到函数的结束位置（匹配的 }）
# 简单方法：找到接下来的 `}\n\nfunction` 或 `}\n\n//`
# 但更可靠的方法是：找到 `}).join("");` 然后找到后面的 `}`
end_marker = '}).join("");\n}'
end_idx = content.find(end_marker, start_idx)
if end_idx == -1:
    print("End marker not found")
    exit(1)

end_idx += len(end_marker)

old_func = content[start_idx:end_idx]
print(f"Found function, length: {len(old_func)}")
print("Old function preview:")
print(old_func[:200])
print("...")

# 新函数
new_func = '''function renderSuggestedTasks(){
  console.log("[RENDER] renderSuggestedTasks start");
  const container=document.getElementById("suggestedTasks");
  if(!container)return;
  const recommended=["read-20","sport-30","screen"];
  const done=todayCompleted();
  const tasks=getActiveTasks();
  console.log("[DEBUG] tasks:", tasks.length, tasks);
  container.innerHTML=recommended.map(id=>{
    const t=tasks.find(x=>x.id===id);
    if(!t){console.log("[DEBUG] Task not found:", id);return"";}
    const checked=done.includes(id);
    const title=t.title||t.name||id;
    const icon=t.icon||"📌";
    return`<div class="suggested-item ${checked?'checked':''}">
      <span class="suggested-icon">${icon}</span>
      <span>${esc(title)}</span>
      ${checked?'<span style="margin-left:auto;color:#059669;font-weight:700">✓ 已完成</span>':'<span style="margin-left:auto;color:#64748b;font-size:12px">+'+(t.pts||0)+'分</span>'}
    </div>`;
  }).join("");
}'''

# 替换
new_content = content[:start_idx] + new_func + content[end_idx:]

with open(file_path, 'w', encoding='utf8') as f:
    f.write(new_content)

print("Successfully replaced renderSuggestedTasks function")
