const fs = require('fs');
const filePath = 'C:\\Users\\86187\\.qclaw\\workspace\\growth-bank-site\\deploy\\index.html';

let content = fs.readFileSync(filePath, 'utf8');

// 简单的字符串替换：添加调试日志和字段兼容处理
// 在 renderSuggestedTasks 函数中添加调试日志

const searchStr1 = '  const tasks=getActiveTasks();\n  container.innerHTML=recommended.map(id=>{';
const replaceStr1 = '  const tasks=getActiveTasks();\n  console.log("[DEBUG] getActiveTasks returned:", tasks.length, "tasks");\n  if(tasks.length>0) console.log("[DEBUG] First task:", JSON.stringify(tasks[0]));\n  container.innerHTML=recommended.map(id=>{';

const searchStr2 = '    if(!t)return"";\n    const checked=done.includes(id);\n    return`<div class="suggested-item ${checked?\'checked\':\'\'}">\n      <span class="suggested-icon">${t.icon}</span>\n      <span>${esc(t.title)}</span>';

const replaceStr2 = '    if(!t)return"";\n    const checked=done.includes(id);\n    const title=t.title||t.name||id;\n    const icon=t.icon||"📌";\n    return`<div class="suggested-item ${checked?\'checked\':\'\'}">\n      <span class="suggested-icon">${icon}</span>\n      <span>${esc(title)}</span>';

// 执行替换
let modified = content;

if (modified.includes(searchStr1)) {
  modified = modified.replace(searchStr1, replaceStr1);
  console.log('Added debug logs');
} else {
  console.log('Could not find searchStr1');
}

if (modified.includes(searchStr2)) {
  modified = modified.replace(searchStr2, replaceStr2);
  console.log('Added field compatibility');
} else {
  console.log('Could not find searchStr2');
}

// 保存
if (modified !== content) {
  fs.writeFileSync(filePath, modified, 'utf8');
  console.log('File updated successfully');
} else {
  console.log('No changes made');
}
