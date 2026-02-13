// Base template for autodocs-ai documents
// Provides common styling and page setup

#let autodocs-base(
  title: none,
  author: none,
  date: none,
  body,
) = {
  // Page setup
  set page(
    paper: "a4",
    margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
    header: context {
      if counter(page).get().first() > 1 [
        #set text(8pt, fill: gray)
        #title
        #h(1fr)
        #author
      ]
    },
    footer: context {
      set text(8pt, fill: gray)
      h(1fr)
      counter(page).display("1 / 1", both: true)
      h(1fr)
    },
  )

  // Typography
  set text(
    font: "Linux Libertine",
    size: 11pt,
    lang: "en",
  )

  set par(
    justify: true,
    leading: 0.65em,
  )

  // Headings
  set heading(numbering: "1.1")
  show heading.where(level: 1): it => {
    set text(14pt, weight: "bold")
    v(0.5em)
    it
    v(0.3em)
  }

  show heading.where(level: 2): it => {
    set text(12pt, weight: "bold")
    v(0.4em)
    it
    v(0.2em)
  }

  // Title block
  if title != none {
    align(center)[
      #text(20pt, weight: "bold")[#title]
      #v(0.5em)
      #if author != none {
        text(12pt)[#author]
      }
      #if date != none {
        v(0.3em)
        text(10pt, fill: gray)[#date]
      }
    ]
    v(1em)
    line(length: 100%, stroke: 0.5pt + gray)
    v(1em)
  }

  body
}
