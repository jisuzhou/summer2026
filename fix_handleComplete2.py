import re

file_path = r"C:\Users\86187\.qclaw\workspace\growth-bank-site\deploy\index.html"

with open(file_path, 'r', encoding='utf8') as f:
    content = f.read()

# 找到 handleCompleteSuggested 函数的准确位置
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

# 提取旧函数
old_func = content[start_idx:end_idx]
print(f"Found function at {start_idx}-{end_idx}")
print("Old function:")
print(old_func)
print("\n" + "="*50 + "\n")

# 新函数（修复bug）
new_func = '''function handleCompleteSuggested(){
  const recommended=["read-20","sport-30","screen"];
  const done=new Set(todayCompleted());
  let addedTasks=0;
  let addedPoints=0;
  recommended.forEach(id=>{
    if(!done.has(id)){
      const t=getActiveTasks().find(x=>x.id===id);
      if(t){
        // 添加到今日完成列表
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

# 保存
with open(file_path, 'w', encoding='utf8') as f:
    f.write(new_content)

print("✅ Successfully fixed handleCompleteSuggested function!")
print("\nChanges made:")
print("1. Added data.completedToday.push() to actually complete tasks")
print("2. Fixed addedTasks/addedPoints tracking")
print("3. History record now shows points instead of task count")
