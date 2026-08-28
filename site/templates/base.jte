@import to.etc.sigeto.ContentItem
@import to.etc.sigeto.PageModel

@param PageModel model

<!doctype html>
<html lang="en">
<head>
<title>${model.getTitle()}</title>
<link rel="stylesheet" href='${model.siteURL("css/site.css")}'/>
<link rel="stylesheet" href='${model.siteURL("css/dracula.css")}'/>

<link rel="stylesheet" bhref="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
</head>
<body>
<div class="ui-page-top">
    <div class="ui-page-header">
        <img src='${model.siteURL("img/logo-h126.png")}'>
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
        © 2024 by Frits Jalvingh. All information in here can be freely used (MIT License)
    </div>
</div>

</body>
</html>
