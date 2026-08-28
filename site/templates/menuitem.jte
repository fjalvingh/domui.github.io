@import to.etc.sigeto.MenuItem
@import to.etc.sigeto.PageModel

@param PageModel model
@param MenuItem rootItem

<ul class="ui-menu-level ui-menu-level-${rootItem.getItemLevel()}">
    @for(MenuItem item : rootItem.getSubItemList())
        @if(model.mustShowItem(item))
            <li class="ui-menu-item ${model.isOpenItem(item) ? "ui-menu-open" : ""} ${model.isCurrentItem(item) ? "ui-menu-current" : ""}">
                <a href="${model.menuHref(item)}">${item.getTitle()}</a>
                @if(item.hasChildren() && model.isOpenItem(item))
                    @template.menuitem(model, item)
                @endif
            </li>
        @endif
    @endfor
</ul>
