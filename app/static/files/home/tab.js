function changeTab(evt, tabName) {
    var i, x, tablinks;
    x = document.getElementsByClassName("tab");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < x.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" w3-light-grey", " w3-grey");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className = evt.currentTarget.className.replace(" w3-round", "")
    evt.currentTarget.className += " w3-border-top w3-border-left w3-border-right w3-border-grey w3-light-grey ";
}