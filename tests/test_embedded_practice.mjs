// Mocked, network-free checks of the Academy's actual embedded-practice functions.
// The browser DOM is substituted only to exercise source selection and stale navigation.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const js = readFileSync(resolve(ROOT, 'app.js'), 'utf8');
const begin = js.indexOf('let embeddedPracticeMapPromise=null;');
const end = js.indexOf('function nav(){', begin);
assert.ok(begin >= 0 && end > begin, 'Expected original embedded-practice integration exists.');
const helper = js.slice(begin, end);
const source = 'core-lesson-guided-practice-2026.json';
const mapping = JSON.parse(readFileSync(resolve(ROOT, 'lesson-practical-title-map-2026.json'), 'utf8'));
const catalog = JSON.parse(readFileSync(resolve(ROOT, source), 'utf8'));
const first = catalog.units[0];
assert.ok(mapping.mappings.some(m => m.course === first.course && m.lesson === first.lesson));

const elements = new Map();
const element = id => {
  if (!elements.has(id)) elements.set(id, { innerHTML: '', textContent: '' });
  return elements.get(id);
};
const requests = [];
const ctx = {
  catalog: { courses: [{ title: first.course, lessons: [[first.lesson]] }] },
  courseIndex: 0,
  lessonIndex: 0,
  screen: 'lesson',
  document: { getElementById: element },
  safe: s => String(s).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;'),
  fetch: async url => {
    requests.push(url);
    if (url.endsWith('lesson-practical-title-map-2026.json'))
      return { ok: true, json: async () => mapping };
    if (url.endsWith(source))
      return { ok: true, json: async () => catalog };
    throw Error('Unexpected fetched source ' + url);
  },
};
vm.createContext(ctx);
vm.runInContext(helper, ctx, { filename: 'app-embedded-practice.js' });
await ctx.loadEmbeddedPracticeForLesson(0, 0);
assert.match(element('academy-embedded-practice').innerHTML, /CURATED PRACTICAL EXTENSION/);
assert.ok(element('academy-embedded-practice').innerHTML.includes(first.title));
assert.deepEqual(requests, ['./lesson-practical-title-map-2026.json', './' + source],
  'Mapped lesson must fetch only its assigned source catalog');

// Repeated visit should use cached source, not refetch a large catalog.
await ctx.loadEmbeddedPracticeForLesson(0, 0);
assert.equal(requests.length, 2, 'Second visit must use the cached practice catalog.');

// Unknown lesson should say it is unmapped rather than show unrelated practice.
ctx.catalog.courses[0].lessons[0] = ['A brand-new lesson with no practical mapping'];
element('academy-embedded-practice').innerHTML = '';
await ctx.loadEmbeddedPracticeForLesson(0, 0);
assert.match(element('academy-embedded-practice').innerHTML, /not been reviewed for this exact lesson/);
assert.ok(!element('academy-embedded-practice').innerHTML.includes('CURATED PRACTICAL EXTENSION'));

// A title that happens to contain HTML characters must be escaped before DOM insertion.
const sampleUnit = JSON.parse(JSON.stringify(first));
sampleUnit.title = '<img src=x onerror=alert(1)>';
const markup = ctx.embeddedPracticeSectionHTML(sampleUnit.sections[0], sampleUnit, 'Test <lesson>');
assert.ok(markup.includes('&lt;img'));
assert.ok(!markup.includes('<img'));
assert.ok(markup.includes('Test &lt;lesson&gt;'));

// A stale promise should never replace practice for a lesson the user left.
let release;
const gate = new Promise(done => { release = done; });
const staleElement = { innerHTML: 'New lesson content', textContent: '' };
ctx.document.getElementById = () => staleElement;
ctx.catalog.courses[0].lessons[0] = [first.lesson];
ctx.lessonIndex = 0;
ctx.fetch = async url => {
  if (url.includes('lesson-practical-title-map-2026.json')) return {ok:true,json:async()=>mapping};
  await gate;
  return {ok:true,json:async()=>catalog};
};
vm.runInContext('embeddedPracticeCatalogs.clear();', ctx);
const promise = ctx.loadEmbeddedPracticeForLesson(0, 0);
ctx.lessonIndex = 1;
release();
await promise;
assert.equal(staleElement.innerHTML, 'New lesson content');

console.log('Embedded practice checks passed: matching, source fetching, caching, fallback, HTML escaping, stale navigation.');
