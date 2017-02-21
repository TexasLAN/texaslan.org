/* Project specific Javascript goes here. */
main();

function main() {
    footerUpdate()
}

window.onresize = function(event) {
    footerUpdate()
};

function footerUpdate() {
    var footerHeight = document.getElementsByTagName("footer")[0].clientHeight;
    var body = document.getElementsByTagName("body")[0];
    body.style.marginBottom = footerHeight + "px";
}
