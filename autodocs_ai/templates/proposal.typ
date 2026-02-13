// Business Proposal template for autodocs-ai

#let proposal(
  title: "Business Proposal",
  author: none,
  company: none,
  date: none,
  client: none,
  body,
) = {
  set page(
    paper: "a4",
    margin: (top: 2.5cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
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

  // Cover page
  v(4cm)
  align(center)[
    #if company != none {
      text(12pt, fill: gray)[#company]
      v(1em)
    }
    #text(28pt, weight: "bold")[#title]
    #v(1em)
    #if client != none {
      text(14pt)[Prepared for: #client]
      v(0.5em)
    }
    #if author != none {
      text(12pt, fill: gray)[Prepared by: #author]
      v(0.3em)
    }
    #if date != none {
      text(11pt, fill: gray)[#date]
    }
  ]
  v(2cm)
  align(center)[
    #line(length: 40%, stroke: 2pt + rgb("#2c3e50"))
  ]
  pagebreak()

  // Section styling
  set heading(numbering: "1.1")

  show heading.where(level: 1): it => {
    v(0.8em)
    text(16pt, weight: "bold", fill: rgb("#2c3e50"))[#it]
    v(0.3em)
    line(length: 100%, stroke: 0.5pt + rgb("#bdc3c7"))
    v(0.3em)
  }

  show heading.where(level: 2): it => {
    v(0.5em)
    text(13pt, weight: "bold", fill: rgb("#34495e"))[#it]
    v(0.2em)
  }

  body
}
