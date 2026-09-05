---
menu:
  sort: "90"
---
# FileUploadMultiple

The same upload as [`FileUpload2`](../fileupload2/index.md), for any number of
files: each one is uploaded as it is chosen, and the value is the list of them.

```java
FileUploadMultiple upload = new FileUploadMultiple("csv", "xlsx");
fb.label("The files to import").control(upload);
...
for(UploadItem item : upload.getValue()) {
    importFrom(item.getFile());
}
```

!demo(to.etc.domuidemo.pages.components.images.FileUploadPage.ui, 100%, 560)

[TOC]

## The difference

It is an `IControl<List<UploadItem>>` rather than an `IControl<UploadItem>`, and
that is nearly the whole of it. The constructors, `setAllowedExtensions()`,
`setMaxSize()`, `setMandatory()`, `setReadOnly()`, `setDisabled()`,
`setOnValueChanged()` and `clear()` are the same calls with the same meanings.

| | `FileUpload2` | `FileUploadMultiple` |
| --- | --- | --- |
| value | one `UploadItem`, or null | a `List<UploadItem>`, never null |
| after a choice | the chooser is replaced by the file's name | the file is added to the list, and the chooser stays |
| mandatory means | something was chosen | the list is not empty |

The chooser staying is the point: the user picks a file, then another, then
another, and each is uploaded when it is picked. Every file gets its own line
with its own button to remove it.

## The same warnings

The files are temporary files of the **conversation** and are deleted when the
user leaves the page, so anything worth keeping is copied out while the page is
still there. The extension and size limits are enforced by the browser, so a
server that cares checks the `UploadItem`s itself. And the screen blocks, with no
progress report, while each file is on its way.
