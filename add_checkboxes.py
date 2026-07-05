import re

file_path = r"C:\Users\86187\.qclaw\workspace\growth-bank-site\deploy\index.html"

with open(file_path, 'r', encoding='utf8') as f:
    content = f.read()

# ========== 1. 添加 toggleSuggestedTask 函数 ==========
# 在 handleCompleteSuggested 函数之前添加新函数

new_toggle_func = '''
/* 切换单个推荐任务 */
function toggleSuggestedTask(id){
  const done=new Set(todayCompleted());
  if(done.has(id)){
    // 如果已完成，移除
    data.completedToday=data.completedToday.filter(x=>x.id!==id);
  }else{
    // 如果未完成，添加
    data.completedToday.push({id,at:new Date().toLocaleDateString("zh-CN")});
  }
  saveState();
  renderAll();
  showToast(done.has(id)?"已取消完成":"任务完成！");
}

'''

# 找到 handleCompleteSuggested 函数的位置
handle_idx = content.find('function handleCompleteSuggested(){')
if handle_idx == -1:
    print("Could not find handleCompleteSuggested function")
    exit(1)

# 在它前面插入新函数
content = content[:handle_idx] + new_toggle_func + content[handle_idx:]

# ========== 2. 修改 renderSuggestedTasks 函数：图标换成勾选框 ==========

old_render = '''function renderSuggestedTasks(){
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

new_render = '''function renderSuggestedTasks(){
  const container=document.getElementById("suggestedTasks");
  if(!container)return;
  const recommended=["read-20","sport-30","screen"];
  const done=new Set(todayCompleted());
  const tasks=getActiveTasks();
  container.innerHTML=recommended.map(id=>{
    const t=tasks.find(x=>x.id===id);
    if(!t)return"";
    const checked=done.has(id);
    const title=t.title||t.name||id;
    const pts=t.pts||0;
    return`<div class="suggested-item ${checked?'checked':''}" style="cursor:pointer" onclick="toggleSuggestedTask('${id}')">
      <input type="checkbox" ${checked?'checked':''} style="margin-right:8px;cursor:pointer" onchange="event.stopPropagation();toggleSuggestedTask('${id}')">
      <span style="flex:1">${esc(title)}</span>
      ${checked?'<span style="color:#059669;font-weight:700;font-size:12px">+${pts}分 ✓</span>':'<span style="color:#64748b;font-size:12px">+'+pts+'分</span>'}
    </div>`;
  }).join("");
}'''

if old_render in content:
    content = content.replace(old_render, new_render)
    print("Updated renderSuggestedTasks function")
else:
    print("Could not find renderSuggestedTasks function")
    # 尝试查找并手动替换
    start_idx = content.find('function renderSuggestedTasks(){')
    if start_idx >= 0:
        end_marker = '}).join("");\n}'
        end_idx = content.find(end_marker, start_idx)
        if end_idx >= 0:
            end_idx += len(end_marker)
            content = content[:start_idx] + new_render + content[end_idx:]
            print("Manually replaced renderSuggestedTasks function")

# ========== 3. 添加 CSS 样式 ==========

# 找到 </style> 标签，在前面插入新样式
css_style = '''
/* 推荐任务勾选框样式 */
.suggested-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  border-radius: 8px;
  margin-bottom: 6px;
  background: var(--sky);
  transition: all 0.2s;
}
.suggested-item:hover {
  background: var(--mint);
}
.suggested-item.checked {
  background: #d1fae5;
}
.suggested-item input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: var(--leaf);
}
'''

style_end_idx = content.find('</style>')
if style_end_idx == -1:
    print("Could not find </style> tag")
else:
    content = content[:style_end_idx] + css_style + content[style_end_idx:]
    print("Added CSS styles")

# 保存
with open(file_path, 'w', encoding='utf8') as f:
    f.write(content)

print("\n✅ All changes applied successfully!")
print("Changes made:")
print("1. Added toggleSuggestedTask(id) function")
print("2. Replaced icons with checkboxes in renderSuggestedTasks")
print("3. Added CSS styles for suggested items")
