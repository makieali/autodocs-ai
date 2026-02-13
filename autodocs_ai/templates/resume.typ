// Resume/CV template for autodocs-ai

#let resume(
  name: "Your Name",
  title: none,
  email: none,
  phone: none,
  location: none,
  website: none,
  body,
) = {
  set page(
    paper: "a4",
    margin: (top: 2cm, bottom: 2cm, left: 2cm, right: 2cm),
  )

  set text(
    font: "Linux Libertine",
    size: 10pt,
    lang: "en",
  )

  set par(
    justify: true,
    leading: 0.6em,
  )

  // Name and title
  align(center)[
    #text(24pt, weight: "bold")[#name]
    #if title != none {
      v(0.2em)
      text(12pt, fill: gray)[#title]
    }
    #v(0.4em)

    // Contact info line
    #set text(9pt)
    #{
      let items = ()
      if email != none { items.push(email) }
      if phone != none { items.push(phone) }
      if location != none { items.push(location) }
      if website != none { items.push(website) }
      items.join("  |  ")
    }
  ]

  v(0.5em)
  line(length: 100%, stroke: 1pt + black)
  v(0.5em)

  // Section styling
  show heading.where(level: 1): it => {
    v(0.5em)
    text(12pt, weight: "bold", fill: rgb("#2c3e50"))[#upper(it.body)]
    v(0.1em)
    line(length: 100%, stroke: 0.5pt + rgb("#2c3e50"))
    v(0.3em)
  }

  show heading.where(level: 2): it => {
    text(11pt, weight: "bold")[#it.body]
  }

  body
}
