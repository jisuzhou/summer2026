const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const match = html.match(/<script>([\s\S]*?)<\/script>/);
if (match) {
  try {
    new Function(match[1]);
    console.log('✅ JS syntax OK');
  } catch (e) {
    console.log('❌ JS syntax error:', e.message);
    // Find the line number
    const lines = match[1].split('\n');
    const lineMatch = e.message.match(/(\d+)/);
    if (lineMatch) {
      const lineNum = parseInt(lineMatch[1]);
      console.log(`Near line ${lineNum}:`);
      console.log(lines.slice(Math.max(0, lineNum - 3), lineNum + 2).join('\n'));
    }
  }
} else {
  console.log('No script tag found');
}
