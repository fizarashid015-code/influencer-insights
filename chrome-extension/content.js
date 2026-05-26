function scrapeComments() {
  const els = document.querySelectorAll('#content-text');
  return Array.from(els).map(el => el.innerText).slice(0, 20);
}