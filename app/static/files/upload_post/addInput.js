var ingre_counter = 1;
var limit = 500;
function ingedInput(divName){
     if (ingre_counter == limit)  {
          alert("You have reached the limit of adding " + ingre_counter + " inputs");
     }
     else {
          var newdiv = document.createElement('div');
          var num = (ingre_counter+1)
          newdiv.id = "ingre_" + num.toString();
          newdiv.innerHTML = "<br>"+"<div class= 'w3-col w3-container w3-large w3-margin-top w3-margin-right' style='width:3%'>" + (ingre_counter+1) + "." + "</div>" + "<input class='w3-col w3-input w3-border w3-margin-bottom' style='width:90%' name='ingredientInput_" + (ingre_counter+1) + "' type='text' placeholder='Enter your ingredient' required></input>";
          document.getElementById(divName).appendChild(newdiv);
          ingre_counter++;
     }
}

var instr_counter = 1;
function instrInput(divName){
     if (instr_counter == limit)  {
          alert("You have reached the limit of adding " + instr_counter + " inputs");
     }
     else {
          var newdiv = document.createElement('div');
          var num = (instr_counter+1)
          newdiv.id = "instr_" + num.toString();
          newdiv.innerHTML = "<br>"+"<div class= 'w3-col w3-container w3-large w3-margin-top w3-margin-right' style='width:3%'>" + (instr_counter+1) + "." + "</div>" + "<input class='w3-col w3-input w3-border w3-margin-bottom' style='width:90%' id='"+ (instr_counter+1) + "' name='instructionInput_" + (instr_counter+1) + "' type='text' placeholder='Enter your instruction' required></input>";
          document.getElementById(divName).appendChild(newdiv);
          instr_counter++;
     }
}

function inged_removeLast(divName){
	if(ingre_counter == 1){
		alert("At least have one ingredient");
	}else{
		var id = "ingre_" + ingre_counter.toString();
		var del = document.getElementById(id);
		document.getElementById(divName).removeChild(del);
		ingre_counter--;
	}
}

function instr_removeLast(divName){
	if(instr_counter == 1){
		alert("At least have one instruction");
	}else{
		var id = "instr_" + instr_counter.toString();
		var del = document.getElementById(id);
		document.getElementById(divName).removeChild(del);
		instr_counter--;
	}
}