import { spawn } from 'child_process';
import chokidar from 'chokidar';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

// Initial build
console.log('Building site...');
const build = spawn('node', [path.join(__dirname, 'render.js')], { stdio: 'inherit' });

build.on('close', (code) => {
  if (code !== 0) {
    console.error('Build failed');
    process.exit(1);
  }

  // Start Vite dev server
  console.log('\nStarting dev server...');
  const vite = spawn('npx', ['vite', '--host'], {
    cwd: ROOT,
    stdio: 'inherit',
    shell: true
  });

  // Watch for changes
  const watcher = chokidar.watch([
    path.join(ROOT, 'app/**/*'),
    path.join(ROOT, 'content/**/*')
  ], {
    ignoreInitial: true
  });

  watcher.on('all', (event, filePath) => {
    console.log(`\n[${event}] ${path.relative(ROOT, filePath)}`);
    console.log('Rebuilding...');

    const rebuild = spawn('node', [path.join(__dirname, 'render.js')], { stdio: 'inherit' });
    rebuild.on('close', () => {
      console.log('Rebuild complete\n');
    });
  });

  // Cleanup on exit
  process.on('SIGINT', () => {
    watcher.close();
    vite.kill();
    process.exit();
  });
});
