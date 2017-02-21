let loneMatch;

function filterMachines(machines, filterString) {
    $.each(machines, function (index, machine) {
        machine = $(machine);
        const name = machine.data("name");
        const match = name.indexOf(filterString) > -1;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
        if (!match) {
            machine.addClass("no-match")
        } else {
            machine.removeClass("no-match")
        }
    });
    const results = $(".machine").not(".no-match");
    if (results.length == 1) {
        loneMatch = results[0];
        $(loneMatch).tooltipster('show');
    } else {
        if (loneMatch) {
            $(loneMatch).tooltipster('hide');
        }
    }
}
