# CV source — asadchattha.com

`cv.html` is the single source of truth for Muhammad Asad's résumé.
Design follows brittanychiang.com/resume (one page, two column, accent headings)
with the portfolio's teal brand (#0f766e) on white for print and ATS safety.

## Rebuild the PDF

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --print-to-pdf=cv_preview.pdf --no-pdf-header-footer \
  "file://$PWD/cv.html"
cp cv_preview.pdf ../main/public/resume.pdf
```

Body is locked to `height: 297mm; overflow: hidden` so it can never spill to a
second page. If content is added, shrink `font-size` / `line-height` on `body`.
