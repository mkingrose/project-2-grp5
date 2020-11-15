// set the dimensions and margins of the graph
var margin = { top: 10, right: 30, bottom: 30, left: 60 },
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#scatterplotscript")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

//Read the data
d3.csv("merged.csv", function (data) {

    // Add X axis
    var x = d3.scaleLinear()
        .domain([2009, 2019])
        .range([0, width]);

    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
        .domain([0, 1000])
        .range([height, 0]);
    svg.append("g")
        .call(d3.axisLeft(y));

    // text label for the x and y axis
    svg.append("text")
        .attr("class", "x label")
        .attr("text-anchor", "end")
        .attr("x", width)
        .attr("y", height - 6)
        .text("Year");

    svg.append("text")
        .attr("class", "y label")
        .attr("text-anchor", "end")
        .attr("y", 6)
        .attr("dy", ".75em")
        .attr("transform", "rotate(-90)")
        .text("New Displacements");


    // Color scale: give me a specie name, I return a color
    var color = d3.scaleOrdinal()
        // Use the 2 hazard categories and 2 of the color options.
        .domain(['Weather related', 'Geophysical'])
        .range(["#440154ff", "#21908dff"]);


    // Add dots
    var myCircle = svg.append('g')
        .selectAll("circle")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", function (d) { return x(d.Year); })  // Updated to use the column names from merged.csv here and next few lines.
        .attr("cy", function (d) { return y(d.New_Displacements); })
        .attr("r", 8)
        .style("fill", function (d) { return color(d.Hazard_Category) })
        .style("opacity", 0.5);

    // Add brushing
    svg
        .call(d3.brush()                 // Add the brush feature using the d3.brush function
            .extent([[0, 0], [width, height]]) // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
            .on("start brush", updateChart) // Each time the brush selection changes, trigger the 'updateChart' function
        )

    // Function that is triggered when brushing is performed
    function updateChart() {
        extent = d3.event.selection
        // Also updated to use the column names from merged.csv
        myCircle.classed("selected", function (d) { return isBrushed(extent, x(d.Year), y(d.New_Displacements)) })
    }

    // A function that return TRUE or FALSE according if a dot is in the selection or not
    function isBrushed(brush_coords, cx, cy) {
        var x0 = brush_coords[0][0],
            x1 = brush_coords[1][0],
            y0 = brush_coords[0][1],
            y1 = brush_coords[1][1];
        return x0 <= cx && cx <= x1 && y0 <= cy && cy <= y1;    // This return TRUE or FALSE depending on if the points is in the selected area
    }

})
