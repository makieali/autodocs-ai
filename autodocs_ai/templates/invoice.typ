// Invoice template for autodocs-ai

#let invoice(
  invoice-number: "INV-001",
  date: none,
  due-date: none,
  from-name: "Your Company",
  from-address: none,
  to-name: "Client Name",
  to-address: none,
  items: (),
  tax-rate: 0,
  notes: none,
  body,
) = {
  set page(
    paper: "a4",
    margin: (top: 2cm, bottom: 2cm, left: 2.5cm, right: 2.5cm),
  )

  set text(
    font: "Linux Libertine",
    size: 10pt,
    lang: "en",
  )

  // Header
  grid(
    columns: (1fr, 1fr),
    align(left)[
      #text(28pt, weight: "bold", fill: rgb("#2c3e50"))[INVOICE]
      #v(0.3em)
      #text(10pt, fill: gray)[#invoice-number]
    ],
    align(right)[
      #text(14pt, weight: "bold")[#from-name]
      #if from-address != none {
        v(0.2em)
        text(9pt, fill: gray)[#from-address]
      }
    ],
  )

  v(1em)
  line(length: 100%, stroke: 2pt + rgb("#2c3e50"))
  v(1em)

  // Dates and client info
  grid(
    columns: (1fr, 1fr),
    [
      #text(9pt, weight: "bold", fill: gray)[BILL TO]
      #v(0.2em)
      #text(11pt, weight: "bold")[#to-name]
      #if to-address != none {
        v(0.1em)
        text(9pt)[#to-address]
      }
    ],
    align(right)[
      #if date != none {
        text(9pt, fill: gray)[Date: ]
        text(10pt)[#date]
        v(0.2em)
      }
      #if due-date != none {
        text(9pt, fill: gray)[Due: ]
        text(10pt, weight: "bold")[#due-date]
      }
    ],
  )

  v(1.5em)

  // Heading style
  show heading.where(level: 1): it => {
    v(0.5em)
    text(12pt, weight: "bold", fill: rgb("#2c3e50"))[#it.body]
    v(0.3em)
  }

  body
}
