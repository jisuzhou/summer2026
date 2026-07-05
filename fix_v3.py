import re

file_path = r"C:\Users\86187\.qclaw\workspace\growth-bank-site\deploy\index.html"

with open(file_path, 'r', encoding='utf8') as f:
    content = f.read()

# 找到 handleCompleteSuggested 函数的开始和结束
start_marker = 'function handleCompleteSuggested(){'
end_marker = '}\ndocument.getElementById("completeSuggested")'

start_idx = content.find(start_marker)
if start_idx == -1:
    print("ERROR: Could not find handleCompleteSuggested function")
    exit(1)

end_idx = content.find(end_marker, start_idx)
if end_idx == -1:
    print("ERROR: Could not find end of handleCompleteSuggested function")
    exit(1)

print(f"Found function at index {start_idx} to {end_idx}")

# 新函数（修复版本）
new_func = '''function handleCompleteSuggested(){
  const recommended=["read-20","sport-30","screen"];
  const done=new Set(todayCompleted());
  let addedTasks=0;
  let addedPoints=0;
  recommended.forEach(id=>{
    if(!done.has(id)){
      const t=getActiveTasks().find(x=>x.id===id);
      if(t){
        data.completedToday.push({id,at:new Date().toLocaleDateString("zh-CN")});
        data.points+=t.pts;
        done.add(id);
        addedTasks++;
        addedPoints+=t.pts;
      }
    }
  });
  if(addedTasks>0){
    data.history.unshift({type:"earn",date:new Date().toLocaleString("zh-CN"),text:"一键完成推荐三项",points:addedPoints});
    saveState();
    celebrate();
    showToast("推荐三项已存入成长账户，获得"+addedPoints+"分！");
  }else{
    showToast("推荐三项今天已完成啦！");
  }
  renderAll();
}

'''

# 替换
new_content = content[:start_idx] + new_func + content[end_idx:]

# 保存（不使用 emoji，避免编码错误）
with open(file_path, 'w', encoding='utf8') as f:
    f.write(new_content)

print("SUCCESS: Fixed handleCompleteSuggested function")
print("Changes:")
print("  1. Added data.completedToday.push() to complete tasks")
print("  2. Fixed addedTasks/addedPoints tracking")
print("  3. History record now shows correct points")
