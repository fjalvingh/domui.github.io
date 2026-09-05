---
menu:
  sort: "80"
---
# FileUpload2

One file, uploaded the moment the user chooses it. There is nothing to submit:
by the time the handler runs, the file is on the server.

```java
FileUpload2 upload = new FileUpload2("png", "jpg", "gif");
upload.setMaxSize(4 * 1024 * 1024);
upload.setOnValueChanged(a -> store(upload.getValue()));
fb.label("An image").control(upload);
```

!demo(to.etc.domuidemo.pages.components.images.FileUploadPage.ui, 100%, 560)

[TOC]

## Making one

| Constructor | What it gives |
| --- | --- |
| `FileUpload2()` | anything the user picks |
| `FileUpload2(String... extensions)` | ...restricted to those extensions |
| `FileUpload2(List<String>)` | the same, from a list |

An extension may be written with or without its dot, and a mime type with a
slash in it (`image/*`) is passed through as one.

| Method | What it does |
| --- | --- |
| `setAllowedExtensions(List<String>)` / `getAllowedExtensions()` | change what may be chosen |
| `setMaxSize(int bytes)` | the largest file that may be chosen (default 100MB) |
| `setValue(UploadItem)` / `getValue()` | the file; setting null empties the control |
| `clear()` | empty it, closing the file, and fire `onValueChanged` |
| `setOnClearClicked(IClicked<FileUpload2>)` | take over what the clear button does |
| `setMandatory(boolean)` | `getValue()` throws a validation exception when nothing was chosen |

It is an `IControl<UploadItem>`, so `setReadOnly()`, `setDisabled()` and data
binding all work the way they do on any other control.

## What you get

```java
UploadItem item = upload.getValue();
item.getRemoteFileName();     // The name it had on the user's machine
item.getContentType();        // What the browser said it is
item.getSize();               // In bytes
item.getFile();               // Where it landed on the server
```

!! That `File` belongs to the **conversation**: it is deleted when the user
!! leaves the page. A page that wants to keep the contents must copy them
!! somewhere while it still can.

## How it gets there

Choosing a file fires an `onchange` in the browser, which posts the file to the
server in the background - a hidden form of its own, not the page's request. The
control then rebuilds itself: the file chooser is replaced by the file's name and
a button to clear it, and `onValueChanged` runs.

The screen blocks while the file is on its way and there is **no progress
report**, so this is a component for files a user waits a moment for, not for
gigabytes.

## Where the checking happens

The allowed extensions and the maximum size are handed to the browser, which
uses them to filter its file chooser and to refuse anything else.

!! That check is the browser's, and a browser is not to be trusted. A server that
!! cares what it was given checks the `UploadItem` - its name, its size, its
!! actual content - itself.

For any number of files at once, use
[`FileUploadMultiple`](../fileuploadmultiple/index.md), which is the same
component with a list for a value. For a picture that has to be *shown* as well
as uploaded, [`ImageSelectControl`](../imageselectcontrol/index.md) does both.
