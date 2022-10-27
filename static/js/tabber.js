(function() {
  function changeTab(tab, tabName) {
    document.querySelector('.tabber__tab.active').classList.remove('active');
    tab.classList.add('active');
    document.querySelector('.tabber__content>.active').classList.remove('active');
    document.querySelector('.tabber__content>#'+tabName).classList.add('active');
  }

  document.querySelectorAll('.tabber__tab').forEach(tab => {
    tab.onclick = () => {
      const tabName = tab.innerText.toLowerCase().replaceAll(' ', '-');
      changeTab(tab, tabName);
    }
  });

  if (location.hash != '' && !!document.querySelector('.tabber')) {
    document.querySelectorAll('.tabber__tab').forEach(tab => {
      const tabName = tab.innerText.toLowerCase().replaceAll(' ', '-');
      if (tabName == location.hash.slice(1)) {
        changeTab(tab, tabName);
      }
    });
  }
})();
