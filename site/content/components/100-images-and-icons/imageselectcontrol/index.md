---
menu:
  sort: "70"
---
# ImageSelectControl

A picture the user can replace: the thumbnail, a button to clear it, and a file
chooser behind the picture itself.

```java
ImageSelectControl avatar = new ImageSelectControl();
avatar.setDisplayDimensions(new Dimension(96, 96));
avatar.setMaxDimensions(new Dimension(512, 512));
fb.label("Your avatar").control(avatar);
```

!demo(to.etc.domuidemo.pages.components.images.ImageUploadPage.ui, 100%, 600)

[TOC]

## The two sizes

They are different things, and both matter:

| Method | What it is |
| --- | --- |
| `setDisplayDimensions(Dimension)` | how big the thumbnail on the screen is (default 32x32) |
| `setMaxDimensions(Dimension)` | what an uploaded picture is **resized down to** before it is kept (default 1024x1024) |

So a control that shows a 96-pixel avatar but keeps a 512-pixel picture sets
both. The second one is the one that decides what ends up in the database.

## The value

It is an `IControl<IUIImage>`, so it behaves like every other control:
`getValue()`, `setValue()`, `setMandatory()`, `setReadOnly()`, `setDisabled()`,
`setOnValueChanged()`, and a `FormBuilder` binds it to a property like any other.

What it produces is a `LoadedImage` over the uploaded file, resized to
`maxDimensions`, and that file is registered as a temporary file of the
**conversation**:

!! The uploaded file is deleted when the conversation ends. A page that wants to
!! keep the picture has to read it and store it - in a blob, on disk, wherever -
!! while the user is still on the page. Nothing is saved for you.

| Method | What it does |
| --- | --- |
| `setEmptyIcon(IIconRef)` | what is shown when there is no picture (default: the theme's empty icon) |
| `setEmptyIcon(Class<?>, String)` | the same, as a java resource beside a class |

## What the user can do

Pressing the picture opens the file chooser; choosing a file uploads it straight
away and the thumbnail becomes the new picture. The button next to it clears the
value. Both fire `onValueChanged`.

The chooser accepts `.jpg`, `.jpeg`, `.png` and `.gif`, at up to 10MB - that is
fixed in the control, not a property. Anything the picture is not, or anything
ImageMagick cannot identify, comes back as a flare saying the image is invalid,
and the old value stays.

## Just showing one

For the same picture without the editing - a list of avatars, a detail screen
that may not be changed - use [`DisplayImage`](../displayimage/index.md), which
is the read-only half of the same mechanism and takes the same `IUIImage`.
