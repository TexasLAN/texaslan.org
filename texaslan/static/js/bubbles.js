minRadius = 20;
maxRadius = 45;
MAX_VELOCITY = 0.5;
maxNumberOfCircles = 15;
circleColor = '#FFFFFF';

var canvas = document.getElementById('bubbles');
var container = document.getElementById('labs-head');
var circles;
var ctx;
main();

function main() {
    updateCanvasDimensions();
    circles = new Array(maxNumberOfCircles);
    ctx = canvas.getContext('2d');

    // Spread out the initial spawning of bubbles
    for (i = 0; i < maxNumberOfCircles; i++) {
        setTimeout(generateBubbleCreatingFuction(i), Math.random() * 20000)
    }

    // Begin the animation loop
    animate()
}

// Required due to closure capture semantics (variables are function scoped)
function generateBubbleCreatingFuction(i) {
    return function () {
        circles[i] = buildCircle();
    }
}

// Calculates new positions and renders all circles
function animate(timestamp) {
    requestID = requestAnimationFrame(animate);
    updateCanvasDimensions();

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (var i = 0; i < maxNumberOfCircles; i++) {
        var circle = circles[i];
        if (typeof circle == "undefined") {
            continue
        }
        circle.x = circle.x + -Math.sin(circle.t / 100) * circle.xVel;
        circle.y = circle.y + -circle.yVel;

        abovescreen = circle.y < 0 - circle.radius;
        if (abovescreen) {
            circles[i] = buildCircle();
        }
        drawCircle(ctx, circles[i]);
    }
}


function buildCircle() {
    var circle = {};
    circle.radius = randomXToY(minRadius, maxRadius);

    //ANYWHERE ON THE X AXIS
    circle.x = Math.random() * canvas.width;
    circle.y = canvas.height + circle.radius;
    circle.xVel = Math.random() * (MAX_VELOCITY / 0.5 ) + 0.1;
    circle.yVel = Math.random() * MAX_VELOCITY + 1.0;
    circle.t = Math.random() * 20;

    return circle
}

var timeAlphaScale = 1 / 3000;
var twoPi = Math.PI * 2.0;
//Render the circle onto the context
function drawCircle(ctx, circle) {
    ctx.beginPath();
    ctx.globalAlpha = Math.max(.16 - circle.t * timeAlphaScale, 0);
    ctx.fillStyle = circleColor;
    ctx.arc(circle.x, circle.y, circle.radius, 0, twoPi, false);
    ctx.fill();
    ctx.closePath();
    circle.t++;
}

function betweenZeroAnd(num) {
    return Math.floor(Math.random() * (num))
}

function updateCanvasDimensions() {
    height = canvas.clientHeight;
    width = canvas.clientWidth;
    canvas.height = height;
    canvas.width = width
}

function randomXToY(minVal, maxVal, floatVal) {
    var randVal = minVal + (Math.random() * (maxVal - minVal));
    return typeof floatVal == 'undefined' ? Math.round(randVal) : randVal.toFixed(floatVal);
}
