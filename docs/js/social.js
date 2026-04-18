Social = {
    facebook: function(ptitle, pimg, text) {
        url = 'http://www.facebook.com/sharer.php?s=100';
        url += '&p[title]=' + encodeURIComponent(ptitle);
        url += '&p[summary]=' + encodeURIComponent(text);
        url += '&p[url]=' + encodeURIComponent(window.location.href);
        url += '&p[images][0]=' + encodeURIComponent(pimg);
        Social.popup(url);
    },
    twitter: function(ptitle) {
        url = 'http://twitter.com/share?';
        url += encodeURIComponent('text=A new Medical AI Dataset is ready to share: ' + ptitle);
        url += '&url=' + encodeURIComponent(window.location.href);
        url += '&counturl=' + encodeURIComponent(window.location.href);
        Social.popup(url);
    },
    linkedin: function(ptitle, text) {
        // https://www.linkedin.com/shareArticle?mini=true&url={articleUrl}&title={articleTitle}&summary={articleSummary}&source={articleSource}
        url = 'https://www.linkedin.com/shareArticle?mini=true';
        url += '&url=' + encodeURIComponent(window.location.href);
        url += '&title=' + encodeURIComponent(ptitle);
        url += '&summary=' + encodeURIComponent(text);
        Social.popup(url);
    },
    popup: function(url) {
        window.open(url, '', 'toolbar=0,status=0,width=626, height=436');
    }
};