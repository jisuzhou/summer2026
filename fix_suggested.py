import re

file_path = r"C:\Users\86187\.qclaw\workspace\growth-bank-site\deploy\index.html"

with open(file_path, 'r', encoding='utf8') as f:
    content = f.read()

# 查找并替换 renderSuggestedTasks 函数
old_func_pattern = r'function renderSuggestedTasks\(\)\{[^}]*container\.innerHTML=recommended\.map\(id=>\{[^}]*\}\)\.join\(""\);\n\}'

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

# 尝试替换
new_content = re.sub(old_func_pattern, new_func, content, flags=re.DOTALL)

if new_content != content:
    with open(file_path, 'w', encoding='utf8') as f:
        f.write(new_content)
    print("Successfully updated renderSuggestedTasks function")
else:
    print("Could not find the function pattern")
    # 手动查找
    idx = content.find('function renderSuggestedTasks')
    if idx >= 0:
        print(f"Found function at index {idx}")
        print("Context:", content[idx:idx+200])
    else:
        print("Function not found in file")
