window.onload = function () {
    var pagerElem = document.getElementById('pager');
    var scroller = document.getElementById('scroller');
    var scrollButton = document.getElementById('triangle-up');

    window.onscroll = function (event) {

        var scrollHeight = document.documentElement.scrollHeight;
        var clientHeight = document.documentElement.clientHeight;
        var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        var height = document.documentElement.clientHeight;
        var percent = Math.round((scrollTop) / (document.body.scrollHeight - height) * 100);

        if (isNaN(percent)) {
            percent = 0;
        }
        if (percent < 0) {
            percent = 0;
        } else if (percent > 100) {
            percent = 100;
        }
        pagerElem.innerHTML = percent + "%";
        pagerElem.onclick = function () {
            if (scrollTop) {
                sc = scrollTop;
                document.body.scrollTop = document.documentElement.scrollTop = 0;
            } else {
                window.scrollTo(0, sc);
            }
        }
    };
    inputElements = document.querySelectorAll('input, textarea');
    submitBtn = document.querySelector('input[type="submit"]');
    inputFunc = function(){
        if (this.value.length > 0){
            this.style.borderColor = '';
        }
    }
    for (i = 0; i < inputElements.length; i++) {
        inputElements[i].oninput = inputFunc;
    }
    submitBtn.onmouseover = function () {
        for (i = 0; i < inputElements.length; i++) {
            elem = inputElements[i];
            if (elem.value == ''){
                elem.style.borderColor = 'red';
            }
        }
    }
}
var xmlhttp;
function loadXMLDoc() {
    if (window.XMLHttpRequest)
    {
        xmlhttp = new XMLHttpRequest();
    } else{
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function(){
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            document.getElementById('ajaxer').innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET", "/getdate", true);
        xmlhttp.send()

}
var timer = setInterval(function() {
  loadXMLDoc();
}, 2000);
