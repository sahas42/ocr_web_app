const canvas = document.getElementById('drawCanvas');
const ctx = canvas.getContext('2d');
let drawing = false;

ctx.fillStyle = 'black';
ctx.fillRect(0, 0, canvas.width, canvas.height);

ctx.strokeStyle = 'white';
ctx.lineWidth = 20;
ctx.lineCap = 'round';

canvas.addEventListener('mousedown', () => drawing = true);
canvas.addEventListener('mouseup', () => { drawing = false; ctx.beginPath(); });
canvas.addEventListener('mouseout', () => { drawing = false; ctx.beginPath(); });
canvas.addEventListener('mousemove', draw);

canvas.addEventListener('touchstart', e => { e.preventDefault(); drawing = true; });
canvas.addEventListener('touchend',   e => { e.preventDefault(); drawing = false; ctx.beginPath(); });
canvas.addEventListener('touchmove',  e => { e.preventDefault(); drawTouch(e); });

function draw(e) {
  if (!drawing) return;
  const rect = canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  ctx.lineTo(x, y);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x, y);
}

function drawTouch(e) {
  if (!drawing) return;
  const rect = canvas.getBoundingClientRect();
  const touch = e.touches[0];
  const x = touch.clientX - rect.left;
  const y = touch.clientY - rect.top;
  ctx.lineTo(x, y);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x, y);
}

document.getElementById('clearBtn').onclick = () => {
  ctx.fillRect(0, 0, canvas.width, canvas.height);
};

document.getElementById('predictBtn').onclick = async () => {
  const dataURL = canvas.toDataURL('image/png');
  const resp = await fetch('/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: dataURL })
  });
  const { prediction } = await resp.json();
  document.getElementById('result').innerText = `Prediction: ${prediction}`;
};

document.getElementById('showImg').onclick = async () => {
  const dataURL = canvas.toDataURL('image/png');
  const resp = await fetch('/show-img', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: dataURL })
  });
  blob = await resp.blob();
  const imageUrl = URL.createObjectURL(blob);
  document.getElementById('processedImg').src = imageUrl;

};
