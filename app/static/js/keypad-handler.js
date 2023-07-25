const itemIDInput = document.getElementById('item-id');
const keypad = document.getElementById('keypad');
const keypadKeys = keypad.querySelectorAll('.key');

itemIDInput.addEventListener('focus', showKeypad);
itemIDInput.addEventListener('blur', hideKeypad);

keypadKeys.forEach((key) => {
  key.addEventListener('click', handleKeypadKey);
});

function showKeypad() {
  keypad.style.display = 'block';
}

function hideKeypad() {
  keypad.style.display = 'block';
}

function handleKeypadKey(event) {
  const key = event.target;
  const digit = key.textContent;

  if (digit === 'Delete') {
    deleteDigit();
  } else {
    appendDigit(digit);
  }
}

function appendDigit(digit) {
  itemIDInput.value += digit;
}

function deleteDigit() {
  itemIDInput.value = itemIDInput.value.slice(0, -1);
}