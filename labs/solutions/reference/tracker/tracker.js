// Reference prototype of the training-room request tracker (Lab 4.3): the rules, with no page.
// Runs in a browser (window.Tracker) and in Node (require). Demo data only; nothing is stored.
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.Tracker = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  const ROOMS = ['قاعة أ', 'قاعة ب', 'قاعة ج'];
  const FIRST_HOUR = 8;
  const LAST_HOUR = 16;
  const COORDINATOR = 'منسقة التدريب';

  function createStore(options) {
    const checkConflict = !options || options.checkConflict !== false;
    const requests = [];
    let next = 1;

    function validate(r) {
      for (const field of ['by', 'room', 'day', 'from', 'to', 'purpose']) {
        if (r[field] === undefined || r[field] === null || r[field] === '') return 'حقل فارغ: ' + field;
      }
      if (!ROOMS.includes(r.room)) return 'قاعة غير موجودة';
      if (!Number.isInteger(r.from) || !Number.isInteger(r.to)) return 'الحجز بالساعة الكاملة';
      if (r.to <= r.from) return 'ساعة النهاية قبل ساعة البداية';
      if (r.from < FIRST_HOUR || r.to > LAST_HOUR) return 'ساعة خارج الدوام';
      return null;
    }

    function conflictWith(r) {
      return requests.find((x) => x.status !== 'مرفوض' && x.room === r.room && x.day === r.day && r.from < x.to && x.from < r.to);
    }

    function add(r) {
      const error = validate(r);
      if (error) return { ok: false, error };
      if (checkConflict) {
        const other = conflictWith(r);
        if (other) return { ok: false, error: `تعارض: ${r.room} محجوزة من الساعة ${other.from} إلى الساعة ${other.to}` };
      }
      const saved = { id: next++, status: 'جديد', ...r };
      requests.push(saved);
      return { ok: true, request: saved };
    }

    function listFor(user) {
      return requests.filter((r) => user.role === COORDINATOR || r.by === user.name).map((r) => ({ ...r }));
    }

    function decide(user, id, status) {
      if (user.role !== COORDINATOR) return { ok: false, error: 'الاعتماد للمنسقة فقط' };
      if (!['معتمد', 'مرفوض'].includes(status)) return { ok: false, error: 'حالة غير معروفة' };
      const r = requests.find((x) => x.id === id);
      if (!r) return { ok: false, error: 'طلب غير موجود' };
      r.status = status;
      return { ok: true, request: { ...r } };
    }

    return { add, listFor, decide, count: () => requests.length };
  }

  return { createStore, ROOMS, FIRST_HOUR, LAST_HOUR, COORDINATOR };
});
