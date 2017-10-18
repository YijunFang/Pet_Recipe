var ingre_counter_base = 0;
var limit = 500;
function ingedInput(divName, base){
     var ingre_counter = ingre_counter_base + base;
     if (ingre_counter == limit)  {
          alert("You have reached the limit of adding " + ingre_counter + " inputs");
     }
     else {
          var newdiv = document.createElement('div');
          var num = (ingre_counter+1)
          newdiv.id = "ingre_" + num.toString();
          newdiv.innerHTML = "<br>"+"<div class= 'w3-col w3-container w3-large w3-margin-right' style='width:3%'>" + (ingre_counter+1) + "." + "</div>" + "<input class='w3-col w3-input w3-border w3-margin-bottom' style='width:90%' name='ingredientInput_" + (ingre_counter+1) + "' type='text' placeholder='Enter your ingredients' required></input>";
          document.getElementById(divName).appendChild(newdiv);
          ingre_counter_base++;
     }
}

var instr_counter_base = 0;
function instrInput(divName, base){
     var instr_counter = instr_counter_base + base;
     if (instr_counter == limit)  {
          alert("You have reached the limit of adding " + instr_counter + " inputs");
     }
     else {
          var newdiv = document.createElement('div');
          var num = (instr_counter+1)
          newdiv.id = "instr_" + num.toString();
          newdiv.innerHTML = "<br>"+"<div class= 'w3-col w3-container w3-large w3-margin-top w3-margin-right' style='width:3%'>" + (instr_counter+1) + "." + "</div>" + "<input class='w3-col w3-input w3-border w3-margin-bottom' style='width:90%' id='"+ (instr_counter+1) + "' name='instructionInput_" + (instr_counter+1) + "' type='text' placeholder='Enter your instructions' required></input>";
          document.getElementById(divName).appendChild(newdiv);
          instr_counter_base++;
     }
}

function inged_removeLast(divName, base){
     var ingre_counter = ingre_counter_base + base;
     if(ingre_counter == 1){
          alert("At least have one ingredient");
     }else{
          var id = "ingre_" + ingre_counter.toString();
          var del = document.getElementById(id);
          document.getElementById(divName).removeChild(del);
          ingre_counter_base--;
     }
}

function instr_removeLast(divName,base){
     var instr_counter = in_counter_base + base;
     if(instr_counter == 1){
          alert("At least have one instruction");
     }else{
          var id = "instr_" + instr_counter.toString();
          var del = document.getElementById(id);
          document.getElementById(divName).removeChild(del);
          instr_counter_base--;
     }
}