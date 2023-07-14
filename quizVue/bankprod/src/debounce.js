export default function debounce(func, timeout = 300) {
  const timerStore = {};
  return (id, ...args) => {
    if (id in timerStore) {
      clearTimeout(timerStore[id]);
    }
    timerStore[id] = setTimeout(() => {
      func.apply(this, args);
    }, timeout);
  };
}
