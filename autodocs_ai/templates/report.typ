// Technical Report template for autodocs-ai

#let report(
  title: "Technical Report",
  author: none,
  organization: none,
  date: none,
  abstract: none,
  body,
) = {
  set page(
    paper: "a4",
    margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
    header: context {
      if counter(page).get().first() > 1 [
        #set text(8pt, fill: gray)
        #title
        #h(1fr)
        #if organization != none { organization }
      ]
    },
    footer: context {
      set text(8pt, fill: gray)
      h(1fr)
      counter(page).display("1 / 1", both: true)
      h(1fr)
    },
  )

  set text(
    font: "Linux Libertine",
    size: 11pt,
    lang: "en",
  )

  set par(
    justify: true,
    leading: 0.65em,
  )

  // Title page
  v(3cm)
  align(center)[
    #if organization != none {
      text(11pt, fill: gray)[#organization]
      v(1.5em)
    }
    #text(24pt, weight: "bold")[#title]
    #v(1.5em)
    #if author != none {
      text(13pt)[#author]
      v(0.5em)
    }
    #if date != none {
      text(11pt, fill: gray)[#date]
    }
  ]

  if abstract != none {
    v(2cm)
    align(center)[
      #rect(
        width: 85%,
        inset: 1em,
        stroke: 0.5pt + gray,
        [
          #text(11pt, weight: "bold")[Abstract]
          #v(0.3em)
          #text(10pt)[#abstract]
        ],
      )
    ]
  }
  pagebreak()

  // Table of contents
  outline(indent: 1.5em, depth: 3)
  pagebreak()

  // Section styling
  set heading(numbering: "1.1")

  show heading.where(level: 1): it => {
    v(0.8em)
    text(16pt, weight: "bold")[#it]
    v(0.3em)
  }

  show heading.where(level: 2): it => {
    v(0.5em)
    text(13pt, weight: "bold")[#it]
    v(0.2em)
  }

  show heading.where(level: 3): it => {
    v(0.3em)
    text(11pt, weight: "bold", style: "italic")[#it]
    v(0.1em)
  }

  body
}
