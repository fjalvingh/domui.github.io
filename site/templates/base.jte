@import to.etc.sigeto.ContentItem
@import to.etc.sigeto.PageModel

@param PageModel model

<!doctype html>
<html lang="en">
<head>
<title>${model.getTitle()} - DomUI</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href='${model.siteURL("img/favicon.ico")}' sizes="any"/>
<link rel="icon" type="image/png" href='${model.siteURL("img/favicon.png")}'/>
<link rel="stylesheet" href='${model.siteURL("css/site.css")}'/>
<link rel="stylesheet" href='${model.siteURL("css/dracula.css")}'/>

<link rel="stylesheet" bhref="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
</head>
<body>
<div class="ui-page-top">
    <div class="ui-page-header">
        <a href='${model.siteURL("index.html")}'><img src='${model.siteURL("img/logo-h126.png")}' alt="DomUI"></a>
    </div>
    <div class="ui-page-nav">
        <div class="ui-page-bc-cont">
            <div class="ui-page-breadcrumb">
                @for(ContentItem item : model.getBreadcrumbPath())
                    <a class="ui-bc-dir ui-bc-item" href="${model.siteURL(item.getRelativeTargetPath())}"><span>${item.getPageTitle()}</span></a>
                @endfor
                <div class="ui-bc-last ui-bc-item"><span>${model.getItem().getPageTitle()}</span></div>
            </div>
        </div>
        <div class="ui-page-nav-end">
            <a href='${model.siteURL("about/index.html")}' class="ui-nav-item">
                <span>About</span>
            </a>
        </div>
    </div>
</div>
<div class="ui-page-middle">
    <div class="ui-page-content">
        <div class="ui-flex-content">
            $unsafe{model.getContent()}
        </div>
    </div>
</div>
<div class="ui-page-bottom">
    @if(model.getPreviousHref() != null || model.getNextHref() != null)
        <div class="ui-blog-nav">
            @if(model.getPreviousHref() != null)
                <a class="ui-blog-nav-prev" href="${model.getPreviousHref()}"><span class="ui-blog-nav-icon">&#8592;</span> ${model.getPreviousTitle()}</a>
            @endif
            @if(model.getNextHref() != null)
                <a class="ui-blog-nav-next" href="${model.getNextHref()}">${model.getNextTitle()} <span class="ui-blog-nav-icon">&#8594;</span></a>
            @endif
        </div>
    @endif
    <div class="ui-page-meta-date">
        Last modified: ${model.getModifiedDateText()}
    </div>
    <div class="ui-page-copyright">
        DomUI is © Frits Jalvingh and contributors, and is released under the
        <a href="https://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html">LGPL 2.1</a>.
        This documentation can be freely used.
    </div>
</div>

</body>
</html>
