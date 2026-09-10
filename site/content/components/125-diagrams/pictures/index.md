---
menu:
  sort: "50"
---
# A picture of the drawing

The diagram as a file, in svg or png. Where it goes is two different questions,
and there is a method for each:

```java
bb.addButton("Save as PNG", () -> panel.download(GraphExportFormat.Png, "diagram.png"));

bb.addButton("Mail it", () -> panel.export(GraphExportFormat.Png, 2.0, image -> {
    File png = image.saveTo(File.createTempFile("diagram", ".png"));
    mailer.send(png);
}));
```

!demo(to.etc.domuidemo.pages.components.graph.ExportGraphPage.ui, 100%, 850)

[TOC]

## Saving, and exporting

| Method | What happens |
| --- | --- |
| `download(GraphExportFormat, String fileName)` | the browser makes the picture and hands it to the user. Nothing reaches the server |
| `download(GraphExportFormat, double scale, String fileName)` | the same, drawn this many times its own size |
| `export(GraphExportFormat, IGraphExportHandler)` | the picture is posted back here and the handler is given it |
| `export(GraphExportFormat, double scale, IGraphExportHandler)` | the same, at that size |

`download()` is what a "save this drawing" button wants: the drawing is in the
browser and so is the file, so nothing has to travel. `export()` is for the
application that has to *keep* the thing - put it in a report, mail it, store it
next to the record it belongs to.

Both are commands, like [arranging](../arranging/index.md): they make a picture
of the drawing as it is at that moment, not of the model as the page built it.

## What the handler gets

```java
public interface IGraphExportHandler {
    void exported(GraphExport image) throws Exception;
}
```

`GraphExport` carries the file and its size: `getData()` the bytes,
`getWidth()` and `getHeight()` the picture in pixels, `getFormat()` and
`getMimeType()` what it is, and `saveTo(File)` writes it out. The size is worth
having, because it is something the server cannot work out for itself.

The picture arrives **in a request of its own**, a moment after the one that
asked for it - making it takes the browser as long as it takes to draw. That
request is an ordinary one, so the handler may change the page like any other:
show what came back, enable a button, or hand the file to the user with
`TempFilePart.createDownloadAction()`.

!! An exported picture travels over the ordinary page POST, and containers limit
!! how big that may be - two megabytes for Tomcat, by default. A drawing big
!! enough to make a picture bigger than that is one to `download()` instead,
!! which has no such limit because nothing is posted at all.

## What is in the picture

The whole drawing, whatever part of it is scrolled into view and whatever the
user has zoomed to. It is not a copy of what is on the screen: the picture is
drawn again into a document of its own, so it has none of the handles, none of
the selection, and nothing of the page around it.

- **`Svg` is vector**, and the one to take when the picture is to be printed,
  scaled or edited afterwards. The scale sets its nominal size and nothing else.
- **`Png` is pixels**, at the size the scale asks for - which is why a picture
  meant for print is worth asking for at 2.0 - and it is drawn on white, because
  a transparent png is printed on whatever it lands on.

!! A picture carries nothing it would have to fetch: a node whose shape is an
!! image, or a font the drawing does not itself contain, is not in the png. The
!! shapes, lines, colours and labels of an ordinary diagram all are.
