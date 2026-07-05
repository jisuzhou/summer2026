import re

file_path = r"C:\Users\86187\.qclaw\workspace\growth-bank-site\deploy\index.html"

with open(file_path, 'r', encoding='utf8') as f:
    content = f.read()

# 修复 handleCompleteSuggested 函数
old_func = '''function handleCompleteSuggested(){
  const recommended=["read-20","sport-30","screen"];
  const done=new Set(todayCompleted());
  let added=0;
  recommended.forEach(id=>{
    if(!done.has(id)){
      const t=getActiveTasks().find(x=>x.id===id);
      if(t){done.add(id);data.points+=t.pts;added++;}
    }
  });
  if(added>0){
    data.history.unshift({type:"earn",date:new Date().toLocaleString("zh-CN"),text:"一键完成推荐三项",points:added});
    saveState();
    celebrate();
    showToast("推荐三项已存入成长账户。");
  }else{
    showToast("推荐三项今天已完成啦！");
  }
  renderAll();
}'''

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
}'''

if old_func in content:
    content = content.replace(old_func, new_func)
    print("✅ Fixed handleCompleteSuggested function")
    print("  - Now properly adds tasks to data.completedToday")
    print("  - Fixed history record to show points instead of task count")
else:
    print("❌ Could not find handleCompleteSuggested function")
    # 手动查找
    idx = content.find('function handleCompleteSuggested(){')
    if idx >= 0:
        print(f"Found function at index {idx}")
        print("Context:", content[idx:idx+200])

# 保存
with open(file_path, 'w', encoding='utf8') as f:
    f.write(content)

print("\n✅ File saved successfully!")
