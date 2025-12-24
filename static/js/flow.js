$('.detailsentiment').empty();
$('.detailkeywords').empty();
$('.detailflows').empty();

document.getElementById('flowTitle').value = localStorage.getItem('titleForFlow');
document.getElementById('flowDescription').value = localStorage.getItem('descriptionForFlow');
document.getElementById('flowPicURL').value = localStorage.getItem('pictureForFlow');
document.getElementById('flowRefURL').value = localStorage.getItem('referenceForFlow');
var mycfs = localStorage.getItem('coreflowForFlow');
var s = document.getElementById("flowCoreFlowSelection");
for (var i = 0; i < s.options.length; i++) {
	if (mycfs != undefined)
	{
		cfs = mycfs.split(",");
		for (var j=0; j < cfs.length; j++)
		{
			currentselection = s.options[i].value;
			if (currentselection === cfs[j])
			{
				s.options[i].selected = "selected";
			}
		}
	}
}

var behaviours = localStorage.getItem('behavioursForFlow');
var b = document.getElementById("flowBehaviourSelection");
for (var i = 0; i < b.options.length; i++) {
	if (behaviours != undefined)
	{
		var beh = behaviours.split(",");
		for (var j=0; j < beh.length; j++)
		{
			if (b.options[i].value === beh[j])
			{
				b.options[i].selected = "selected";
			}
		}
	}
}

var risks = localStorage.getItem('risksForFlow');
var c = document.getElementById("flowRiskSelection");
for (var i = 0; i < c.options.length; i++) {
	if (risks != undefined)
	{
		ri = risks.split(",");
		for (var j=0; j < ri.length; j++)
		{
			if (c.options[i].value === ri[j])
			{
				c.options[i].selected = "selected";
			}
		}
	}
}

var upph = localStorage.getItem('upphaseForFlow');
var d = document.getElementById("flowUPSelection");
for (var i = 0; i < d.options.length; i++) {
	if (upph != undefined)
	{
		upp = upph.split(",");
		for (var j=0; j < upp.length; j++)
		{
			if (d.options[i].value === upp[j])
			{
				d.options[i].selected = "selected";
			}
		}
	}
}


document.getElementById('importJson').onclick = function() {
	console.log("here at import")
	var files = document.getElementById('file').files;
  console.log(files);
  if (files.length <= 0) {
    return false;
  }
  
  var fr = new FileReader();
  
  fr.onload = function(e) { 
  console.log(e);
    var result = JSON.parse(e.target.result);
	document.getElementById("flowTitle").value = result.title;
	document.getElementById("flowDescription").value = result.description;
	document.getElementById('flowPicURL').value = result.pictureURL;
	document.getElementById('flowRefURL').value = result.referenceURL;
	
	var mycfs = result.coreflows;
	var s = document.getElementById("flowCoreFlowSelection");
	for (var i = 0; i < s.options.length; i++) {
		s.options[i].selected = false;
		if (mycfs != undefined)
		{
			//cfs = mycfs.split(",");
			for (var j=0; j < mycfs.length; j++)
			{
				currentselection = s.options[i].value;
				if (currentselection === mycfs[j])
				{
					s.options[i].selected = "selected";
				}
			}
		}
	}
	$('#flowCoreFlowSelection').trigger('change');

	var behaviours = result.behaviours;
	var b = document.getElementById("flowBehaviourSelection");
	for (var i = 0; i < b.options.length; i++) {
		b.options[i].selected = false;
		if (behaviours != undefined)
		{
			//var beh = behaviours.split(",");
			for (var j=0; j < behaviours.length; j++)
			{
				if (b.options[i].value === behaviours[j])
				{
					b.options[i].selected = "selected";
				}
			}
		}
	}
	$('#flowBehaviourSelection').trigger('change');
	

	var risks = result.risks;
	var c = document.getElementById("flowRiskSelection");
	for (var i = 0; i < c.options.length; i++) {
		c.options[i].selected = false;
		if (risks != undefined)
		{
			//ri = risks.split(",");
			for (var j=0; j < risks.length; j++)
			{
				if (c.options[i].value === risks[j])
				{
					c.options[i].selected = "selected";
				}
			}
		}
	}
	$('#flowRiskSelection').trigger('change');

	var upph = result.upphases;
	var d = document.getElementById("flowUPSelection");
	for (var i = 0; i < d.options.length; i++) {
		d.options[i].selected = false;
		if (upph != undefined)
		{
			//upp = upph.split(",");
			for (var j=0; j < upph.length; j++)
			{
				if (d.options[i].value === upph[j])
				{
					d.options[i].selected = "selected";
				}
			}
		}
	}
	$('#flowUPSelection').trigger('change');
	
	
    //var formatted = JSON.stringify(result, null, 2);
	//console.log(formatted);
		//document.getElementById('result').value = formatted;
  }
  
  fr.readAsText(files.item(0));
};

document.getElementById('exportJson').onclick = function exportAsJson()
{
	console.log("here at export")
	var titletext = document.getElementById("flowTitle").value;
	var description = document.getElementById("flowDescription").value;
	var pic = document.getElementById("flowPicURL").value;
	var ref = document.getElementById("flowRefURL").value;
	
	var coreflows = [];
    var s = document.getElementById("flowCoreFlowSelection");
    for (var i = 0; i < s.options.length; i++) {
        if (s.options[i].selected == true) {
            var flowid = s.options[i].value;
            coreflows.push(flowid);
    	}
	}
	
	var behaviours = [];
    var b = document.getElementById("flowBehaviourSelection");
    for (var i = 0; i < b.options.length; i++) {
        if (b.options[i].selected == true) {
            var behavid = b.options[i].value;
            behaviours.push(behavid);
    	}
	}
	
	var risks = [];
    var c = document.getElementById("flowRiskSelection");
    for (var i = 0; i < c.options.length; i++) {
        if (c.options[i].selected == true) {
            var riskid = c.options[i].value;
            risks.push(riskid);
    	}
	}
	
	var upph = [];
    var d = document.getElementById("flowUPSelection");
    for (var i = 0; i < d.options.length; i++) {
        if (d.options[i].selected == true) {
            var upid = d.options[i].value;
            upph.push(upid);
    	}
	}

	var myObj = { "title":titletext, "description":description, "pictureURL": pic, "referenceURL": ref, "coreflows":coreflows, "behaviours":behaviours, "risks":risks, "upphases":upph};
	var myJSON = JSON.stringify(myObj);
	jsonPresentation = window.open("data:text/json," + encodeURIComponent(myJSON),
                       "_blank");
	jsonPresentation.focus();	
}

var timeoutId;
$('#flowTitle, #flowDescription, #flowPicURL, #flowRefURL').on('input propertychange change', function() {
    console.log('Textarea Change');
    
    clearTimeout(timeoutId);
    timeoutId = setTimeout(function() {
        // Runs 1 second (1000 ms) after the last change    
        saveData();
	}, 1000);
});

$('#flowCoreFlowSelection, #flowBehaviourSelection, #flowRiskSelection, #flowUPSelection').on('change', function() {
    console.log('Multiselect Change');
    
    clearTimeout(timeoutId);
    timeoutId = setTimeout(function() {
        // Runs 1 second (1000 ms) after the last change    
        saveData();
	}, 1000);
});
/**
document.getElementById('saveFlow').onclick = 
		**/
function saveData()
{
	var titletext = document.getElementById("flowTitle").value;
	var description = document.getElementById("flowDescription").value;
	var pic = document.getElementById("flowPicURL").value;
	var ref = document.getElementById("flowRefURL").value;
	
	var coreflows = [];
    var s = document.getElementById("flowCoreFlowSelection");
    for (var i = 0; i < s.options.length; i++) {
        if (s.options[i].selected == true) {
            var flowid = s.options[i].value;
            coreflows.push(flowid);
    	}
	}
	
	var behaviours = [];
    var b = document.getElementById("flowBehaviourSelection");
    for (var i = 0; i < b.options.length; i++) {
        if (b.options[i].selected == true) {
            var behavid = b.options[i].value;
            behaviours.push(behavid);
    	}
	}
	
	var risks = [];
    var c = document.getElementById("flowRiskSelection");
    for (var i = 0; i < c.options.length; i++) {
        if (c.options[i].selected == true) {
            var riskid = c.options[i].value;
            risks.push(riskid);
    	}
	}
	
	var upph = [];
    var d = document.getElementById("flowUPSelection");
    for (var i = 0; i < d.options.length; i++) {
        if (d.options[i].selected == true) {
            var upid = d.options[i].value;
            upph.push(upid);
    	}
	}
	localStorage.setItem("titleForFlow", titletext);
	localStorage.setItem("descriptionForFlow", description);
	localStorage.setItem("pictureForFlow", pic);
	localStorage.setItem("referenceForFlow", ref);
	localStorage.setItem("coreflowForFlow", coreflows);
	localStorage.setItem("behavioursForFlow", behaviours);
	localStorage.setItem("risksForFlow", risks);
	localStorage.setItem("upphaseForFlow", upph);
	
	console.log("saved")
	//alert("Flow successfully saved in local browser storage!");

}


function handleData(data) {
	console.log(data)
	$('.detailsentiment').empty();
	var mysentiment = data.sentiment;
	var senticon = "~";
	if (mysentiment < -0.3)
	{
		senticon = "-";
	}
	if (mysentiment > 0.3)
	{
		senticon = "+";
	}
	$('.detailsentiment').html('<span class="badge badge-warning mb-2">Sentiment: ' + mysentiment.toFixed(2) + ' ' + senticon + '</span>');
    
	var keywordsfound = false;
	var keyw = {};
	
	$('.detailkeywords').empty();
	
	keywords = data.keywords;
	if (keywords != undefined)
	{
		for (var i = 0; i < keywords.length; i++)
		{
			var aname = keywords[i][0];
			keyw[aname]=Math.round(Number(keywords[i][1]))*2;
		}
		var sortable = [];
		for (var keywo in keyw) {
		    sortable.push([keywo, keyw[keywo]]);
		}
		
		sortable.sort(function(first, second) {
		    return second[1] - first[1];
		});
		
		if(sortable.length > 0)
		{
			if (keywordsfound == false)
			{
				$('.detailkeywords').append('<b>Keywords:</b>');
				keywordsfound = true;
			}
		}
		
		for (var i = 0; i < sortable.length; i++)
		{
			key = sortable[i][0];
			console.log(key);
			$('.detailkeywords').append('<span class="badge badge-secondary ml-1">' + key + '(' + keyw[key] + ')</span>');
		}
	}
	$('.detailflows').empty();
	flowsfound = false;
	flows = data.flowranking;
	//if(sortable.length > 0)
	//{
		if(flows != undefined)
		{
			if (flowsfound == false)
			{
				$('.detailflows').append('<b>Related Reference Flows:</b>');
				$('.detailflows').append('<div id="accordion" role="tablist">');
				flowsfound = true;
			}
			for (var x = 0; x < 11; x++)
			{
				fl = flows[x][1][0];
				desc = flows[x][1][1];
				ref = flows[x][1][2];
				var id = fl.replace(/\s+/g,'');
				//$('.detailflows').append('<button type="button" onmouseover="handleMouseOver(this)" class="btn btn-sm btn-outline-info mt-1 mb-1 ml-1 mr-1">' + fl + '</button>');
				$('.detailflows').append('<div class="card"><div class="card-header" role="tab" id="'+ id + x +'"><h5 class="mb-0"><a data-toggle="collapse" href="#'+id+'" aria-expanded="true" aria-controls="'+ id +'">'+fl+'</a></h5></div>');
				$('.detailflows').append('<div id="'+id+'" class="collapse" role="tabpanel" aria-labelledby="'+ id + x +'" data-parent="#accordion"><div class="card-body">'+desc+' <a target="_blank" href=' + ref + '>Read more</a></div></div></div>');
			}
			$('.detailflows').append('</div>');
		}
		//}
	
}

function handleMouseOver(d)
{
	console.log(d.textContent);
}

document.getElementById('analyze').onclick = function(e) {
        e.preventDefault();
		console.log("analyze");
		var titletext = document.getElementById("flowTitle").value;
		var description = document.getElementById("flowDescription").value;
		var pic = document.getElementById("flowPicURL").value;
		var ref = document.getElementById("flowRefURL").value;
	
		var coreflows = [];
	    var s = document.getElementById("flowCoreFlowSelection");
	    for (var i = 0; i < s.options.length; i++) {
	        if (s.options[i].selected == true) {
	            var flowid = s.options[i].value;
	            coreflows.push(flowid);
	    	}
		}
	
		var behaviours = [];
	    var b = document.getElementById("flowBehaviourSelection");
	    for (var i = 0; i < b.options.length; i++) {
	        if (b.options[i].selected == true) {
	            var behavid = b.options[i].value;
	            behaviours.push(behavid);
	    	}
		}
	
		var risks = [];
	    var c = document.getElementById("flowRiskSelection");
	    for (var i = 0; i < c.options.length; i++) {
	        if (c.options[i].selected == true) {
	            var riskid = c.options[i].value;
	            risks.push(riskid);
	    	}
		}
	
		var upph = [];
	    var d = document.getElementById("flowUPSelection");
	    for (var i = 0; i < d.options.length; i++) {
	        if (d.options[i].selected == true) {
	            var upid = d.options[i].value;
	            upph.push(upid);
	    	}
		}

		var myObj = { "title":titletext, "description":description, "pictureURL": pic, "referenceURL": ref, "coreflows":coreflows, "behaviours":behaviours, "risks":risks, "upphases":upph};
		var myJSON = JSON.stringify(myObj);
		
		$.ajax({
		            url: '/analyze_flow',
		            type: 'POST',
					contentType:'application/json',
		            dataType: 'json',
		            success: handleData,
		            data: myJSON
		        });
};






