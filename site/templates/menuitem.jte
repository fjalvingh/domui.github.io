@import to.etc.sigeto.ContentItem
@import to.etc.sigeto.MenuItem
@import to.etc.sigeto.PageModel

@param PageModel model
@param MenuItem rootItem

@for(MenuItem item : rootItem.getSubItemList())
    @if(model.mustShowItem(item))
        <div class=" cl-${model.isCurrentItem(item)}">${item.getTitle()}</div>
        @if(!item.getSubItemList().isEmpty())
            <div class="ui-menu-level ui-menu-level-${item.getItemLevel()}">
                @template.menuitem(model, item)
            </div>
        @endif
    @endif
@endfor
