function renderTooltips(spaces, spaceTipTemplate, monitorTipTemplate) {

    function renderTooltip(data) {
        const templateData = {data: data};
        _.templateSettings.variable = "data";
        return spaceTipTemplate(templateData)
    }

    function renderMonitorTooltip(data) {
        const templateData = {data: data};
        _.templateSettings.variable = "data";
        return monitorTipTemplate(templateData)

    }

    for (let i = 0; i < spaces.length; i++) {
        const space = spaces[i];
        const classes = space.className;

        let tooltipContent;
        if (classes.includes("monitor")) {
            const data = extractData(space);
            tooltipContent = renderMonitorTooltip(data);
        } else {
            const data = extractData(space);
            tooltipContent = renderTooltip(data);
        }

        $(space).tooltipster({
            content: $(tooltipContent),
            theme: "tooltip",
            speed: 200,
            trigger: "hover",
            // Using the click trigger may be helpful for debugging styles
            //trigger: "click"
        });
    }
}

function extractData(space) {
    return space.dataset;
}


