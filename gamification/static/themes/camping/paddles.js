var paddles = {canvas:null, $canvas:null, ctx:null, loadedImages:0, loadedArray:[]};
paddles.imageArray = "canoe_green_sideways.png oar.png".split(" ");
paddles.imageUrlPrefix = "/static/themes/camping/";

paddles.init = function(){
    //Initialization

    paddles.$canvas = $('<canvas>')
        .attr({width:1000,height:220,id:'badge_data_canvas'})
        .text("This graph doesn't show on your browser")
        .prependTo($('#leader_board'));

    paddles.canvas = document.getElementById('badge_data_canvas');
    if (paddles.canvas && paddles.canvas.getContext){
        paddles.ctx = paddles.canvas.getContext('2d');
        paddles.preloadImages();
    } else {
        console.log("No Canvas Support");
        if (paddles.$canvas) paddles.$canvas.hide();
    }
};

paddles.preloadImages = function() {
    for (var i = 0; i < paddles.imageArray.length; i++) {
        paddles.loadedArray[i] = new Image();
        paddles.loadedArray[i].addEventListener("load", paddles.trackProgress, true);
        var url = paddles.imageArray[i];
        if (document.location.host != "") url = paddles.imageUrlPrefix + url;
        paddles.loadedArray[i].src = url;
    }
};

paddles.trackProgress = function() {
    paddles.loadedImages++;
    if (paddles.loadedImages == paddles.imageArray.length) {
        paddles.imagesLoaded();
    }
};

paddles.imagesLoaded = function() {
    //Run after all images are ready
    //TODO: Pass a list of visualization types and call appropriately with proper data
    paddles.draw_canoe_and_oars(project_info.badge_json || []);
};

paddles.draw_canoe_and_oars = function(badge_info){
    //Shortcuts
    var ctx = paddles.ctx;
    var canoe = paddles.loadedArray[0];
    var oar = paddles.loadedArray[1];

    var canvas_width = paddles.canvas.width;
    var canvas_height = paddles.canvas.height;

    //Variables
    var canvas_spacing = 50;
    var canoe_spacing = 15;
    var canoe_spacing_right = 25;
    var canoe_width = canvas_width-(canvas_spacing*2);
    var canoe_height = 200 / (1460/canoe_width);
    var oar_width = 70;
    var num_oars = 20;
    if (badge_info && badge_info.length < num_oars) num_oars = badge_info.length;
    if (num_oars < 2) num_oars = 2;

    var oar_spacing = parseInt((canoe_width-canvas_spacing-canoe_spacing_right-(canoe_spacing/2)) / (num_oars-1));
    ctx.font="bold 12px Verdana";

    var badges_max=0;
    var badges_min=100000000;
    var points_max=0;
    var points_min=100000000;

    for (var i=0;i<num_oars;i++){
        var badge = badge_info[i];
        var awards = badge[1].length;
        var points = badge[2] || parseInt(awards*1.5) || 1;
        if (awards>badges_max) badges_max=awards;
        if (awards<badges_min) badges_min=awards;
        if (points>points_max) points_max=points;
        if (points<points_min) points_min=points;
    }

    //Draw the oars
    for (var i=0;i<num_oars;i++){
        var badge = badge_info[i];
        var awards = badge[1].length;
        var points = badge[2] || parseInt(awards*1.5) || 1;
        var name = paddles.nameFormat(badge[0] || "Unknown");

        var oar_size = maths.sizeFromAmountRange(oar_width*0.75,oar_width*1.8,points,points_min,points_max);

        //Draw the Oar
        var oar_x = canvas_spacing+canoe_spacing+(i*oar_spacing);
        var oar_y = 70 + maths.heightOnSin(0,1,i,num_oars-1,30);
        ctx.drawImage(oar,oar_x,oar_y,oar_size,oar_size);


        //Save oar location, and draw user name
        ctx.save();
        ctx.translate(oar_x+oar_size, oar_y+3);
        ctx.rotate(-Math.PI/4);
        ctx.textAlign = "left";
        ctx.fillText(name, 0, 0);


        //Draw Meatball
        var mb_spacing = maths.sizeFromAmountRange(15,25,points,points_min,points_max);
        ctx.beginPath();
        ctx.arc(-mb_spacing, -3, mb_spacing/2, 0, 2 * Math.PI, false);
        var bgColor = maths.colorBlendFromAmountRange('#00ff00','#660000',points,points_min,points_max);
        ctx.fillStyle = bgColor;
        ctx.fill();
        ctx.lineWidth = 1;
        ctx.strokeStyle = '#003300';
        ctx.stroke();

        //Draw Meatball text
        ctx.fillStyle = maths.idealTextColor(bgColor);
        ctx.textAlign = "center";
        ctx.font="bold "+(1+mb_spacing/2)+"px Verdana";
        var meatball =  points;
        ctx.fillText(meatball, -mb_spacing, 1);

        ctx.restore();

    }

    ctx.drawImage(canoe,50,100,canoe_width,canoe_height);

    ctx.translate(canoe_width+30, 140);
    ctx.fillStyle = "white";
    ctx.rotate(-Math.PI/16);
    ctx.textAlign = "right";
    ctx.font="bold 16px Verdana";
    ctx.fillText(project_info.name, 0, 0);

};
paddles.nameFormat = function(name){
    var lenName = name.length;
    return name.substring(0,1).toUpperCase() + name.substring(1,lenName-1)+ name.substring(lenName-1,lenName).toUpperCase();
};

$(document).ready(paddles.init);