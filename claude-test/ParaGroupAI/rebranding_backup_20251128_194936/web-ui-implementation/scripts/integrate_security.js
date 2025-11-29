const fs = require('fs');
const path = require('path');

console.log('🔧 Starting security integration...\n');

// Routes to enhance
const routes = [
  'src/pages/api/auth/me.ts',
  'src/pages/api/auth/callback.ts',
  'src/pages/api/auth/validate.ts',
  'src/pages/api/auth/logout.ts',
  'src/pages/api/query.ts'
];

let successCount = 0;
let skipCount = 0;

routes.forEach(routePath => {
  const fullPath = path.join(__dirname, '..', routePath);

  if (!fs.existsSync(fullPath)) {
    console.log(`⚠️  Skipping ${routePath} - file not found`);
    skipCount++;
    return;
  }

  let content = fs.readFileSync(fullPath, 'utf8');

  // Check if already integrated
  if (content.includes('securityLogger')) {
    console.log(`✅ ${routePath} - already has security logging (skipping)`);
    skipCount++;
    return;
  }

  // Add security imports at the top (after existing imports)
  const importIndex = content.lastIndexOf("import");
  if (importIndex === -1) {
    console.log(`⚠️  Could not find imports in ${routePath} - skipping`);
    skipCount++;
    return;
  }

  const importEndIndex = content.indexOf(';', importIndex) + 1;
  const beforeImports = content.substring(0, importEndIndex);
  const afterImports = content.substring(importEndIndex);

  const securityImports = `\n\n// ✅ OWASP Security Integration (Added ${new Date().toISOString().split('T')[0]})\nimport { securityLogger, SecurityEvent } from '@/lib/security/logging';\n`;

  const newContent = beforeImports + securityImports + afterImports;

  // Write updated content
  fs.writeFileSync(fullPath, newContent, 'utf8');
  console.log(`✅ ${routePath} - added security imports`);
  successCount++;
});

console.log(`\n📊 Integration Summary:`);
console.log(`   ✅ Enhanced: ${successCount} routes`);
console.log(`   ⏭️  Skipped: ${skipCount} routes`);
console.log(`\n✅ Security integration complete!\n`);

process.exit(0);
