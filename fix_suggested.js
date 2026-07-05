const fs = require('fs');
const filePath = 'C:\\Users\\86187\\.qclaw\\workspace\\growth-bank-site\\deploy\\index.html';

let content = fs.readFileSync(filePath, 'utf8');

// 添加调试日志和字段兼容处理到 renderSuggestedTasks 函数
const oldPattern = /function renderSuggestedTasks\(\)\{[\s\S]*?container\.innerHTML=recommended\.map\(id=>\{[\s\S]*?\}\)\.join\(""\);\n\}/;

const newFunction = `function renderSuggestedTasks(){
  console.log("[RENDER] renderSuggestedTasks start");
  const container=document.getElementById("suggestedTasks");
  if(!container)return;
  const recommended=["read-20","sport-30","screen"];
  const done=todayCompleted();
  const tasks=getActiveTasks();
  console.log("[DEBUG] getActiveTasks returned:", tasks.length, "tasks");
  if(tasks.length>0) console.log("[DEBUG] First task sample:", JSON.stringify(tasks[0]));
  container.innerHTML=recommended.map(id=>{
    const t=tasks.find(x=>x.id===id);
    console.log("[DEBUG] Looking for task:", id, "found:", t?"yes":"no", t?("title="+t.title+", icon="+t.icon):"");
    if(!t)return"";
    const checked=done.includes(id);
    const title=t.title||t.name||id;
    const icon=t.icon||"📌";
    return\`<div class="suggested-item \${checked?'checked':''}">
      <span class="suggested-icon">\${icon}</span>
      <span>\${esc(title)}</span>
      \${checked?'<span style="margin-left:auto;color:#059669;font-weight:700">✓ 已完成</span>':'<span style="margin-left:auto;color:#64748b;font-size:12px">+'+(t.pts||0)+'分</span>'}
    </div>\`;
  }).join("");
}`;

// 尝试替换
const result = content.replace(oldPattern, newFunction);

if (result !== content) {
  fs.writeFileSync(filePath, result, 'utf8');
  console.log('Successfully updated renderSuggestedTasks function');
} else {
  console.log('Could not find the function pattern. Manual fix needed.');
  console.log('Please check the function manually.');
}
