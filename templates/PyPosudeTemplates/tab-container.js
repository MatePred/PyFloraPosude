function openTab(event, tabId) {
  const tabPanes = document.getElementsByClassName('tab-pane');
  const tabButtons = document.getElementsByClassName('tab-button');

  for (let i = 0; i < tabButtons.length; i++) {
    tabButtons[i].classList.remove('active');
    tabPanes[i].classList.remove('active');
  }

  event.target.classList.add('active');
  document.getElementById(tabId).classList.add('active');
}
