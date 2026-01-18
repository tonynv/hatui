import nunjucks from 'nunjucks';
import { marked } from 'marked';
import yaml from 'js-yaml';
import matter from 'gray-matter';
import { glob } from 'glob';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

// Configure Nunjucks
const env = nunjucks.configure(path.join(ROOT, 'app/templates'), {
  autoescape: true,
  noCache: process.env.NODE_ENV !== 'production'
});

// Custom Filters
env.addFilter('md', (str) => {
  if (!str) return '';
  return marked.parse(str);
});

env.addFilter('date', (str, format) => {
  const d = new Date(str);
  if (format === 'short') {
    return d.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
  }
  return d.toLocaleDateString('en-US', { dateStyle: 'long' });
});

// Load site config
async function loadConfig() {
  const configPath = path.join(ROOT, 'content/config.yaml');
  const content = await fs.readFile(configPath, 'utf-8');
  return yaml.load(content);
}

// Load documentation pages
async function loadPages() {
  const pagesDir = path.join(ROOT, 'content/pages');
  const mdFiles = await glob(`${pagesDir}/*.md`);

  const pages = [];

  for (const mdPath of mdFiles) {
    const content = await fs.readFile(mdPath, 'utf-8');
    const { data, content: markdown } = matter(content);

    pages.push({
      ...data,
      content: marked.parse(markdown),
      slug: path.basename(mdPath, '.md')
    });
  }

  // Sort by order field
  pages.sort((a, b) => (a.order || 99) - (b.order || 99));

  return pages;
}

// Write HTML file
async function writeHtml(outputPath, html) {
  const dir = path.dirname(outputPath);
  await fs.mkdir(dir, { recursive: true });
  await fs.writeFile(outputPath, html);
  console.log(`  ✓ ${outputPath.replace(ROOT + '/', '')}`);
}

// Copy styles
async function copyStyles() {
  const srcPath = path.join(ROOT, 'app/styles/main.css');
  const destPath = path.join(ROOT, 'dist/styles/main.css');
  await fs.mkdir(path.dirname(destPath), { recursive: true });
  await fs.copyFile(srcPath, destPath);
  console.log('  ✓ dist/styles/main.css');
}

// Copy scripts
async function copyScripts() {
  const srcPath = path.join(ROOT, 'app/scripts/main.js');
  const destPath = path.join(ROOT, 'dist/scripts/main.js');
  await fs.mkdir(path.dirname(destPath), { recursive: true });
  await fs.copyFile(srcPath, destPath);
  console.log('  ✓ dist/scripts/main.js');
}

// Copy static assets
async function copyStatic() {
  const srcDir = path.join(ROOT, 'app/static');
  const destDir = path.join(ROOT, 'dist');

  try {
    const files = await glob(`${srcDir}/**/*`, { nodir: true });
    for (const file of files) {
      const relativePath = path.relative(srcDir, file);
      const destPath = path.join(destDir, relativePath);
      await fs.mkdir(path.dirname(destPath), { recursive: true });
      await fs.copyFile(file, destPath);
    }
    if (files.length > 0) {
      console.log(`  ✓ Copied ${files.length} static files`);
    }
  } catch {
    // Static dir might not exist or be empty
  }
}

// Main build function
async function build() {
  console.log('\n═══════════════════════════════════════════════');
  console.log('  Building HATUI Documentation');
  console.log('═══════════════════════════════════════════════\n');

  const config = await loadConfig();
  const pages = await loadPages();

  const context = { config, pages };

  // Ensure dist directory
  await fs.mkdir(path.join(ROOT, 'dist'), { recursive: true });

  console.log('Rendering pages...');

  // Render index
  const indexHtml = nunjucks.render('index.njk', context);
  await writeHtml(path.join(ROOT, 'dist/index.html'), indexHtml);

  // Render each documentation page
  for (const page of pages) {
    const pageHtml = nunjucks.render('page.njk', {
      ...context,
      page,
      current_page: page.slug
    });
    await writeHtml(path.join(ROOT, `dist/${page.slug}/index.html`), pageHtml);
  }

  console.log('\nCopying assets...');
  await copyStyles();
  await copyScripts();
  await copyStatic();

  console.log('\n═══════════════════════════════════════════════');
  console.log(`  Build complete! ${pages.length + 1} pages rendered.`);
  console.log('═══════════════════════════════════════════════\n');
}

// Run build
build().catch(console.error);
