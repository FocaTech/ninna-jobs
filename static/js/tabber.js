(function() {
  function changeTab(tab, tabName) {
    ['.tabber__tab', '.tabber__content>']
    .map(selector => document.querySelector(selector+'.active'))
    .forEach(element => { if (!!element) element.classList.remove('active') });
    tab.classList.add('active');
    document.querySelector('.tabber__content>#'+tabName).classList.add('active');
  }

  document.querySelectorAll('.tabber__tab').forEach(tab => {
    tab.onclick = () => {
      const tabName = tab.innerText.toLowerCase().replaceAll(' ', '-');
      changeTab(tab, tabName);
    }
  });

  if (location.search != '' && !!document.querySelector('.tabber')) {
    document.querySelectorAll('.tabber__tab').forEach(tab => {
      const tabName = tab.innerText.toLowerCase().replaceAll(' ', '-');
      if (tabName == location.search.slice(1)) {
        changeTab(tab, tabName);
      }
    });
  }

  (function() {
    let tab = ['.tabber__tab', '.tabber__content>section'];
    tab = [
      tab.map(selector => document.querySelector(selector)),
      tab.map(selector => document.querySelector(selector+'.active'))
    ];
    if (!!tab[0][0] && !tab[1][0] || !!tab[0][1] && !tab[1][1]) tab[0][0].click();
  })();
})();
