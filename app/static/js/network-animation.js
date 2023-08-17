
// Random number generator function (excluding excludedIndices)
function getRandomIndex(max, excludedIndices = []) {
  let index;
  do {
    index = Math.floor(Math.random() * max);
  } while (excludedIndices.includes(index));
  return index;
}

// Random number generator function
function getRandomPosition(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}


function drawAnimationNetwork (){

    const svg = document.querySelector('.network-animation');
    const numCircles = 20;
    const circles = [];

    for (let i = 0; i < numCircles; i++) {
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('class', 'circle');
    circle.setAttribute('r', '6');
    circle.setAttribute('cx', getRandomPosition(0, 1000));
    circle.setAttribute('cy', getRandomPosition(0, 1000));
    svg.appendChild(circle);
    circles.push(circle);
    }

// Generate lines connecting circles
    const numLines = 5;

    for (let i = 0; i < numLines; i++) {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('class', 'line');

        const startCircleIndex = getRandomIndex(numCircles);
        const endCircleIndex = getRandomIndex(numCircles, [startCircleIndex]);

        line.setAttribute('x1', circles[startCircleIndex].getAttribute('cx'));
        line.setAttribute('y1', circles[startCircleIndex].getAttribute('cy'));
        line.setAttribute('x2', circles[endCircleIndex].getAttribute('cx'));
        line.setAttribute('y2', circles[endCircleIndex].getAttribute('cy'));

        svg.appendChild(line);
    }
    
}

drawAnimationNetwork();


