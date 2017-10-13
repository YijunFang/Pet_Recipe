var ingre_counter = 1;
var limit = 500;
function ingedInput(divName){
     if (ingre_counter == limit)  {
          alert("You have reached the limit of adding " + ingre_counter + " inputs");
     }
     else {
          var newdiv = document.createElement('div');
          newdiv.innerHTML = "<br>"+"<div class= 'w3-col w3-container w3-large w3-margin-top w3-margin-right' style='width:3%'>" + (ingre_counter+1) + "." + "</div>" + "<input class='w3-col w3-input w3-border w3-margin-bottom' style='width:90%' name='ingrediantInputs[]' type='text' placeholder='Enter your ingrediant'></input>";
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
          newdiv.innerHTML = "<br>"+"<div class= 'w3-col w3-container w3-large w3-margin-top w3-margin-right' style='width:3%'>" + (instr_counter+1) + "." + "</div>" + "<input class='w3-col w3-input w3-border w3-margin-bottom' style='width:90%' name='instructionInputs[]' type='text' placeholder='Enter your instruction'></input>";
          document.getElementById(divName).appendChild(newdiv);
          instr_counter++;
     }
}