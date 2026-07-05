$file = "C:\Users\86187\.qclaw\workspace\growth-bank-site\deploy\index.html"
$content = Get-Content $file -Encoding UTF8 -Raw

# 找到 renderSuggestedTasks 函数的位置
$pattern = '(?s)function renderSuggestedTasks\(\)\{.*?^\}'
$match = [regex]::Match($content, $pattern)

if ($match.Success) {
    $oldFunc = $match.Value
    Write-Host "Found renderSuggestedTasks function, length: $($oldFunc.Length)"
    
    # 新函数：添加调试日志和字段兼容处理
    $newFunc = @'
function renderSuggestedTasks(){
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
    return`<div class="suggested-item ${checked?'checked':''}">
      <span class="suggested-icon">${icon}</span>
      <span>${esc(title)}</span>
      ${checked?'<span style="margin-left:auto;color:#059669;font-weight:700">✓ 已完成</span>':'<span style="margin-left:auto;color:#64748b;font-size:12px">+'+(t.pts||0)+'分</span>'}
    </div>`;
  }).join("");
}
'@
    
    # 替换
    $newContent = $content -replace [regex]::Escape($oldFunc), $newFunc
    Set-Content -Path $file -Value $newContent -Encoding UTF8
    Write-Host "Fixed renderSuggestedTasks function"
} else {
    Write-Host "Could not find renderSuggestedTasks function"
}
