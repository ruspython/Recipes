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
        /* scroller.onmouseover = function () {
            pager.style.display = 'none';
            scrollButton.style.display = 'block';
            scroller.style.backgroundColor = '#ccc'
        }
        scroller.onmouseout =  function () {
            pager.style.display = '';
            scrollButton.style.display = 'none';
        }
        */
    };
}