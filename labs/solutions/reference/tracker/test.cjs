// The three acceptance checks of the requirements document, run against the tracker's rules.
//   node test.cjs            the reference prototype
//   node test.cjs --first    the builder's first version (the stand-in: it does not check conflicts)
const Tracker = require('./tracker.js');
const first = process.argv.includes('--first');
const employee = { name: 'ماجد', role: 'موظف' };
const other = { name: 'لمى', role: 'موظف' };
const coordinator = { name: 'سارة', role: Tracker.COORDINATOR };
const base = { room: 'قاعة أ', day: 'الأحد', purpose: 'تدريب البوابة' };
const results = [];
const check = (name, fn) => {
  const store = Tracker.createStore({ checkConflict: !first });
  let ok = false;
  let detail = '';
  try {
    detail = fn(store) || '';
    ok = detail === '';
  } catch (e) {
    detail = String(e.message || e);
  }
  results.push(ok);
  console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${detail ? ': ' + detail : ''}`);
};

check('check 1, no double booking', (s) => {
  if (!s.add({ ...base, by: employee.name, from: 9, to: 11 }).ok) return 'the first request was refused';
  const second = s.add({ ...base, by: other.name, from: 10, to: 12 });
  if (second.ok) return 'an overlapping request for the same room was accepted';
  if (!second.error.includes('تعارض')) return 'the refusal does not name the conflict';
  if (s.count() !== 1) return 'the refused request was recorded';
  if (!s.add({ ...base, by: other.name, from: 11, to: 12 }).ok) return 'a request that starts when the first ends was refused';
  if (!s.add({ ...base, room: 'قاعة ب', by: other.name, from: 9, to: 11 }).ok) return 'another room at the same hours was refused';
});

check('check 2, wrong inputs', (s) => {
  const wrong = [
    ['end before start', { ...base, by: employee.name, from: 11, to: 9 }, 'النهاية'],
    ['outside working hours', { ...base, by: employee.name, from: 6, to: 9 }, 'خارج الدوام'],
    ['unknown room', { ...base, room: 'قاعة د', by: employee.name, from: 9, to: 10 }, 'غير موجودة'],
    ['empty field', { ...base, by: employee.name, from: 9, to: 10, purpose: '' }, 'فارغ'],
  ];
  for (const [label, request, word] of wrong) {
    const r = s.add(request);
    if (r.ok) return `${label} was accepted`;
    if (!r.error.includes(word)) return `${label}: the message does not name the error`;
  }
  if (s.count() !== 0) return 'a wrong request was recorded';
});

check('check 3, roles', (s) => {
  const mine = s.add({ ...base, by: employee.name, from: 9, to: 10 }).request;
  s.add({ ...base, by: other.name, from: 12, to: 13 });
  const seen = s.listFor(employee);
  if (seen.length !== 1 || seen[0].by !== employee.name) return 'an employee sees requests of others';
  if (s.decide(employee, mine.id, 'معتمد').ok) return 'an employee approved a request';
  if (s.listFor(coordinator).length !== 2) return 'the coordinator does not see every request';
  const decided = s.decide(coordinator, mine.id, 'معتمد');
  if (!decided.ok || s.listFor(employee)[0].status !== 'معتمد') return 'the approval did not change the status';
});

const passed = results.filter(Boolean).length;
console.log(`${passed} of ${results.length} checks pass (${first ? 'first version' : 'reference prototype'})`);
process.exit(passed === results.length ? 0 : 1);
